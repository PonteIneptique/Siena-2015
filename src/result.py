class ResultSet(object):
  def __init__(self):
    self.data = {}

  def keys(self):
    return (key for key in self.data)

  def rows(self, key):
    return (occ for occ in self.data[key])

  def append(self, key, value):
    self.data[key] = value

  def toString(self):
    s = []
    for key in self.data:
      for value in self.data[key]:
        s.append("{0} [{2}-{3}]: {1}".format(key, " ".join([v[1] for v in value]), value[0][3], value[-1][3]))
    return "\n".join(s)