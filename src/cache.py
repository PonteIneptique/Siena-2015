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
