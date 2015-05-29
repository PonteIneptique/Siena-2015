from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.j_v import JVReplacer
from cltk.tag.pos import POSTag
from nltk.tokenize.punkt import PunktLanguageVars
from .cache import Cache
import hashlib
from nltk.tokenize import RegexpTokenizer


class Lemmatizer(object):
  def __init__(self, text):
    self.text = text
    self.data = []

  def parse(self):
    raise NotImplementedError()

  def install(self):
    raise NotImplementedError

  def format(self, word=None, lemma=None, pos=None):
    return (word, lemma, pos)


class LatinCLTK(Lemmatizer):
  def __init__(self, text):
    self.text = self.normalize(text)
    self.data = []

  def normalize(self, text):
    """ Normalize the text """
    jv = JVReplacer()
    punkt = RegexpTokenizer(r'\w+')
    return " ".join(punkt.tokenize(jv.replace(text.lower())))

  def getLemma(self):
    lemmatizer = LemmaReplacer('latin')
    return lemmatizer.lemmatize(self.text)

  def getPos(self):
    tagger = POSTag('latin')
    return tagger.tag_unigram(self.text)

  def parse(self):
    lemmaList = self.getLemma()
    posList = self.getPos()
    self.data = [self.format(word=posList[i][0], lemma=lemmaList[i], pos=posList[i][1]) for i in range(0, len(lemmaList))]
    return self.data


def Lemmatize(text, lemmatizer, cachePath=None):
  text = "\n".join(text)
  path = "cache/" + hashlib.md5(text.encode('utf-8')).hexdigest() + ".lem"

  cache = Cache(path)
  if cache.exists():
    return cache.read()

  process = lemmatizer(text)
  process.parse()
  cache.write(process.data)
  return cache.read()