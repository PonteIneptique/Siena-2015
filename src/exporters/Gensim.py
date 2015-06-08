from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import PCA as skPCA
import matplotlib.pyplot as pyplot
from collections import namedtuple
class GensimExporter(object):
  def __init__(self, model, dictionary):
    self.model = model
    self.dictionary = dictionary

class PCA(GensimExporter):
  """ @Original : https://gist.github.com/tokestermw/3588e6fbbb2f03f89798 """
  def topics_to_vectorspace(self, n_topics, n_words=100):
    rows = []
    for i in range(n_topics):
      temp = self.model.show_topic(i, n_words)
      row = dict(((i[1],i[0]) for i in temp))
      rows.append(row)
    return rows  
   
  def export(self, query, n_topics, n_words, title="PCA Export", fname="PCAExport"):
    vec = DictVectorizer()
    
    rows = self.topics_to_vectorspace(n_topics, n_words)
    X = vec.fit_transform(rows)
    pca = skPCA(n_components=2)
    X_pca = pca.fit(X.toarray()).transform(X.toarray())
    
    match = []
    for i in range(n_topics):
      topic = [t[1] for t in self.model.show_topic(i, len(self.dictionary.keys()))]
      m = None
      for word in topic:
        if word in query:
          match.append(word)
          break

    pyplot.figure()
    for i in range(X_pca.shape[0]):
      pyplot.scatter(X_pca[i, 0], X_pca[i, 1], alpha=.5)
      pyplot.text(X_pca[i, 0], X_pca[i, 1], s=' '.join([str(i), match[i]]))  
     
    pyplot.title(title)
    pyplot.savefig(fname)
     
    pyplot.close()
     
Node = namedtuple("Node", ["id", "text", "type"])
Edge = namedtuple("Edge", ["source", "target", "weight"])

class Graph(GensimExporter):   
  def export(self, query, n_topics, n_words, force=True, fname="PCAExport"):
    """ Force : force an edge between query words and topic words """
    nodes = []
    edges = []
    treated = []
    for q in query:
      nodes.append(Node("q-"+q, q, "query"))

    rows = [self.model.show_topic(i, len(self.dictionary.keys())) for i in range(n_topics)]
    nodes = nodes + [Node(id=i, text="Topic " + str(i+1), type="topic") for i in range(n_topics)]

    for i in range(n_topics):
      topic = [t[1] for t in rows[i]]
      for word in query:
        z = topic.index(word)
        edges.append(Edge(source=word, target=i, weight=rows[i][z][0]))

    for i in range(n_topics):
      topic = rows[i][0:n_words]
      for word in topic:
        edges.append(Edge(source=word[1], target=i, weight=word[0]))
        if word[1] not in treated:
          nodes.append(Node(id=word[1], text=word[1], type="lemma"))

    with open(fname.format("nodes"), "w") as f:
      f.write("\n".join([";".join([str(e) for e in list(node)]) for node in nodes]))
      f.close()

    with open(fname.format("edges"), "w") as f:
      f.write("\n".join([";".join([str(e) for e in list(edge)]) for edge in edges]))
      f.close()