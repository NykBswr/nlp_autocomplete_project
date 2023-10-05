import re
from collections import defaultdict

import nltk
nltk.download('punkt')
from nltk import word_tokenize
from nltk.corpus import stopwords
from data import docs_clear
# Load data and preprocess it

def build_ngram_model(docs, n):
    ngram_model = defaultdict(list)
    for doc in docs:
        tokens = word_tokenize(doc)
        for i in range(len(tokens) - n + 1):
            ngram = " ".join(tokens[i:i+n])
            prefix = " ".join(tokens[i:i+n-1])
            suffix = tokens[i+n-1]
            ngram_model[prefix].append(suffix)
    return ngram_model

bigram_model = build_ngram_model(docs_clear, 2)
trigram_model = build_ngram_model(docs_clear, 3)

def autocomngram(prefix, bigram_model, trigram_model):
    bigram_suggestions = bigram_model.get(prefix, [])
    trigram_suggestions = trigram_model.get(prefix, [])
    suggestions = bigram_suggestions + trigram_suggestions 
    return suggestions
