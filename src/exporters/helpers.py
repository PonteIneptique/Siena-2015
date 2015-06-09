from collections import namedtuple

Node = namedtuple("Node", ["id", "text", "type"])
Edge = namedtuple("Edge", ["source", "target", "weight"])

def row(length):
    """ Create a namedtuple of length column + label """
    rows = ["label"] + ["topic"+str(i) for i in range(length)]
    return namedtuple("Row", rows)
