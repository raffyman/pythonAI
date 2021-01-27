from py2neo import Graph, NodeMatcher
from py2neo.data import Node
import aiml
import colorful as cf
import random
import spacy
import graph

nlp = spacy.load("en_core_web_sm")

k = None


def pprint(*args):
    print(cf.magenta("[respond]:"), *args)


def init(kernel):
    global k
    k = kernel


def reply(query, user=None):
    """ generates a response of the bot """

    fallback = lambda query: k.respond(query)

    if k is None:
        raise "call init() with kernel"

    if not query.endswith("?"):
        print(cf.red("AIML fallback"))
        return fallback(query)

    # remove stop words
    doc = nlp(query)

    words = [w for w in doc if w.is_punct == False]
    wordst = [w.text for w in doc if w.is_punct == False]
    pprint(list(words))

    proper_nouns = [w.text for w in words if w.pos_ == "PROPN"]
    nouns = [w.text for w in words if w.pos_ == "NOUN"]

    pprint("proper-nouns", proper_nouns)

    # check if the sentences is about "I"

    if "I" in query and len(proper_nouns) == 0:
        at_i = wordst.index("I")
        if words[at_i].dep_ == "nsubj":
            if user:
                # make I a proper noun by replace with user's name
                res = graph.run("MATCH (p:Person{ip: '%s'}) RETURN p" % user["ip"])
                user = res.next()
                proper_nouns.append(user[0].get("name"))

    elif len(proper_nouns) == 0:
        print(cf.red("AIML fallback"))
        return fallback(query)

    if len(proper_nouns) == 1:
        pnoun = proper_nouns[0]

        query = "MATCH (p{name: '%s'})-[r]->(n) RETURN p, type(r), n" % pnoun
        res = graph.run(query)

        for row in res:
            p, rel, n = row.values()
            # pprint(p, rel, n)
            # pprint("words", words)

            # search in rels
            rel_mask = [word.text in rel.lower() for word in words]
            n_mask = [word.text in str(n.labels).lower() for word in words]

            if any(rel_mask):
                # found in the relationship
                word = words[rel_mask.index(True)]
                pprint("word", word)
                return "{} {} {}".format(p["name"], word, n["name"])
            elif any(n_mask):
                # check the node
                word = words[n_mask.index(True)]
                pprint("word", word)
                return "{} {} {} {}".format(p["name"], word, rel.lower(), n["name"])

        print(cf.red("AIML fallback"))
        return fallback(query)


if __name__ == "__main__":
    pass
    #
    # testing
    #

    q = "What do I like?"
    k = aiml.Kernel()
    import botloader

    botloader.init(k)
    init(k)

    user = {"ip": "23.21.4.2"}
    res = reply(q, user)
    pprint("reply", res)
