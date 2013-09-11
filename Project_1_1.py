__author__ = 'Liuyin'

import nltk
from lxml import html
from lxml import etree
from nltk.corpus import stopwords
from lab1_sgm import *
from nltk import FreqDist

PUNCTUATION =[';', ':', ',', '.', '!', '?', '>', '<']
GENERAL_STOPWORDS_LIST = stopwords.words("english") + PUNCTUATION

def preprocess(paragraph): # Tokenize, stem, remover general stop words
    from nltk import stem
    tokenized_paragraph = nltk.word_tokenize(paragraph)
    stemmed_paragraph =[]
    stemmer = stem.snowball.EnglishStemmer()
    for word in tokenized_paragraph:
        stemmed_paragraph.append(stemmer.stem(word))
    # we don't want to merge repeated words, so that we could not use set
    # preprocessed_paragragh = list(set(stemmed_paragraph) - set(GENERAL_STOPWORDS_LIST))
    preprocessed_paragragh = [x for x in stemmed_paragraph if x not in GENERAL_STOPWORDS_LIST]
    return preprocessed_paragragh

class Article:
    def __init__(self,text_id,title,content):
        self.text_id = text_id
        self.title = title
        self.content = content
    def title_keywords(self):
        return set(preprocess(self.title))
    def content_freqDist(self):
        return count_words(self.content)

def article_reader(filename):
    articles_list = []
    sgm_extractor = SgmFile(filename)
    articles_amount = xrange(len(sgm_extractor.articles))
    articles_list=[Article(tid, sgm_extractor.articles[tid].title, sgm_extractor.articles[tid].content) for tid in articles_amount]
    return articles_list

def title_keyword_vector_generator(articles_list):
    title_keywords_vector={}
    articles_amount = xrange(len(articles_list))
    for aid in articles_amount:
        title_keywords_vector.update({articles_list[aid].text_id : articles_list[aid].title_keywords()})
    return title_keywords_vector

# get the frequency distribution of given string
def count_words(data):
    # tokens = nltk.tokenize.word_tokenize(data)
    tokens = preprocess(data)
    fdist = FreqDist(tokens) #input is a list of string
    # print "type fdist:", fdist
    # vocabulary = fdist.keys() 
    # print vocabulary[:50]
    # print "# York: ", fdist['york']
    # fdist.plot(100, title="hello", cumulative=False)
    # print fdist.tabulate()
    # FreqDist: http://nltk.googlecode.com/svn/trunk/doc/api/nltk.probability.FreqDist-class.html
    return fdist

def read_all_files():
    articles_list = []
    for i in xrange(22):
        filename = "./rawdata/reut2-" + str(i).zfill(3) + ".sgm"
        articles_list += article_reader(filename)
    return articles_list

# NOTE: we need to replace <body> and </body> tags in all *.sgm files
# articles_list = article_reader("./rawdata/reut2-000.sgm")
articles_list = read_all_files()
print "len articles_list:", len(articles_list)
title_keywords_vector = title_keyword_vector_generator(articles_list)
fdist_content = articles_list[0].content_freqDist()

# print len(articles_list)
print articles_list[0].title
# print articles_list[0].content
# print title_keywords_vector
print "# York: ", fdist_content['york']
print "top 10 Frequency:\n", fdist_content.tabulate(10)




