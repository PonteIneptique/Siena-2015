from ..helpers import flatten
from collections import defaultdict, namedtuple
from gensim import corpora
import hashlib

MmCorpus = corpora.MmCorpus
SvmLightCorpus = corpora.SvmLightCorpus
BleiCorpus = corpora.BleiCorpus
LowCorpus = corpora.LowCorpus

GensimStringCorpora = {
  "MmCorpus" : corpora.MmCorpus,
  "SvmLightCorpus" : corpora.SvmLightCorpus,
  "BleiCorpus" : corpora.BleiCorpus,
  "LowCorpus" : corpora.LowCorpus
}

GensimObject = namedtuple("Gensim", ["corpus", "dictionary"])

class GensimAdapter(object):
  def __init__(self, resultset):
    """ Transform ResultSet object into a Gensim adapted structure """
    self.raw = resultset
    self.documents, self.references = self.toList(self.raw)
    self.filter()
    self.dictionary = corpora.Dictionary(self.documents)
    self.corpus = [self.dictionary.doc2bow(text) for text in self.documents]
    self.GensimObject = GensimObject(self.corpus, self.dictionary)

  def filter(self):
    frequency = defaultdict(int)
    for text in self.documents:
      for token in text:
        frequency[token] += 1
        
    self.documents = [[token for token in text if frequency[token] > 1]
         for text in self.documents]
    return self.documents

  def toList(self, rawdata):
    references = []
    documents  = []

    occurences = rawdata.occurences()
    for occurence in occurences:
      references.append("/".join([occurence.ref, occurence.topic]))
      documents.append(flatten([[element for element in list(word)[0:2] if element is not None] for word in occurence.text]))
    return documents, references

  def tuples(self):
    return list(zip(self.references, self.documents))

  def fname(self, method):
    fname = "/".join(["cache", hashlib.md5(".".join(self.references).encode('utf-8')).hexdigest() + "." + str(method)])
    print(fname)
    return fname

  def serialize(self, method):
    if(type(method) != type):
      method = GensimStringCorpora[method]
    return method.serialize(fname=self.fname(method), corpus=self.corpus)

  def read(self, method, fname=None):
    if(type(method) != type):
      method = GensimStringCorpora[method]
    if fname is None:
      fname = self.fname(method)
    return method.serialize(fname=fname, corpus=self.corpus)

