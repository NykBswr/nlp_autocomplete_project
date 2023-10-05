import tensorflow as tf
from tensorflow.keras.models import load_model
from keras.models import Model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from data import data_list

# Load the saved model
model_bilstm = load_model('model_bilstm_fix.h5')

tokenizer = Tokenizer(oov_token='<oov>')
tokenizer.fit_on_texts(data_list)
total_words = len(tokenizer.word_index) + 1
input_sequences = []
for line in data_list:
    token_list = tokenizer.texts_to_sequences([line])[0]
    #print(token_list)

    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)
# pad sequences - menyamakan length dari semuanya
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

# create features and label
xs, labels = input_sequences[:,:-1],input_sequences[:,-1]
ys = tf.keras.utils.to_categorical(labels, num_classes=total_words)

def bilstm_predict(prefix):
    top_n = 5  # Set the number of top predictions you want
    suggestions = []  # Initialize suggestions as an empty list
    # Inisialisasi tokenizer
    seed_text = prefix
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=18, padding='pre')
    predicted = model_bilstm.predict(token_list, verbose=0)

    # Get the indices of the top N predicted words
    predicted_indices = np.argsort(predicted[0])[::-1][:top_n]

    predicted_words = []

    for index in predicted_indices:
        for word, idx in tokenizer.word_index.items():
            if idx == index:
                predicted_words.append(word)
                break

    suggestions.extend(predicted_words) 
    return suggestions
