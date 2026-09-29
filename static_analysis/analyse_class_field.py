import json
import re
import numpy as np
# from gensim.models import KeyedVectors
from sentence_transformers import SentenceTransformer

from static_analysis.keyword_matching import is_matched_keyword
from static_analysis.phrase_similarity import cal_phrase_sim
from static_analysis.word_similarity import cal_word_sim

app_pkg = 'cn.fangchan.fanzan'

class_field_dir = 'generated_files/class_fields/'
output_file = 'generated_files/phrase_similarity/data_raw/' + app_pkg + '.txt'


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


def main():
    with open('predefined_files/classes.txt', 'r') as f:
        pre_classes = f.read().split('\n')
    with open('predefined_files/fields.txt', 'r') as f:
        pre_fields = f.read().split('\n')
    file_path = class_field_dir + app_pkg + '_ClassAndField.json'
    with open(file_path, 'r', encoding='UTF-8') as f:
        jsonObjects = json.load(f)
    # print(len(jsonObjects))

    # 1 Load SBert model
    SBert_model = SentenceTransformer('../ExploreRecks/resources/paraphrase-multilingual-MiniLM-L12-v2')

    # 2 Word2Vec, Glove, FastText
    # word2vec_model_path = 'language_models/Word2Vec/GoogleNews-vectors-negative300.bin'
    # word_model = KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True)
    #
    # glove_model_path = 'language_models/Glove_model/glove.6B.300d.word2vec.txt'
    # word_model = KeyedVectors.load_word2vec_format(glove_model_path, binary=False)
    #
    # fasttext_model_path = 'language_models/FastText_model/wiki-news-300d-1M.vec'
    # word_model = KeyedVectors.load_word2vec_format(fasttext_model_path)

    for jsonObject in jsonObjects:
        packageName = jsonObject['packageName']
        className = jsonObject['className']
        # Main class
        for pre_class in pre_classes:
            if pre_class in segment_class_name(className):
                # print(className)
                fieldNames = jsonObject['fieldNames']
                match_fields = []
                field_sim_scores = []
                for fieldName in fieldNames:
                    if not is_obfuscated_var(fieldName) and not is_constant(fieldName):
                        # 1: Keyword Matching
                        # if is_matched_keyword(fieldName):
                        #     match_fields.append(fieldName)
                        #     # print(f"{packageName}.{className}: {fieldName}")

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
                    # result = "Class Name:" + packageName +'.'+ className +'\n'+ "Field Name:" + str(match_fields)

                    # 2-3 Word/Phrase Similarity
                    max_sim_score = max(field_sim_scores)
                    max_score_count = field_sim_scores.count(max_sim_score)
                    result = "Class Name:" + packageName + '.' + className + '\n' + "Field Name:" + \
                             str(match_fields) + '\n' + "Similarity Scores:" + str(field_sim_scores) + '\n' + \
                             "Max Score:" + str(max_sim_score) + '\n' + "Max Score Count:" + str(max_score_count)
                    print(result)
                    with open(output_file, 'a+') as f:
                        f.write(result + '\n')

                # Inner class
                innerClasses = jsonObject['innerClasses']
                is_match_inner = False
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
                            #     # print(f"{packageName}.{className}${innerClassName}: {innerFieldName}")

                            # 2: Sentence-level Semantic Matching (Sentence-Bert)
                            sim_score = cal_phrase_sim(SBert_model, innerFieldName)
                            if sim_score >= np.float32(0.7):
                                is_match_inner = True
                                match_innerFields.append(innerFieldName)
                                inner_field_sim_scores.append(sim_score)

                            # 3: Word-level Semantic Matching (Word2Vec, Glove, FastText)
                            # sim_score = cal_word_sim('Word2Vec', word_model, innerFieldName)
                            # if sim_score >= np.float32(0.7):
                            #     is_match_inner = True
                            #     match_innerFields.append(innerFieldName)
                            #     inner_field_sim_scores.append(sim_score)

                    if len(match_innerFields) > 0:
                        is_match_inner = True
                        # 1 Keyword Matching
                        # result = "innerClass Name:" + packageName +'.'+ className + '$' + innerClassName + '\n' \
                        #          + "innerField Name:" + str(match_innerFields)

                        # 2-3 Word/Phrase Similarity
                        max_sim_score = max(inner_field_sim_scores)
                        max_score_count = inner_field_sim_scores.count(max_sim_score)
                        result = "innerClass Name:" + packageName + '.' + className + '$' + innerClassName + '\n' \
                                 + "innerField Name:" + str(match_innerFields) + '\n' + "Similarity Scores:" + \
                                 str(inner_field_sim_scores) + '\n' + "Max Score:" + str(max_sim_score) + '\n' + \
                                 "Max Score Count:" + str(max_score_count)
                        print(result)
                        with open(output_file, 'a+') as f:
                            f.write(result + '\n')

                if len(match_fields) or is_match_inner:
                    print("=======================")
                    with open(output_file, 'a+') as f:
                        f.write("=======================" + '\n')
                break


if __name__ == '__main__':
    main()
