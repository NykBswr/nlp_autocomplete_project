from flask import Flask, render_template, request, jsonify
import pickle
from ngram import preprocess, build_ngram_model, autocomngram

app = Flask(__name__)


src_name = '20newsgroup.pckl'

with open(src_name, 'rb') as fin:
    data = pickle.load(fin)

if data:
    docs = [doc for doc in data.data]
    label = data.target

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/bilstm')
def bilstm():
    return render_template('bilstm.html')

docs_clear = [preprocess(doc) for doc in docs]

bigram_model = build_ngram_model(docs_clear, 2)
trigram_model = build_ngram_model(docs_clear, 3)
quadgram_model = build_ngram_model(docs_clear, 4)
pentagram_model = build_ngram_model(docs_clear, 5)

# Route for ngram results
@app.route('/autocomngram', methods=['POST'])
def get_autocomngram():
    prefix = request.form['prefix']
    prefix = prefix.strip().lower()
    suggestions = autocomngram(prefix, bigram_model, trigram_model, quadgram_model, pentagram_model)
    max_suggestions = 5
    suggestions = suggestions[:max_suggestions]
    return jsonify({'suggestions': suggestions})

if __name__ == '__main__':
    app.run(debug=True)