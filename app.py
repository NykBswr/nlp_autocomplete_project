from flask import Flask, render_template, request, jsonify
import pickle
import os
import re
from nltk import word_tokenize, PorterStemmer
from collections import defaultdict
import string
import nltk
from nltk.corpus import stopwords

nltk.download('punkt')

app = Flask(__name__)

# Load data and preprocess it
stop_words = set(stopwords.words('english'))
src_name = '20newsgroup.pckl'

with open(src_name, 'rb') as fin:
    data = pickle.load(fin)

if data:
    docs = [doc for doc in data.data]
    label = data.target

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

    docs_clear = [preprocess(doc) for doc in docs]

    # Build n-gram models for bigram and trigram
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
    quadgram_model = build_ngram_model(docs_clear, 4)
    pentagram_model = build_ngram_model(docs_clear, 5)

    # Autocomplete function using bigram and trigram models
    def autocomplete(prefix, bigram_model, trigram_model, quadgram_model, pentagram_model):
        bigram_suggestions = bigram_model.get(prefix, [])
        trigram_suggestions = trigram_model.get(prefix, [])
        quadgram_suggestions = quadgram_model.get(prefix, [])
        pentagram_suggestions = pentagram_model.get(prefix, [])
        suggestions = bigram_suggestions + trigram_suggestions + quadgram_suggestions + pentagram_suggestions
        return suggestions

    # Route for the main page
    @app.route('/')
    def index():
        return render_template('index.html')

    # Route for autocomplete results
    @app.route('/autocomplete', methods=['POST'])
    def get_autocomplete():
        prefix = request.form['prefix']
        prefix = prefix.strip().lower()
        suggestions = autocomplete(prefix, bigram_model, trigram_model, quadgram_model, pentagram_model)
        max_suggestions = 5
        suggestions = suggestions[:max_suggestions]
        return jsonify({'suggestions': suggestions})

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, render_template, request, jsonify
# import pickle
# import os
# import re
# from nltk import word_tokenize, PorterStemmer
# from collections import defaultdict
# import string
# import nltk
# from nltk.corpus import stopwords

# nltk.download('punkt')

# app = Flask(__name__)

# # Load data and preprocess it
# stop_words = set(stopwords.words('english'))
# src_name = '20newsgroup.pckl'

# with open(src_name, 'rb') as fin:
#     data = pickle.load(fin)

# if data:
#     docs = [doc for doc in data.data]
#     label = data.target

#     # Improved text preprocessing with stemming
#     stemmer = PorterStemmer()

#     def preprocess(doc):
#         sents = word_tokenize(doc)
#         sents_tok = []
#         for s in sents:
#             s = s.strip().lower()
#             s = s.replace("\n", " ")
#             s = re.sub(r"[^a-zA-Z0-9 ]", ' ', s)
#             s = re.sub(' +', ' ', s)
#             s = re.sub(r'\s+', ' ', s)
#             # Apply stemming
#             s = stemmer.stem(s)
#             sents_tok.append(s)
#         return " ".join(sents_tok)

#     docs_clear = [preprocess(doc) for doc in docs]

#     # Build n-gram models for bigram and trigram
#     def build_ngram_model(docs, n):
#         ngram_model = defaultdict(list)
#         for doc in docs:
#             tokens = word_tokenize(doc)
#             for i in range(len(tokens) - n + 1):
#                 ngram = " ".join(tokens[i:i+n])
#                 prefix = " ".join(tokens[i:i+n-1])
#                 suffix = tokens[i+n-1]
#                 ngram_model[prefix].append(suffix)
#         return ngram_model

#     # Membuat model n-gram dinamis sesuai dengan panjang prefix
#     def build_dynamic_ngram_model(docs, max_n):
#         ngram_models = {}
#         for n in range(2, max_n + 1):
#             ngram_models[n] = build_ngram_model(docs, n)
#         return ngram_models

#     # Route for the main page
#     @app.route('/')
#     def index():
#         return render_template('index.html')

#     # Route for autocomplete results
#     @app.route('/autocomplete', methods=['POST'])
#     def get_autocomplete():
#         prefix = request.form['prefix']
#         prefix = prefix.strip().lower()
        
#         # Mendapatkan panjang prefix (jumlah kata dalam prefix)
#         num_words_in_prefix = len(prefix.split())

#         # Membuat model n-gram sesuai dengan panjang prefix
#         if num_words_in_prefix >= 2:
#             max_n = min(num_words_in_prefix, 5)  # Batasan hingga 5-gram
#             ngram_models = build_dynamic_ngram_model(docs_clear, max_n)
#             suggestions = []
#             for n in range(2, max_n + 1):
#                 tokens = prefix.split()[-n:]  # Ambil n kata terakhir dari prefix
#                 ngram_prefix = " ".join(tokens)
#                 ngram_suggestions = ngram_models[n].get(ngram_prefix, [])
#                 suggestions.extend(ngram_suggestions)

#             max_suggestions = 5
#             suggestions = suggestions[:max_suggestions]
#             return jsonify({'suggestions': suggestions})
        
#         return jsonify({'suggestions': []})  # Jika prefix terlalu pendek, kembalikan daftar kosong

# if __name__ == '__main__':
#     app.run(debug=True)
