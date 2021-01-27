import spacy
from spacy import displacy
import pandas as pd

text="Apple has laptop of model MacBook. \
Lenovo has laptop of model Thinkpad.  \
HP has laptop of inspiron."

nlp = spacy.load("en_core_web_sm")
doc = nlp(text)



entities = []
labels = []
position_start = []
position_end = []

for ent in doc.ents:
    entities.append(ent)
    labels.append(ent.label_)
    position_start.append(ent.start_char)
    position_end.append(ent.end_char)

df = pd.DataFrame(
    {'Entities': entities, 'Labels': labels, 'Position_Start': position_start, 'Position_End': position_end})

print(df)