import pickle
import pandas as pd
import nltk
nltk.download('punkt')
from nltk import word_tokenize

df = pd.read_csv('cleared_medium_title.csv', sep=',')

text = " ".join(df['Judul'])
docs_clear = text.split()
string = " ".join(docs_clear)
tokens = word_tokenize(string)

data_list = df['Judul'].values.tolist()
