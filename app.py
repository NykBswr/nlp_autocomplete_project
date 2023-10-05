from flask import Flask, render_template, request, jsonify

# N-GRAM
from ngram import autocomngram, unigram_model, bigram_model, trigram_model

# BILSTM 
from bilstm import bilstm_predict

app = Flask(__name__)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/bilstm')
def bilstm():
    return render_template('bilstm.html')

# Route for N-GRAM results
@app.route('/autocomngram', methods=['POST'])
def get_autocomngram():
    prefix = request.form.get('prefix', '').strip().lower()
    suggestions = autocomngram(prefix, unigram_model, bigram_model, trigram_model)
    suggestion_list = [suggestion[0] for suggestion in suggestions]
    return jsonify({'suggestions': suggestion_list})


# Route for BILSTM results
@app.route('/autocombilstm', methods=['POST'])
def get_autocombilstm():
    prefix = request.form.get('prefix', '').strip().lower()
    
    suggestions = bilstm_predict(prefix)
    
    return jsonify({'suggestions2': suggestions})


if __name__ == '__main__':
    app.run(debug=True)