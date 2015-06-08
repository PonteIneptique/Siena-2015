from collections import namedtuple

Citation  = namedtuple("Citation", ["text", "ref"])
Occurence = namedtuple("Occurence", ["text", "ref", "topic"])
Word = namedtuple("Word", ["word", "lemma", "pos", "ref"])