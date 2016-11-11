#coding:utf-8
import re
import string
import nltk
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import *
from sklearn.feature_extraction.text import TfidfVectorizer

from ExcelFileFeed import ExcelFileIn


class TfIdfHelper:
    """
    Take a list of documents as the knowledge. When input some sentence, return the TfIdf value of each word.
    """
    def __init__(self, tokenizer, document_lines=None, document_file_path=None):
        if document_file_path is not None:
            xlsFile = ExcelFileIn(document_file_path)
            self.document_lines = xlsFile.get_lines()
        elif document_lines is not None:
            self.document_lines = document_lines
        else:
            raise Exception('Error: Should define either document path or document string list, provided none.')
        self.tokenizer = tokenizer
        self.tfidf = TfidfVectorizer(tokenizer=self.tokenizer, stop_words='english')
        self.tfidf.fit_transform(self.document_lines)


    def get_non_zero_tfidf(self, sentence):
        '''
        Input a sentence and return non-zero tf-idf values
        :param sentence:
        :return: dictionary, {term: val}
        '''
        _, stem_dict = stem_with_translation_dict(pre_processing(sentence, stem=False))
        response = self.tfidf.transform([sentence])
        feature_names = self.tfidf.get_feature_names()
        tfidf_dict = {}
        for col in response.nonzero()[1]:
            tfidf_dict[stem_dict[feature_names[col]]] = response[0, col]
        return tfidf_dict


def stem_with_translation_dict(tokens):
    stemmed = []
    stem_dict = {}
    stemmer = PorterStemmer()
    for item in tokens:
        stemmed.append(stemmer.stem(item))
        stem_dict[stemmed[-1]] = item
    return stemmed, stem_dict


def pre_processing(sentence, stem=True):
    pattern = r'<a.*>.*</a>'
    sentence = re.sub(pattern, "", sentence)
    pattern = r'((http|ftp|https):\/\/)?[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    sentence = re.sub(pattern, "", sentence)
    sentence = sentence.translate({key: None for key in string.punctuation}).lower()
    sentence = ''.join([c for c in sentence if ord(c) < 128])   # Remove non-ascii characters
    tokens = nltk.word_tokenize(sentence)

    # Stop Word Removal
    tokens = [word for word in tokens if not word in stopwords.words('english')]
    #tokens = Counter(tokens)
    if not stem:
        return tokens

    # Stem Tokens
    stemmed = []
    stemmer = PorterStemmer()
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

if __name__ == '__main__':
    filein = r'/Users/hebowei/OneDrive/众包平台/方案条目汇总.xlsx'
    xlsFile = ExcelFileIn(filein)
    lines = xlsFile.get_lines()

    tfidf = TfidfVectorizer(tokenizer=pre_processing, stop_words='english')
    tfidf.fit_transform(lines)
    str = 'this sentence has unseen text such as computer but also king lord juliet'
    response = tfidf.transform([str])
    feature_names = tfidf.get_feature_names()
    for col in response.nonzero()[1]:
        print feature_names[col], ' - ', response[0, col]