__author__ = 'Liuyin'

import nltk
from lxml import html
from lxml import etree
from nltk.corpus import stopwords

PUNCTUATION =[';', ':', ',', '.', '!', '?', '>', '<']
GENERAL_STOPWORDS_LIST = stopwords.words("english") + PUNCTUATION

class RawArticle:
    def __init__(self, title, content, topic=""):
        self.title = title
        self.content = content
        self.topic = topic

class SgmFile:
    articles = []

    def __init__(self, filename):
        def hasTopic(node):
            return node.get('topics').lower() == "yes" and node.find('topics').find('d') != None
        def hasContent(node):
            return node.find('text').find('content') != None
        def hasTitle(node):
            return node.find('text').find('title') != None

        root = html.parse(filename).getroot()

        # the first article is warpped into a 'body' tag
        # so that we need to process it first
        reuters = root.find('body').getchildren()[0]
        title = ""
        content = ""
        if hasTitle(reuters):
            title = reuters.find('text').find('title').text
        # else:
            # print "no title, line#:", reuters.sourceline
        if hasContent(reuters):
            content = reuters.find('text').find('content').text
        # else:
            # print title
        ra0 = RawArticle(title, content) # raw article 0
        # print "topic :", reuters.get('topics')
        if reuters.get('topics').lower() == "yes":
            topic = reuters.find('topics').find('d').text
            ra0.topic = topic
        self.articles.append(ra0)

        ras = root.getchildren() # raw articles
        # print "ras type: ", type(ras), "; len=", len(ras)
        for reuter in ras:
            # print "type reuter: ", type(reuter), "; tag=", reuter.tag
            if reuter.tag == 'body':
                continue
            title = ""
            content = ""
            if hasTitle(reuter):
                title = reuter.find('text').find('title').text
            # else:
            #     print "no title, line#:", reuter.sourceline
            if hasContent(reuter):
                content = reuter.find('text').find('content').text
            # else:
            #     print title
            ra = RawArticle(title, content)
            if hasTopic(reuter):
                topic = reuter.find('topics').find('d').text
                ra.topic = topic
            self.articles.append(ra)

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


article_reader()
print simplelist[1].title
print simplelist[1].title_keywords()

