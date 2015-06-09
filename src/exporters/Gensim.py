from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import PCA as skPCA
import matplotlib.pyplot as pyplot
from collections import namedtuple
from .helpers import Node, Edge, row

from .writers import TextWriter, TopWordsWriter

class GensimExporter(object):
  def __init__(self, model, dictionary):
    self.model = model
    self.dictionary = dictionary


def topics_to_vectorspace(model, n_topics, n_words=100):
  rows = []
  for i in range(n_topics):
    temp = model.show_topic(i, n_words)
    row = dict(((i[1],i[0]) for i in temp))
    rows.append(row)
  return rows  


class PCA(GensimExporter):
  """ @Original : https://gist.github.com/tokestermw/3588e6fbbb2f03f89798 """
   
  def export(self, query, n_topics, n_words, title="PCA Export", fname="PCAExport"):
    vec = DictVectorizer()
    
    rows = topics_to_vectorspace(self.model, n_topics, n_words)
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
     

class Graph(GensimExporter):   
  def export(self, query, n_topics, n_words, force=True, fname="PCAExport"):
    """ Force : force an edge between query words and topic words """
    nodes = [Node("id", "label", "type")]
    edges = [Edge("source", "target", "weight")]
    treated = []
    for q in query:
      nodes.append(Node("q-"+q, q, "query"))

    rows = [self.model.show_topic(i, len(self.dictionary.keys())) for i in range(n_topics)]
    nodes = nodes + [Node(id=i, text="Topic " + str(i+1), type="topic") for i in range(n_topics)]

    for i in range(n_topics):
      topic = [t[1] for t in rows[i]]
      for word in query:
        z = topic.index(word)
        edges.append(Edge(source="q-"+word, target=i, weight=rows[i][z][0]))

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

class TopWords(GensimExporter):   
  def export(self, query, n_topics, n_words, markdown=True, fname="TopWords.txt"):
    """
      Should have a force parameter to register each word score for each topic 
    """
    Row = row(n_topics)
    legend = [Row(*list(["Word"] + ["Topic "+str(i) for i in range(n_topics)]))]
    # We need the top 20 words
    rows = [self.model.show_topic(i, n_words) for i in range(n_topics)]
    # We need a dict of all words for all topic
    dic  = topics_to_vectorspace(self.model, n_topics, len(self.dictionary.keys()))
    # Query
    topics = [Row(*list([topic] + [dic[n][topic] for n in range(n_topics)])) for topic in query]
    words = {}
    for r in rows:
      for word in r:
        if word[1] not in words:
          words[word[1]] = Row(*list([word[1]] + [dic[n][word[1]] for n in range(n_topics)]))
    
    # We send to the writer
    TopWordsWriter(legend, [words[word] for word in words], topics, markdown, fname)


class Text(GensimExporter):   
  def export(self, query=None, n_topics=10, n_words=20, fname="TextExport.txt"):
    """
      Should have a force parameter to register each word score for each topic 
    """
    topics = list()
    # We need the top n_words words
    rows = [self.model.show_topic(i, n_words) for i in range(n_topics)]
    # We need a dict of all words for all topic
    if query is not None:
      dic  = topics_to_vectorspace(self.model, n_topics, len(self.dictionary.keys()))
      topics = [list([topic] + [dic[n][topic] for n in range(n_topics)]) for topic in query]

    TextWriter(rows, topics, fname)
