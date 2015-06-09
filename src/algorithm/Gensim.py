from .model import Algorithm
from .adapter import GensimObject

import gensim.models

class GensimAlgorythm(Algorithm):
  def __init__(self, data):
    if not isinstance(data, GensimObject):
      raise TypeError("Expected GensimObject, got something else")
    self.data = data
    self.model = None

  def process(self, **kwargs):
    self.model = self.method(self.data.corpus, id2word=self.data.dictionary, **kwargs)
    return self.model


class LSI(GensimAlgorythm):
  def __init__(self, data):
    GensimAlgorythm.__init__(self, data)
    self.method = gensim.models.LsiModel


class LDA(GensimAlgorythm):
  def __init__(self, data):
    GensimAlgorythm.__init__(self, data)
    self.method = gensim.models.LdaModel


def tfidf(GO):
  """ GO @GensimObject """
  tfidf = gensim.models.TfidfModel(GO.corpus)
  corpus = tfidf[GO.corpus]
  return GensimObject(corpus, GO.dictionary)
