import traceback;
from scipy.sparse import dok_matrix;
from random import random, choice; 
from numpy import float64, array, multiply;

corpus = ""
with open("messages.txt", 'r', encoding="utf8") as f:
        corpus+=f.read()
corpus = corpus.replace('\n',' ')
corpus = corpus.replace('\t',' ')
corpus = corpus.replace('“', ' " ')
corpus = corpus.replace('”', ' " ')
for spaced in ['.','-',',','!','?','(','—',')']:
    corpus = corpus.replace(spaced, ' {0} '.format(spaced))
print(len(corpus))

corpus_words = corpus.split(' ')
corpus_words = [word for word in corpus_words if word != '']
print(len(corpus_words))

distinct_words = list(set(corpus_words))
word_idx_dict = {word: i for i, word in enumerate(distinct_words)}
print(len(list(set(corpus_words))))

k = 3
sets_of_k_words = [ ' '.join(corpus_words[i:i+k]) for i, w in enumerate(corpus_words[:-k]) ]
distinct_sets_of_k_words = list(set(sets_of_k_words))
next_after_k_words_matrix = dok_matrix((len(distinct_sets_of_k_words), len(distinct_words)))
k_words_idx_dict = {word: i for i, word in enumerate(distinct_sets_of_k_words)}
for i, word in enumerate(sets_of_k_words[:-k]):
    word_sequence_idx = k_words_idx_dict[word]
    next_word_idx = word_idx_dict[corpus_words[i+k]]
    next_after_k_words_matrix[word_sequence_idx, next_word_idx] +=1

def weighted_choice(objects, weights):
    weights = array(weights, dtype=float64)
    sum_of_weights = weights.sum()
    multiply(weights, 1 / sum_of_weights, weights)
    weights = weights.cumsum()
    x = random()
    for i in range(len(weights)):
        if x < weights[i]:
            return objects[i]

def sample_next_word_after_sequence(word_sequence, alpha=0):
    next_word_vector = next_after_k_words_matrix[
        k_words_idx_dict[word_sequence]
    ] + alpha
    likelihoods = next_word_vector/next_word_vector.sum()
    return weighted_choice(distinct_words, likelihoods.toarray())
    
def stochastic_chain(seed, chain_length = 30):
    current_words = seed.split(" ")
    sentence = seed
    for j in range(chain_length - len(current_words)):
        next_word = sample_next_word_after_sequence(" ".join(current_words))
        sentence += f" {next_word}"
        current_words = current_words[1:] + [next_word]
    return sentence

while True:
    try:
        inp = input("Input seed words and chain length:\n").lower().split(" ")
        if inp == ["0"]: exit()
        words = inp[:-1]
        chain_length = int(inp[-1])
        if len(words) < k:
            num = len(words)
            inds = [i for i, j in enumerate(corpus_words) if i + num <= len(corpus_words) and corpus_words[i:i+num] == words]
            ind = choice(inds)
            words = corpus_words[ind:ind+k]
        print(stochastic_chain(" ".join(words), chain_length))
    except Exception as e: 
        print(traceback.format_exc())
        print(e)
