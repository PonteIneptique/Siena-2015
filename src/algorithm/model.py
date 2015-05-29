class Algorithm(object):
  def __init__(self, data):
    self.source = data
    self.output = []

  def process(self):
    raise NotImplementedError