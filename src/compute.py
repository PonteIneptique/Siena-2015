from .result import ResultSet

def Compute(data, algorithm):
  A = algorithm(data)
  A.process()
  return A
