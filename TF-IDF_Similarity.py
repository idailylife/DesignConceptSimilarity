#coding:utf-8
import re
import string
import nltk
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import *
from sklearn.feature_extraction.text import TfidfVectorizer

from ExcelFileFeed import ExcelFileIn

def pre_processing(sentence):
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