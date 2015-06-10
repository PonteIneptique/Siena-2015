from src.xml import Parse, Content

from src.language import Lemmatize
from src.language.lemmatizer import LatinCLTK, FrenchNLTK

from src.compute import Compute

from src.algorithm.adapter import GensimAdapter
from src.algorithm import Gensim
from src.exporters.Gensim import PCA, Graph, TopWords, Text
from src.result import ResultSet as RS
#We need to install data, don't forget to run "install.py"

# We first need to process the XML resource
RawText = Parse("./resources/tcp_raw.xml", Content)
# We lemmatize the text then
LemmSet = Lemmatize(RawText, FrenchNLTK, stopwords=True)

""" To be : fromReftoResultSet """
resultset = {}
for data in LemmSet:
    if data.lemma is not None:
        if data.ref not in resultset:
            resultset[data.ref] = []
        resultset[data.ref].append([data])

ResultSet = RS()
for doc in resultset:
    ResultSet.append(doc, resultset[doc])
"""
# Now we search for occurences
ResultSet = (Search(LemmSet, ["mors", "letum", "morior"], windowMaker(500))).process()
"""
G = GensimAdapter(ResultSet)

tfidf = Gensim.tfidf(G.GensimObject)

lsi = Gensim.LDA(tfidf)
lsi.process(num_topics=10)
d = lsi.model.print_topics(10)

exports = {}
exports["Json"] = TopWords(lsi.model, tfidf.dictionary)
exports["Json"].export(query=[], n_topics=10, n_words=10, mode="json", fname="presentation/topics.json")

exports["Text"] = Text(lsi.model, tfidf.dictionary)
exports["Text"].export(query=[], n_topics=10, n_words=10, fname="presentation/topics.txt")

exports["TW"] = TopWords(lsi.model, tfidf.dictionary)
exports["TW"].export(query=[], n_topics=10, n_words=10, mode="markdown", fname="presentation/Text.md")

exports["Graph"] = Graph(lsi.model, tfidf.dictionary)
exports["Graph"].export(query=[], n_topics=10, n_words=10, force=True, fname="graph-LDA-{0}.csv")
"""
exports["PCA"] = PCA(lsi.model, tfidf.dictionary)
exports["PCA"].export(query=[], n_topics=50, n_words=500, title="PCA Topics of Aeneid Death", fname="LDA")
"""