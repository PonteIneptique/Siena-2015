from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.j_v import JVReplacer
from cltk.tag.pos import POSTag
from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict

from .words import Word
from ..texts import Citation


class Lemmatizer(object):
  def __init__(self, text):
    self.data = defaultdict(list)
    self.refs = []

    if self.normalize:
      self.text = self.normalize(text)
    else:
      self.text = self._normalize(text)

  def _normalize(self, text):
    data = []
    for citation in text:
      line = citation.text.split()
      data = data + line
      for i in range(0, len(line)):
        self.refs[len(refs) + 1] = citation.ref
    return " ".join(data)

  def parse(self):
    raise NotImplementedError()

  def install(self):
    raise NotImplementedError

  def format(self, word=None, lemma=None, pos=None, ref=None):
    return Word(word=word, lemma=lemma, pos=pos, ref=ref)


class LatinCLTK(Lemmatizer):
  """ Lemmatizer using the CLTK Latin Lemmatizer """

  def normalize(self, text):
    """ Normalize the text """
    jv = JVReplacer()
    punkt = RegexpTokenizer(r'\w+')
    data = []

    for citation in text:
      line = punkt.tokenize(jv.replace(citation.text.lower()))
      data = data + line
      self.refs = self.refs + [citation.ref] * len(line)
    return " ".join(data)

  def getLemma(self):
    lemmatizer = LemmaReplacer('latin')
    return lemmatizer.lemmatize(self.text)

  def getPos(self):
    tagger = POSTag('latin')
    return tagger.tag_unigram(self.text)

  def parse(self):
    lemmaList = self.getLemma()
    posList = self.getPos()
    self.data = [self.format(word=posList[i][0], lemma=lemmaList[i], pos=posList[i][1], ref=self.refs[i]) for i in range(0, len(lemmaList))]
    return self.data