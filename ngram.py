import re
from collections import defaultdict

import nltk
nltk.download('punkt')
from nltk import word_tokenize, PorterStemmer
from nltk.corpus import stopwords

# Load data and preprocess it
stop_words = set(stopwords.words('english'))

# Improved text preprocessing with stemming
stemmer = PorterStemmer()

def preprocess(doc):
    sents = word_tokenize(doc)
    sents_tok = []
    for s in sents:
        s = s.strip().lower()
        s = s.replace("\n", " ")
        s = re.sub(r"[^a-zA-Z0-9 ]", ' ', s)
        s = re.sub(' +', ' ', s)
        s = re.sub(r'\s+', ' ', s)
        # Apply stemming
        s = stemmer.stem(s)
        sents_tok.append(s)
    return " ".join(sents_tok)

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

def autocomngram(prefix, bigram_model, trigram_model, quadgram_model, pentagram_model):
    bigram_suggestions = bigram_model.get(prefix, [])
    trigram_suggestions = trigram_model.get(prefix, [])
    quadgram_suggestions = quadgram_model.get(prefix, [])
    pentagram_suggestions = pentagram_model.get(prefix, [])
    suggestions = bigram_suggestions + trigram_suggestions + quadgram_suggestions + pentagram_suggestions
    return suggestions
