__author__ = 'Liuyin'

import nltk
from lxml import html
from lxml import etree
from nltk.corpus import stopwords
from lab1_sgm import *

PUNCTUATION =[';', ':', ',', '.', '!', '?', '>', '<']
GENERAL_STOPWORDS_LIST = stopwords.words("english") + PUNCTUATION

def preprocess(paragraph): # Tokenize, stem, remover general stop words
    from nltk import stem
    tokenized_paragraph = nltk.word_tokenize(paragraph)
    stemmed_paragraph =[]
    stemmer = stem.snowball.EnglishStemmer()
    for word in tokenized_paragraph:
        stemmed_paragraph.append(stemmer.stem(word))
    preprocessed_paragragh = list(set(stemmed_paragraph) - set(GENERAL_STOPWORDS_LIST))
    return preprocessed_paragragh

class Article:
    def __init__(self,text_id,title,body):
        self.text_id = text_id
        self.title = title
        self.body = body
    def title_keywords(self):
        return preprocess(self.title)

def article_reader():
    global simplelist
    sgm_extractor = SgmFile("./rawdata/reut2-000.sgmCopy")
    simplelist=[Article(tid, sgm_extractor.articles[tid].title, sgm_extractor.articles[tid].content) for tid in xrange(len( sgm_extractor.articles))]
    # for i in xrange(len(sgm_extractor.articles)):
    #     print simplelist[i].title

def key_word_vector():
    pass

article_reader()
print simplelist[1].title
print simplelist[1].title_keywords()

