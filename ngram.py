import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
from data import tokens
import string

# Menghitung frekuensi unigram, bigram, dan trigram
unigram_model = Counter(tokens)

def count_ngrams(tokens):
    bigram_model = Counter([(tokens[i], tokens[i+1]) for i in range(len(tokens) - 1)])
    trigram_model = Counter([(tokens[i], tokens[i+1], tokens[i+2]) for i in range(len(tokens) - 2)])
    return bigram_model, trigram_model

bigram_model, trigram_model = count_ngrams(tokens)

def autocomngram(prefix, unigram_model, bigram_model, trigram_model):
    # Pra-pemrosesan token
    vocabulary = set(tokens)
    tokenized_prefix = word_tokenize(prefix.lower())
    last_bigram = tuple(tokenized_prefix[-2:])
    vocabulary_probabilities = {}

    if not prefix.strip():
        unigram_counter = Counter(unigram_model)
        punctuation_chars = set(string.punctuation)
        frequent = [(word, frequency) for word, frequency in unigram_counter.most_common() if word not in punctuation_chars][:5]
        return frequent 

    elif len(tokenized_prefix) == 1:
        if last_bigram:
            last_unigram = last_bigram[0]
            unigram_count = unigram_model.get(last_unigram, 1)
            for vocabulary_word in vocabulary:
                test_bigram = (last_unigram, vocabulary_word)
                if unigram_count > 0:
                    probability = bigram_model.get(test_bigram, 0) / unigram_count
                    vocabulary_probabilities[vocabulary_word] = probability
    else:
        for vocabulary_word in vocabulary:
            test_trigram = (last_bigram[0], last_bigram[1], vocabulary_word)
            test_bigram = last_bigram
            if bigram_model[test_bigram] > 0 :
                probability = trigram_model.get(test_trigram, 0) / bigram_model[test_bigram]
                vocabulary_probabilities[vocabulary_word] = probability

    suggestions = sorted(vocabulary_probabilities.items(), key=lambda x: x[1], reverse=True)[:5]
    return suggestions