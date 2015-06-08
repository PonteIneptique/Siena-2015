from src.xml import Parse, Verse

from src.language import Lemmatize
from src.language.lemmatizer import LatinCLTK

from src.search import Search, windowMaker
from src.weight import Level, DistanceBalance
from src.compute import Compute
from src.algorithm.topic import LDA
#We need to install data, don't forget to run "install.py"

# We first need to process the XML resource
RawText = Parse("./resources/normalized.virgil.perseus.xml", Verse)
# We lemmatize the text then
LemmSet = Lemmatize(RawText, LatinCLTK)
# Now we search for occurences
ResultSet = (Search(LemmSet, ["mors", "letum", "morior"], windowMaker(500))).process()
"""
# We want to weight our ResultSet to take into account the distance
ResultSetWeighted = Level(ResultSet, DistanceBalance)
ResultSetWeighteds.toString()
# Now, we compute what we want to compute !
# You said topic modeling ?
C = Compute(ResultSet, LDA)
"""