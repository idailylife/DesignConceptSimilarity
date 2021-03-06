#coding:utf-8
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import re
import string
import math

from ExcelFileFeed import ExcelFileIn
from TfIdfSimilarity import *
import Constants



def generate_word_list(sentence, remove_stopword=True):
    pattern = r'<a.*>.*</a>'
    sentence = re.sub(pattern, "", sentence)
    pattern = r'((http|ftp|https):\/\/)?[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    sentence = re.sub(pattern, "", sentence)
    #sentence.translate({key: None for key in string.punctuation})
    sentence = re.sub('[' + string.punctuation + ']', '', sentence)
    sentence = ''.join([c for c in sentence if ord(c) < 128])
    sentence_list = sentence.lower().split()
    if remove_stopword:
        sentence_list = [word for word in sentence_list if word not in stopwords.words('english')]
    return sentence_list

word_sim_buffer = {}


def get_word_similarity(w1, w2, type='path'):
    '''
    Get maximum similarity between w1 and w2
    :param w1:
    :param w2:
    :param type:
    :return:
    '''
    if type not in ['path', 'lch', 'wup', 'res', 'jcn', 'lin']:
        raise Exception('WordNet similarity type not supported.')
    max_similarity = 0
    if word_sim_buffer.has_key((w1, w2)):
        return word_sim_buffer[(w1, w2)]
    elif word_sim_buffer.has_key((w2, w1)):
        return word_sim_buffer[(w2, w1)]

    for w1_synset in wn.synsets(w1):
        for w2_synset in wn.synsets(w2):
            if type=='path':
                simi = w1_synset.path_similarity(w2_synset)
            elif type=='lch':
                simi = w1_synset.lch_similariity(w2_synset)
            elif type=='wup':
                simi = w1_synset.wup_similarity(w2_synset)
            elif type=='res':
                simi = w1_synset.res_similarity(w2_synset)
            elif type=='jcn':
                simi = w1_synset.jcn_similarity(w2_synset)
            elif type=='lin':
                simi = w1_synset.lin_similarity(w2_synset)
            if simi > max_similarity:
                max_similarity = simi
    word_sim_buffer[(w1, w2)] = max_similarity
    return max_similarity


def get_word_sentence_similarity(word, sentence, type='path', tf_idf_diction_tuple=None):
    '''
    simi(word|sentence) = \sum{instance in sentence}(simi(word, instance))/||sentence||
    :param word:
    :param sentence: list of words
    :param type:
    :param tf_idf_diction_tuple: (tf_idf_dictionary_of_sentence_1, tf_idf_dictionary_of_sentence_2)
    :return:
    '''
    if len(sentence) == 0:
        return Constants.VAL_SIMILARITY_NA
    sum = 0.0

    for instance in sentence:
        if tf_idf_diction_tuple is None:
            sum += get_word_similarity(word, instance, type)
        else:
            if tf_idf_diction_tuple[1].has_key(instance):
                instance_tf_idf = tf_idf_diction_tuple[1][instance]
            else:
                instance_tf_idf = Constants.TF_IDF_WEIGHT_DEFAULT
            sum += instance_tf_idf * get_word_similarity(word, instance, type)

    if tf_idf_diction_tuple is not None:
        if tf_idf_diction_tuple[0].has_key(word):
            word_tf_idf = tf_idf_diction_tuple[0][word]
        else:
            word_tf_idf = Constants.TF_IDF_WEIGHT_DEFAULT
        sum *= word_tf_idf

    sum /= float(len(sentence))
    return sum


def get_sentence_log_similarity(s1, s2, type='path', tf_idf_helper=None):
    '''
    Log similarity between two sentences
    log simi(s1|s2) = (\sum{instance in s1}(log simi(instance|s2))/||s1||
    :param s1: list of words
    :param s2: list of words
    :param type:
    :param tf_idf_helper: If taken tf-idf into account, push an instance of TfIdfHelper in.
    :return:
    '''
    if len(s1) == 0:
        return Constants.VAL_SIMILARITY_NA
    sum = 0.0
    if tf_idf_helper is not None:
        s2_tfidf_dict = tf_idf_helper.get_non_zero_tfidf(' '.join(s2))

    for instance in s1:
        if tf_idf_helper is None:
            sim = get_word_sentence_similarity(instance, s2, type)
        else:
            s1_tfidf_dict = tf_idf_helper.get_non_zero_tfidf(' '.join(s1))
            sim = get_word_sentence_similarity(instance, s2, type, (s1_tfidf_dict,s2_tfidf_dict))
        if sim < 1e-20:
            continue
        sum += math.log(sim)
    sum /= float(len(s1))
    return sum


if __name__ == '__main__':
    #print get_word_similarity('dog', 'cat')
    #print get_word_similarity('belt', 'strip')

    filein = Constants.EXCEL_INPUT_FILE
    xlsFile = ExcelFileIn(filein)
    lines = xlsFile.get_lines()
    tf_idf_helper = TfIdfHelper(pre_processing, document_lines=lines)

    lines = [generate_word_list(line) for line in lines]
    line_size = len(lines)
    results = []
    outfile = r'D:\output_with_tfidf.csv'
    outfile = open(outfile, 'w')
    for i in range(0, line_size):
        print "Line %d" % i
        results.append({})
        for j in range(0, line_size):
            results[i][j] = get_sentence_log_similarity(lines[i], lines[j], tf_idf_helper=tf_idf_helper)
            print "%f " % results[i][j],
            if not j == 0:
                outfile.write(",%f"%results[i][j])
            else:
                outfile.write("%f"%results[i][j])
            outfile.flush()
        print "\n"
        outfile.write("\n")
    outfile.close()
    print 'done'