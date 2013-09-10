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
    articles_list = []
    sgm_extractor = SgmFile("./rawdata/reut2-000.sgm")
    # print len(sgm_extractor.articles)
    articles_amount = xrange(len(sgm_extractor.articles))
    articles_list=[Article(tid, sgm_extractor.articles[tid].title, sgm_extractor.articles[tid].content) for tid in articles_amount]
    # for i in xrange(len(sgm_extractor.articles)):
    #     print simplelist[i].title
    return articles_list

def title_keyword_vector_generator(articles_list):
    title_keywords_vector={}
    articles_amount = xrange(len(articles_list))
    for aid in articles_amount:
        title_keywords_vector.update({articles_list[aid].text_id : articles_list[aid].title_keywords()})
    return title_keywords_vector

articles_list = article_reader()
title_keywords_vector = title_keyword_vector_generator(articles_list)

# print len(articles_list)
print articles_list[1].title
print title_keywords_vector
