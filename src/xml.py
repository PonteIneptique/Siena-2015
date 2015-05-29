from lxml import etree
from .cache import Cache


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
