from .model import Algorithm
from lda.lda import LDA as PyLDA
from lda.utils import lists_to_matrix
import numpy as np

def flatten(l):
  return [x for y in l for x in y]


class LDA(Algorithm):
  def subnormalize(self, row):
    output = []
    id = row[0]
    row = row[1]
    for tup in row:
      output.append(tup[1])
      """
      if tup[2]:
        output.append(tup[1]+"-"+tup[2])
      """
    ids = [id]*len(output)
    return list(zip(output, ids))

  def normalize(self, key):
    data = self.source.rows(key)
    rows = [(docId, value) for docId, value in enumerate(data)]
    normalized = [self.subnormalize(row) for row in rows]
    flat = flatten(normalized)
    words, documents = zip(*flat)

    words = list(words)
    documents = list(documents)

    # We need the dictionary
    ws = list(set(words))
    #Could be avoided with search or so
    wordsDict = {}
    for i, w in enumerate(ws):
      wordsDict[w] = i
    # words = [[wordsDict[word] for word in tup[1]] for tup in normalized]
    words = [[wordsDict[tup[0]] for tup in sentence] for sentence in normalized]
    documents = [docId for docId, value in enumerate(data)]
    print(words)
    return words, documents, ws


  def subprocess(self, key):
    model = PyLDA(n_topics=20, n_iter=1)
    words, documents, wordsDict = self.normalize(key)
    matrix = lists_to_matrix(words, documents)
    model.fit_transform(matrix)
    return (model, documents, wordsDict)

  def process(self):
    self.output = [(key, self.subprocess(key)) for key in self.source.keys()]

  def toString(self):
    output = []
    for key, resources in self.output:
      model, documents, vocab = resources
      output.append("Result for {0}".format(key))
      topic_word = model.topic_word_  # model.components_ also works
      n_top_words = 20
      for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        output.append('Topic {}: {}'.format(i, ' '.join(topic_words)))
      output.append("")
    return "\n".join(output)
