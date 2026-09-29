import re
from sentence_transformers.util import cos_sim
import numpy as np
import pickle


# The variable name is tokenized into a phrase.
def segment_word(token):
    camel_words = re.sub(r'([a-z])([A-Z])', r'\1 \2', token)
    snake_words = re.sub('_', ' ', camel_words)
    return snake_words.lower()


# The average of the word embeddings in the phrase is used as the phrase embedding.
def get_phrase_vector(phrase, model):
    words = phrase.split()
    word_vectors = [model[word] for word in words if word in model]
    if len(word_vectors):
        return np.mean(word_vectors, axis=0)
    else:
        return None


def cal_word_sim(model_name, model, variable):
    with open('predefined_files/fields.txt', 'r', encoding='UTF-8') as file:
        field_words = file.read().split('\n')
    if model_name == 'Word2Vec':
        with open('predefined_files/embeddings/field_embeddings_Word2Vec.pkl', 'rb') as f:
            vectors = pickle.load(f)
    elif model_name == 'Glove':
        with open('predefined_files/embeddings/field_embeddings_Glove.pkl', 'rb') as f:
            vectors = pickle.load(f)
    elif model_name == 'FastText':
        with open('predefined_files/embeddings/field_embeddings_FastText.pkl', 'rb') as f:
            vectors = pickle.load(f)
    else:
        print('The model does not exist!')

    phrase = segment_word(variable)
    word_vec = get_phrase_vector(phrase, model)
    if word_vec is None:
        sim_score = 0
        # print(f"{variable} ({phrase}) => (score:{sim_score})")
    else:
        cosine_sim = cos_sim(word_vec, vectors)
        arr = cosine_sim[0].numpy()
        max_sim = max(arr)
        # pos = np.where(arr == max_sim)
        # print(f"{variable} ({phrase}) => {field_words[pos[0][0]]} (score:{max_sim})")
        sim_score = round(max_sim, 2)
    return sim_score
