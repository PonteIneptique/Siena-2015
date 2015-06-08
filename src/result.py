from .texts import Occurence


class ResultSet(object):
  def __init__(self):
    self.data = {}
    self._occurences =()

  def keys(self):
    return (key for key in self.data)

  def rows(self, key):
    return (occ for occ in self.data[key])

  def occurences(self):
    occ = []
    for key in self.data:
      for line in self.data[key]:
        occ.append(Occurence(text=line, ref="-".join([line[0][3], line[-1][3]]), topic=key))
    return occ

  def append(self, key, value):
    self.data[key] = value

  def toString(self):
    s = []
    for key in self.data:
      for value in self.data[key]:
        s.append("{0} [{2}-{3}]: {1}".format(key, " ".join([v[1] for v in value]), value[0][3], value[-1][3]))
    return "\n".join(s)