import json
import re
import numpy as np
# from gensim.models import KeyedVectors
from sentence_transformers import SentenceTransformer

from static_analysis.keyword_matching import is_matched_keyword
from static_analysis.word_similarity import cal_word_sim
from static_analysis.phrase_similarity import cal_phrase_sim

app_pkg = 'cn.fangchan.fanzan'

class_field_dir = 'generated_files/class_fields/'
output_file = 'generated_files/phrase_similarity/sorted_tuples/' + app_pkg + '.txt'


# Check whether the variable is obfuscated
def is_obfuscated_var(name):
    # Match variable names（e.g., f1234g）
    pattern_field1 = r'^f\d+[a-z]?$'
    # Match variable names（e.g., a, b0, c12）
    pattern_field2 = r'^[a-z]\d*$'
    # Match variable names（e.g., var1, var2）
    pattern_local = r'^var\d+$'
    return bool(re.match(pattern_field1, name)) or bool(re.match(pattern_field2, name)) or bool(
        re.match(pattern_local, name))


# Check whether it is a constant
def is_constant(name):
    pattern_field = r'^[A-Z_][A-Z0-9_]*$'
    return bool(re.match(pattern_field, name))


# Segment class names into a phrase
def segment_class_name(name):
    camel_words = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
    snake_words = re.sub('_', ' ', camel_words)
    return snake_words.lower().split(' ')


# sort the five-tuple
def sort_tuples(tuples):
    """
    Sorted by max_sim_score, max_num, and class_priority in descending order.
    """
    sorted_tuples = sorted(
        tuples,
        key=lambda x: (-x[2], -x[3], -x[4])
    )
    result = ''
    for item in sorted_tuples:
        print(item)
        result += str(item) + '\n'
    with open(output_file, 'w+') as f:
        f.write(result)


def main():
    """
    Five-tuple: (class, [field_1, field_2,...], max_sim_score, max_num, class_priority)
    """
    with open('predefined_files/classes.txt', 'r') as f:
        pre_classes = f.read().split('\n')
    with open('predefined_files/fields.txt', 'r') as f:
        pre_fields = f.read().split('\n')

    # 1 Load SBert model
    SBert_model = SentenceTransformer('../ExploreRecks/resources/paraphrase-multilingual-MiniLM-L12-v2')

    # 2 Word2Vec, Glove, FastText
    # word2vec_model_path = 'language_models/Word2Vec/GoogleNews-vectors-negative300.bin'
    # word_model = KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True)

    # glove_model_path = 'language_models/Glove_models/glove.6B.300d.word2vec.txt'
    # word_model = KeyedVectors.load_word2vec_format(glove_model_path, binary=False)
    #
    # fasttext_model_path = 'language_models/FastText_models/wiki-news-300d-1M.vec'
    # word_model = KeyedVectors.load_word2vec_format(fasttext_model_path)

    file_path = class_field_dir + app_pkg + '_ClassAndField.json'
    with open(file_path, 'r', encoding='UTF-8') as f:
        jsonObjects = json.load(f)

    data_tuples = []
    for jsonObject in jsonObjects:
        packageName = jsonObject['packageName']
        className = jsonObject['className']
        # Main class
        for pre_class in pre_classes:
            segment_name = segment_class_name(className)
            # Assign a priority score to each class
            if pre_class in segment_name:
                class_score = 0
                if 'user' in segment_name:
                    class_score = 8
                elif 'account' in segment_name:
                    class_score = 7
                elif 'wallet' in segment_name:
                    class_score = 6
                elif 'mine' in segment_name:
                    class_score = 5
                elif 'me' in segment_name:
                    class_score = 4
                elif 'person' in segment_name:
                    class_score = 3
                elif 'entity' in segment_name:
                    class_score = 2
                elif 'reward' in segment_name:
                    class_score = 1

                fieldNames = jsonObject['fieldNames']
                match_fields = []
                field_sim_scores = []
                for fieldName in fieldNames:
                    if not is_obfuscated_var(fieldName) and not is_constant(fieldName):
                        # 1: Keyword Matching
                        # if is_matched_keyword(fieldName):
                        #     match_fields.append(fieldName)

                        # 2: Sentence-level Semantic Matching (Sentence-Bert)
                        sim_score = cal_phrase_sim(SBert_model, fieldName)
                        if sim_score >= np.float32(0.7):
                            match_fields.append(fieldName)
                            field_sim_scores.append(sim_score)

                        # 3: Word-level Semantic Matching (Word2Vec, Glove, FastText)
                        # sim_score = cal_word_sim('Word2Vec', word_model, fieldName)
                        # if sim_score >= np.float32(0.7):
                        #     match_fields.append(fieldName)
                        #     field_sim_scores.append(sim_score)

                if len(match_fields) > 0:
                    # 1 Keyword Matching
                    # class_tuple = (className, match_fields, class_score)
                    # pkg_comp_data.append(class_tuple)
                    # print(class_tuple)

                    # 2-3 Word/Phrase Similarity
                    max_sim_score = max(field_sim_scores)
                    max_score_count = field_sim_scores.count(max_sim_score)
                    class_tuple = (packageName + '.' + className, match_fields, max_sim_score, max_score_count, class_score)
                    data_tuples.append(class_tuple)

                # Inner class
                innerClasses = jsonObject['innerClasses']
                for innerClass in innerClasses:
                    match_innerFields = []
                    inner_field_sim_scores = []
                    innerClassName = innerClass['innerClassName']
                    innerFieldNames = innerClass['innerFieldNames']
                    for innerFieldName in innerFieldNames:
                        if not is_obfuscated_var(innerFieldName) and not is_constant(innerFieldName):
                            # 1: Keyword Matching
                            # if is_matched_keyword(innerFieldName):
                            #     match_innerFields.append(innerFieldName)

                            # 2: Sentence-level Semantic Matching (Sentence-Bert)
                            sim_score = cal_phrase_sim(SBert_model, innerFieldName)
                            if sim_score >= np.float32(0.7):
                                match_innerFields.append(innerFieldName)
                                inner_field_sim_scores.append(sim_score)

                            # 3: Word-level Semantic Matching (Word2Vec, Glove, FastText)
                            # sim_score = cal_word_sim('Word2Vec', word_model, innerFieldName)
                            # if sim_score >= np.float32(0.7):
                            #     match_innerFields.append(innerFieldName)
                            #     inner_field_sim_scores.append(sim_score)

                    if len(match_innerFields) > 0:
                        # 1 Keyword Matching
                        # innerClassName = className + '$' + innerClassName
                        # class_tuple = (innerClassName, match_innerFields, class_score)
                        # pkg_comp_data.append(class_tuple)
                        # print(class_tuple)

                        # 2-3 Word/Phrase Similarity
                        max_sim_score = max(inner_field_sim_scores)
                        max_score_count = inner_field_sim_scores.count(max_sim_score)
                        innerClassName = packageName + '.' + className + '$' + innerClassName
                        class_tuple = (
                            innerClassName, match_innerFields, max_sim_score, max_score_count, class_score)
                        data_tuples.append(class_tuple)
                break

    if len(data_tuples) > 0:
        print('Before sorting:')
        print(data_tuples)
        print('After sorting:')
        sort_tuples(data_tuples)


if __name__ == '__main__':
    main()
