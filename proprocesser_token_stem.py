__author__ = 'Liuyin'

### TO TOKEN, STEM AND REMOVE GENERAL STOPWORDS ###
import nltk
from nltk.corpus import stopwords

PUNCTUATION =[';', ':', ',', '.', '!', '?', '>', '<', '"', ']', '[', '-', '(', ')', "''", '``']
GENERAL_STOPWORDS_LIST = stopwords.words("english") + PUNCTUATION

def preprocess(paragraph): # Tokenize, stem, remover general stop words
    from nltk import stem

    tokenized_paragraph = nltk.tokenize.word_tokenize(paragraph)
    # tokenized_paragraph = nltk.word_tokenize(paragraph)

    ##############
    # another way of tokenize
    ##############
    # stop_symbols = "!@#$%^&*()_+=-?></.,';\":][}{\r\n\t~`"
    # tokenized_paragraph = paragraph
    # for s in stop_symbols:
    #     tokenized_paragraph = tokenized_paragraph.replace(s, '')
    # tokenized_paragraph = tokenized_paragraph.lower()
    # tokenized_paragraph = tokenized_paragraph.split()

    stemmed_paragraph =[]
    stemmer = stem.snowball.EnglishStemmer()
    for word in tokenized_paragraph:
        stemmed_paragraph.append(stemmer.stem(word))
        # we don't want to merge repeated words, so that we could not use set
    # preprocessed_paragragh = list(set(stemmed_paragraph) - set(GENERAL_STOPWORDS_LIST))
    preprocessed_paragragh = [x for x in stemmed_paragraph if x not in GENERAL_STOPWORDS_LIST]
    return preprocessed_paragragh
