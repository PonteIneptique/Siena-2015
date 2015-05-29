from src.xml import Parse, Verse
from src.language import LatinCLTK, Lemmatize

#We need to install data, don't forget to run "install.py"

# We first need to process the XML resource
RawText = Parse("./resources/normalized.virgil.perseus.xml", Verse)
# We lemmatize the text then
LemmSet = Lemmatize(RawText, LatinCLTK)
print(LemmSet)