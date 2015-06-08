import hashlib
from ..cache import Cache
from .words import *
from .lemmatizer import *


def Lemmatize(text, lemmatizer, cachePath=None):
  """ Helper to lemmatize """
  cachetext = "\n".join([cite.text for cite in text])
  path = "cache/" + hashlib.md5(cachetext.encode('utf-8')).hexdigest() + ".lem"
  cache = Cache(path)
  if cache.exists():
    return cache.read()
  process = lemmatizer(text)
  process.parse()
  cache.write(process.data)
  return cache.read()