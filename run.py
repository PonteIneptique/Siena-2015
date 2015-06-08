from src.xml import Parse, Verse

from src.language import Lemmatize
from src.language.lemmatizer import LatinCLTK

from src.search import Search, windowMaker
from src.weight import Level, DistanceBalance
from src.compute import Compute

from src.algorithm.adapter import GensimAdapter
from src.algorithm import Gensim
#We need to install data, don't forget to run "install.py"

# We first need to process the XML resource
RawText = Parse("./resources/normalized.virgil.perseus.xml", Verse)
# We lemmatize the text then
LemmSet = Lemmatize(RawText, LatinCLTK, stopwords=True)
# Now we search for occurences
ResultSet = (Search(LemmSet, ["mors", "letum", "morior"], windowMaker(500))).process()

G = GensimAdapter(ResultSet)

Gensim.tfidf(G.GensimObject)

lsi = Gensim.LSI(G.GensimObject)
lsi.process(num_topics=200)
d = lsi.model.print_topics(50)
print("\n".join(d))
"""
# We want to weight our ResultSet to take into account the distance
ResultSetWeighted = Level(ResultSet, DistanceBalance)
ResultSetWeighteds.toString()
# Now, we compute what we want to compute !
# You said topic modeling ?
C = Compute(ResultSet, LDA)
"""