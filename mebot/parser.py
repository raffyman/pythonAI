import colorful as cf
from collections import defaultdict
import spacy
import model  # ML model for types
import os

ENV = os.getenv("MEBOT_ENV", "PROD")  # default val is PROD

# load the NLP model
nlp = spacy.load("en_core_web_sm")


def pprint(*args):
    print(cf.yellow("[parser]:"), *args)


def go_deep(children, strc):
    """supports single children exploration"""

    for child in children:
        print("c->", child.text, child.dep_, child.pos_)

        # if it is a direct object, see if something modifies it
        if child.dep_ == "dobj":
            strc["dobj"] = child.text
            chl = tuple(child.children)
            for i, c in enumerate(chl):
                if c.pos_ == "NOUN":
                    strc["conj"].append(c.text)
                elif c.dep_ == "det":
                    strc["dobj_det"] = c.text
                else:
                    strc["dobj_attr"].append(c.text)

        if child.dep_ == "pobj":
            strc["pobjs"].append(child.text)

        if child.dep_ == "attr":
            strc["s_attr"] = child.text

        if child.dep_ == "acomp" and child.pos_ == "ADJ":
            strc["s_adj"] = child.text

        if child.pos_ == "ADP":
            strc["adps"].append(child.text)
            go_deep(list(child.children), strc)

        if child.pos_ == "ADV" or child.pos_ == "VERB":
            strc["root"] += "_" + child.text
            go_deep(list(child.children), strc)

    return strc


def parser(sent, verbose=True):
    doc = nlp(sent)  # processing

    ents = doc.ents
    ent_labels = [ent.label_ for ent in ents]
    ent_texts = [ent.text for ent in ents]
    words = [tok.text for tok in doc]
    deps = [tok.dep_ for tok in doc]
    pos = [tok.pos_ for tok in doc]

    if verbose:
        print(cf.green("words:"), words)
        print(cf.green("deps:"), deps)
        print(cf.green("pos:"), pos)
        print(cf.green("ent_labels:"), ent_labels)
        print(cf.green("ent_texts:"), ent_texts)

    # structure of the sentence (to be used to insert in Neo4j)
    strc = defaultdict(list)
    subject = None

    # if it has a subject (which it always will?)
    if deps[0] == "nsubj" or deps[0] == "poss":
        strc["subject"] = doc[0].text
    else:
        raise "No subject found"

    # find root
    ri = deps.index("ROOT")
    if ri:
        root = doc[ri]
    else:
        raise "No root found"

    strc["root"] = root.text

    # store the words right to the root
    # and remove the punctuations
    root_rights = list(filter(lambda x: x.pos_ != "PUNCT", list(doc[ri].rights)))

    # check children of root for a negation
    root_deps = [c.dep_ for c in root.children]
    if "neg" in root_deps:
        ni = root_deps.index("neg")
        strc["root_neg"] = doc[ri + ni].text

    strc = go_deep(root_rights, strc)

    return (strc, list(doc.noun_chunks))


def embed_types(strc, ncs):
    """ embeds type using ML for every thing """
    # subject type
    if strc["subject"]:
        subject = strc["subject"]
        if subject.upper() == "I":
            strc["subject_label"] = "Person"
        else:
            strc["subject_label"] = model.predict(subject)
        pprint("subject_label", strc["subject_label"])

    if strc["dobj"]:
        dobj = strc["dobj"]
        label = model.predict(dobj)
        strc["dobj_label"] = label
        pprint("dobj_label", strc["dobj_label"])

    if strc["s_attr"]:
        s_attr = strc["s_attr"]
        label = model.predict(s_attr)
        strc["s_attr_label"] = label
        pprint("s_attr_label", strc("s_attr_label"))

    if strc["s_adj"]:
        s_adj = strc["s_adj"]
        label = model.predict(s_adj)
        strc["s_adj_label"] = label
        pprint("s_adj_label", strc["s_adj_label"])

    if strc["pobjs"]:
        strc["pobjs_labels"] = []
        for pobj in strc["pobjs"]:
            strc["pobjs_labels"].append(model.predict(pobj))


if __name__ == "__main__":

    #
    # testing
    # THIS IS JUST FOR TESTING. 
    easy_sents = [
        "John likes green apple.",
        "Black is a color.",
        "Mango is Yellow.",
        "I like cats.",
        "John is a programmer.",
        "Mary is a gardner.",
    ]

    medium_sents = [
        "Mouse is not a color.",
        "Mary moved to the garden.",
        "John went to the hallway.",
        "Daniel went back to the hallway.",
        "Sandra moved to the garden.",
        "Ali is driving to Lahore with Ahmed.",
    ]

    test_sents = [
        "John is my father",
        "Cat has a fur.",
        "Cat sat on a mat.",
        "I like my phone.",
        "Water is a liquid.",
        "I have a mouse.",
        "I like music and movies.",
    ]

    new_test_sents = [
        "I have a Cat",
        "Cat's color is brown",
        "Ali is driving to Lahore with Ahmed while eating a pizza in his car",
        "She is buying a stairway to heaven.",
        "Cat is cute",
        "Cat likes milk",
        "I'd like to order pizza",
        "Haider has a big pen.",
    ]

    import graph

    # delete everything from graph
    # this is just for testing
    graph.init()
    graph.delete_all()

    # create a test user
    query = (
        "CREATE (p:Person{name: 'khichi', username: 'khichi', password: 123, ip:"
        " '23.21.4.2'})"
    )
    graph.run(query)

    for sent in new_test_sents:
        print("\n*****")
        strc, ncs = parser(sent)

        user = {"ip": "23.21.4.2"}
        embed_types(strc, ncs)

        print(cf.yellow("strc:"), strc)
        print(cf.yellow("noun chunks:"), ncs)

        graph.make_graph(strc, ncs, clear=False, user=user)
        print("*****")
        if input("next? ") == "n":
            break
