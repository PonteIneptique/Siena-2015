class ResultSet(object):
  def __init__(self):
    self.data = {}

  def append(self, key, value):
    self.data[key] = value

  def toString(self):
    s = []
    for key in self.data:
      for value in self.data[key]:
        s.append("{0} : {1}".format(key, " ".join([v[1] for v in value])))
    return "\n".join(s)


class Finder(object):
  def __init__(self, haystack):
    self.haystack = haystack

  def search(self, needle):
    raise NotImplementedError()


class WindowFinder(object):
  def __init__(self, haystack=[], window=100):
    self.window = window
    self.haystack = haystack

  def search(self, needle):
    indexes = [i for i, v in enumerate(self.haystack) if v[1] == needle]
    results = []
    window = int(self.window / 2)
    max_index = len(self.haystack)

    for index in indexes:
      s = max([0, index - window])
      e = min([max_index, index + window + 1])
      results.append(self.haystack[s:e])
    return results


def windowMaker(rng):
  """ Make a WindowSearch giving a number """
  return lambda **kwargs : WindowFinder(window=rng, **kwargs)


class Search(object):
  def __init__(self, haystack=[], needle=[], farmer=None):
    self.haystack = haystack
    self.needle = needle
    self.farmer = farmer(haystack=self.haystack)
    self.ResultSet = ResultSet()
    self.process()


  def process(self):
    for needle in self.needle:
      self.ResultSet.append(needle, self.farmer.search(needle))
    return self.ResultSet


