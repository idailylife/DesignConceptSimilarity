#coding:utf-8
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import re
import string


def generate_word_list(sentence, remove_stopword=True):
    pattern = r'<a.*>.*</a>'
    sentence = re.sub(pattern, "", sentence)
    pattern = r'((http|ftp|https):\/\/)?[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    sentence = re.sub(pattern, "", sentence)
    sentence = sentence.translate(string.maketrans("",""), string.punctuation)
    sentence_list = sentence.lower().split()
    if remove_stopword:
        sentence_list = [word for word in sentence_list if word not in stopwords.words('english')]
    return sentence_list


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
    return max_similarity



if __name__ == '__main__':
    print get_word_similarity('dog', 'cat')
    print get_word_similarity('belt', 'strip')
    print 'done'