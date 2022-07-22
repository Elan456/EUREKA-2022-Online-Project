import spacy
from tqdm import tqdm
from spacytextblob.spacytextblob import SpacyTextBlob  # Necessary for the spacytextblob pipe to be added
from not_recognize import get_verb

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe('spacytextblob')  # Adds sentiment analysis when nlp is used

sent = nlp("worst. worse. bad.")


for i, token in enumerate(sent):
    print(token, token.tag_, spacy.explain(token.tag_), "|||", token.pos_, spacy.explain(token.pos_), "|||", token.dep_, spacy.explain(token.dep_), "lemma:", token.lemma_, "|", "getverb:", get_verb(token), "HEAD:", token.head.text)
    if token.lemma_.lower() == "alexa" and token.head.lemma_ == "voice":
        print("\n\nTALKING ABOUT ALEXA's voice\n\n")