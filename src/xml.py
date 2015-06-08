from lxml import etree

from .cache import Cache
from .texts import Citation


class Parser(object):
  def __init__(self, path):
    self.path = path
    self.data = ()
    self.read()

  def read(self):
    raise NotImplementedError

  def parse(self):
    raise NotImplementedError

  def toString(self):
    for x in self.data:
      print("{0} : {1}".format(self.data[x].ref, self.data[x].text))

class Verse(Parser):
  def read(self):
    """ Read the file and put it in the object """
    with open(self.path, "r") as xml:
      self.xml = etree.parse(xml)
      xml.close()

  def cts(self, line):
    if line.get("n"):
      parent = line.getparent().get("n")
      return ".".join([parent, line.get("n")])
    return ""

  def parse(self):
    """ Parse the file """
    data = self.xml.xpath("//l")    
    self.data = [Citation(text=line.text, ref=self.cts(line)) for line in data if line.text is not None]
    return self.data

def Parse(path, reader=Verse):
  """ Parse the XML lines of a Text"""
  cache = Cache(path)
  #if cache.exists():
  #  return cache.read()
  xml = reader(path)
  data = xml.parse()
  cache.write(data)
  return cache.read()
