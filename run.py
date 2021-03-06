from src.xml import Parse, Verse

from src.language import Lemmatize
from src.language.lemmatizer import LatinCLTK

from src.search import Search, windowMaker
from src.weight import Level, DistanceBalance
from src.compute import Compute

from src.algorithm.adapter import GensimAdapter
from src.algorithm import Gensim
from src.exporters.Gensim import PCA, Graph, TopWords, Text

#We need to install data, don't forget to run "install.py"

# We first need to process the XML resource
RawText = Parse("./resources/normalized.virgil.perseus.xml", Verse)
# We lemmatize the text then
LemmSet = Lemmatize(RawText, LatinCLTK, stopwords=True)
# Now we search for occurences
ResultSet = (Search(LemmSet, ["mors", "letum", "morior"], windowMaker(500))).process()

G = GensimAdapter(ResultSet)

tfidf = Gensim.tfidf(G.GensimObject)

lsi = Gensim.LDA(tfidf)
lsi.process(num_topics=50)
d = lsi.model.print_topics(50)

exports = {}
exports["Json"] = TopWords(lsi.model, tfidf.dictionary)
exports["Json"].export(query=["mors", "letum", "morior"], n_topics=50, n_words=20, mode="json", fname="presentation/topics.json")

exports["Text"] = Text(lsi.model, tfidf.dictionary)
exports["Text"].export(query=["mors", "letum", "morior"], n_topics=50, n_words=20, fname="presentation/topics.txt")

exports["TW"] = TopWords(lsi.model, tfidf.dictionary)
exports["TW"].export(query=["mors", "letum", "morior"], n_topics=50, n_words=20, mode="markdown", fname="presentation/Text.md")
"""
exports["Graph"] = Graph(lsi.model, tfidf.dictionary)
exports["Graph"].export(query=["mors", "letum", "morior"], n_topics=50, n_words=20, force=True, fname="graph-LDA-{0}.csv")

exports["PCA"] = PCA(lsi.model, tfidf.dictionary)
exports["PCA"].export(query=["mors", "letum", "morior"], n_topics=50, n_words=500, title="PCA Topics of Aeneid Death", fname="LDA")
"""