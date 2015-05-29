from lxml import etree
import os.path
import pickle


class Cache(object):
  def __init__(self, path):
    self.path = path
    self.cachedPath = "/".join(["cache", path.split("/")[-1]])

  def exists(self):
    """ Tell if the cache exists for given Path """
    return os.path.isfile(self.cachedPath)

  def write(self, data):
    """ Write some cache in pickle """
    with open(self.cachedPath, "wb") as c:
      pickle.dump(data, c)
      return True

  def read(self):
    """ Read some pickle cache """
    data = None
    with open(self.cachedPath, "rb") as c:
      data = pickle.load(c)
      c.close()
    return data


class Parser(object):
  def __init__(self, path):
    self.path = path
    self.read()

  def read(self):
    raise NotImplementedError

  def parse(self):
    raise NotImplementedError


class Verse(Parser):
  def read(self):
    """ Read the file and put it in the object """
    with open(self.path, "r") as xml:
      self.xml = etree.parse(xml)
      xml.close()

  def parse(self):
    """ Parse the file """
    data = self.xml.xpath("//l")
    self.data = [line.text for line in data]
    return self.data


def Parse(path, reader=Verse):
  """ Parse the XML lines of a Text"""
  cache = Cache(path)
  if cache.exists():
    return cache.read()
  xml = reader(path)
  data = xml.parse()
  cache.write(data)
  return cache.read()
