from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.j_v import JVReplacer
from cltk.tag.pos import POSTag
from cltk.stop.latin.stops import STOPS_LIST as STOPS_LIST_LATIN
from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import FrenchStemmer
from collections import defaultdict

from ..texts import Citation, Word


class Lemmatizer(object):
  def __init__(self, text, **kwargs):
    self.data = defaultdict(list)
    self.refs = []

    if self.normalize:
      self.text = self.normalize(text, **kwargs)
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

  def normalize(self, text, stopwords):
    """ Normalize the text """
    jv = JVReplacer()
    punkt = RegexpTokenizer(r'\w+')
    data = []

    for citation in text:
      line = punkt.tokenize(jv.replace(citation.text.lower()))
      data = data + line
      self.refs = self.refs + [citation.ref] * len(line)

    if stopwords:
      return " ".join([lem for lem in data if lem not in STOPS_LIST_LATIN])
    else:
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


class FrenchNLTK(Lemmatizer):
  """ Lemmatizer using the CLTK Latin Lemmatizer """

  def normalize(self, text, stopwords):
    """ Normalize the text """
    jv = JVReplacer()
    punkt = RegexpTokenizer(r'\w+')
    data = []

    for citation in text:
      line = punkt.tokenize(jv.replace(citation.text.lower()))
      data = data + line
      self.refs = self.refs + [citation.ref] * len(line)
    return data

  def getLemma(self):
    stemmer = FrenchStemmer(ignore_stopwords=True)
    return [stemmer.stem(word) for word in self.text]


  def getPos(self):
    stemmer = FrenchStemmer(ignore_stopwords=True)
    return [(word, "") for word in self.text]

  def parse(self):
    lemmaList = self.getLemma()
    posList = self.getPos()
    self.data = [self.format(word=posList[i][0], lemma=lemmaList[i], pos=posList[i][1], ref=self.refs[i]) for i in range(0, len(lemmaList)) if lemmaList[i] is not None]
    return self.data

    