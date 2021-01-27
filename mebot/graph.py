from joblib import load
from py2neo import Graph, NodeMatcher, RelationshipMatcher
from py2neo.data import Node, Relationship
import colorful as cf
import py2neo
import os

ENV = os.getenv("MEBOT_ENV", "PROD")  # default val is PROD

# ----
# credentials
uri = "bolt://3.90.84.205:34732"
pswd = "swaps-alloy-classrooms"
# ----

# global graph instance
graph = None

# global nodematcher instance
nodematcher = None

# global relmatcher instance
relmatcher = None


def init():
    global graph
    global nodematcher
    global relmatcher

    if graph is None and nodematcher is None and relmatcher is None:
        graph = Graph(uri, password=pswd)
        nodematcher = NodeMatcher(graph)
        relmatcher = RelationshipMatcher(graph)


def get_graph_instance():
    init()
    return graph


def get_nodematcher_instance():
    init()
    return nodematcher


def get_relmatcher_instance():
    init()
    return relmatcher


def delete_all():
    init()
    graph.delete_all()


def run(query):
    init()
    return graph.run(query)


def pprint(*args):
    print(cf.cyan("[graph]:"), *args)


def merge(node1_label, node1_props, rel, node2_label, node2_props, prev_id=None):
    """ merges a node with an existing node if it exits, otherwise creates it """

    pprint(
        cf.red("merge"),
        node1_label,
        node1_props,
        "-",
        rel,
        "->",
        node2_label,
        node2_props,
        cf.red("prev_id"),
        prev_id,
    )

    rel = rel.upper()  # convention

    if prev_id is not None:
        # if prev_id is provided we want to chain the new node
        query = """
                    MATCH(n)
                    WHERE id(n) = %d
                    MERGE (n)-[r:%s]->(n2:%s %s)
                    RETURN id(n), id(r), id(n2)
                """ % (
            prev_id,
            rel,
            node2_label,
            py2neo.cypher.cypher_repr(node2_props),
        )
    else:
        query = """
                    MERGE (n1:%s %s)
                    MERGE (n1)-[r:%s]->(n2:%s %s)
                    RETURN id(n1), id(r), id(n2)
                """ % (
            node1_label,
            py2neo.cypher.cypher_repr(node1_props),
            rel,
            node2_label,
            py2neo.cypher.cypher_repr(node2_props),
        )

    pprint("query", query)
    # pprint(node1_label, node1_props, "-", rel, "->", node2_label, node2_props)
    # replace node1 (I) basically with the user

    if ENV == "DEV" and input("looks good? ") == "n":
        exit(1)

    res = graph.run(query)
    return res.next()


def get_user_id(user):
    """if there is a user supplied we want to replace I with it"""
    query = "MATCH (p:Person{ip: '%s'}) RETURN id(p)" % user["ip"]
    res = graph.run(query)
    return res.next()[0]


def make_graph(strc, ncs, clear=False, user=None):
    init()

    node1 = strc["subject"]
    node1_label = strc["subject_label"]
    node1_props = {"name": node1}

    rel = strc["root"]

    # check for negation
    if strc["root_neg"]:
        rel += "_" + strc["root_neg"]

    # node2 can be a dobj, s_attr, pobj, dobj_attr, [s_adj (one noun)]
    node2 = None
    if len(ncs) == 1:
        node2 = strc["s_adj"]
        node2_label = strc["s_adj_label"]
    else:
        # assign them their labels
        if strc["dobj"]:
            node2 = strc["dobj"]
            node2_label = strc["dobj_label"]
        elif strc["s_attr"]:
            node2 = strc["s_attr"]
            node2_label = strc["s_attr_label"]

    node2_props = {"name": node2}

    # dobj attributes
    if len(strc["dobj_attr"]):  # list of attributes
        node2_props["dobj_attr"] = strc["dobj_attr"]
    if strc["dobj_det"]:
        node2_props["dobj_det"] = strc["dobj_det"]

    # if len(ncs) > 2:
    if not node2:
        # if there still isn't a second object,
        # take one from pobjs

        # making sure this is true
        # assert len(ncs) - 1 == len(strc["pobjs"]) == len(strc["adps"])

        r, n = strc["adps"].pop(0), strc["pobjs"].pop(0)

        # append rel to root

        rel += "_" + r

        node2_label = strc["pobjs_labels"].pop()
        node2_props["name"] = node2 = n

    pprint(
        "before func",
        node1_label,
        node1_props,
        "-",
        rel,
        "->",
        node2_label,
        node2_props,
    )

    if user is not None and node1.upper() == "I":
        node1 = get_user_id(user)
        id1, id2, id3 = merge(None, None, rel, node2_label, node2_props, node1)
    else:
        id1, id2, id3 = merge(node1_label, node1_props, rel, node2_label, node2_props)

    # more than two nows? not done then, yet
    if len(ncs) > 2:
        for rel, node, label in zip(strc["adps"], strc["pobjs"], strc["pobjs_labels"]):
            node_props = {"name": node}
            pprint(node1, "-", rel, "->", node_props)
            id1, id2, id3 = merge(None, None, rel, label, node_props, id3)


if __name__ == "__main__":
    pass
    #
    # testing
    # delete_all()
    # merge("Cat", "Is", {"type": "cute"})
    # merge("Cat", "Likes", "Milk")
