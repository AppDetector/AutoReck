from sentence_transformers.util import cos_sim
import re
import pickle


# The variable name is tokenized into a phrase.
def segment_word(token):
    # 1. CamelCase: longVariableName
    # 2. snake_case: long_variable_name
    # 3. CamelCase + snake_case: Long_VariableName
    # ==> long variable name
    camel_words = re.sub(r'([a-z])([A-Z])', r'\1 \2', token)
    snake_words = re.sub('_', ' ', camel_words)
    return snake_words.lower()


def cal_phrase_sim(model, variable):
    with open('predefined_files/fields.txt', 'r', encoding='UTF-8') as file:
        field_words = file.read().split('\n')
    with open('predefined_files/embeddings/field_embeddings_SBERT.pkl', 'rb') as f:
        vectors = pickle.load(f)
    phrase = segment_word(variable)
    phrase_vec = model.encode(phrase)
    cosine_sim = cos_sim(phrase_vec, vectors)
    arr = cosine_sim[0].numpy()
    max_sim = max(arr)
    # pos = np.where(arr == max_sim)
    # print(f"{variable} ({phrase}) => {field_words[pos[0][0]]} (score:{max_sim})")

    # sim_score = round(max_sim, 1)
    sim_score = round(max_sim, 2)
    return sim_score
