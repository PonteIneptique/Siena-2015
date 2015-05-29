from .result import ResultSet

class Balance(object):
  def __init__(self, source):
    self.source = source
    self.ResultSet = ResultSet()

  def balance(self):
    raise NotImplementedError


class DistanceBalance(Balance):
  def occBalance(self, key, data):
    index = [i for i, v in enumerate(data) if v[1] == key][0]
    result = []
    for i, v in enumerate(data):
      if i == index:
        result.append(v)
      else:
        for i in range(0, abs(index - i)):
          result.append(v)
    return result

  def balance(self):
    for key in self.source.keys():
      data = []
      for result in self.source.rows(key):
        data.append(self.occBalance(key, result))
      self.ResultSet.append(key, data)
    return self.ResultSet


def Level(ResultSet, weighter):
  W = weighter(ResultSet)
  W.balance()
  return W.ResultSet
