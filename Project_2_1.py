__author__ = 'Liuyin'


from proprocesser_token_stem import *
from lab1_sgm import *
from nltk import FreqDist

class Article:
    def __init__(self,text_id,title,content, topic):
        self.text_id = text_id
        self.title = title
        self.content = content
        if topic != "":
            self.topic = topic
        else:
            self.topic = "N/A"
    def title_keywords(self):
        return set(preprocess(self.title))
    def content_freqDist(self):
        return count_words(self.content)
def article_reader(filename, file_id):
    articles_list = []
    sgm_extractor = SgmFile(filename)
    prev_article_count = file_id * 1000
    articles_amount = xrange(len(sgm_extractor.articles))
    articles_list=[Article(tid + prev_article_count, sgm_extractor.articles[tid].title, sgm_extractor.articles[tid].content, sgm_extractor.articles[tid].topic) for tid in articles_amount]
    return articles_list

def title_keyword_vector_generator(articles_list):
    title_keywords_vector={}
    articles_amount = xrange(len(articles_list))
    for aid in articles_amount:
        title_keywords_vector.update({articles_list[aid].text_id : articles_list[aid].title_keywords()})
    return title_keywords_vector

def content_FreqDist_generator(articles_list):
    # get the FreqDist of all articles
    all_fdist = FreqDist()
    for article in articles_list:
        for item in article.content_freqDist().iteritems():
            key = item[0]
            value = item[1]
            all_fdist.inc(key, value)
    return all_fdist

def count_words(data):
    ### get the frequency distribution of given string ###

    # tokens = nltk.tokenize.word_tokenize(data)
    tokens = preprocess(data)
    # here we want to try to set the tokens
    # tokens = list(set(preprocess(data)))

    fdist = FreqDist(tokens) #input is a list of string
    # vocabulary = fdist.keys() 
    # print vocabulary[:50]
    # print fdist.tabulate()
    # FreqDist: http://nltk.googlecode.com/svn/trunk/doc/api/nltk.probability.FreqDist-class.html
    return fdist

def read_all_files():
    articles_list = []
    for i in xrange(22):
        filename = "./rawdata/reut2-" + str(i).zfill(3) + ".sgm"
        articles_list += article_reader(filename, i)
    return articles_list

def sample_content_keywords_generator(sample_list):
    # generate sample content keywords by the first .sgm file (1000 articles)
    sample_fdist = content_FreqDist_generator(sample_list)
    relative_word_list = []
    for word, word_fdist in sample_fdist.items():
        if word_fdist <=600 and word_fdist >= 100:
            relative_word_list.append(word)
    return relative_word_list

def content_keywords_generator(relative_word_list, articles_list):
    # generate all content keywords based on sample content keywords
    content_relative_word_vector = {}
    for article in articles_list:
        article_id = article.text_id
        article_relative_word_counter = []
        article_content = preprocess(article.content)
        for word in relative_word_list:
            word_counter = article_content.count(word)
            article_relative_word_counter.append(word_counter)
        content_relative_word_vector.update({article_id : article_relative_word_counter})
    return content_relative_word_vector

def generate_topics_list(articles_list):
    ### Generate topics list ###
    topic_list = set()
    for article in articles_list:
        topic_list.add(article.topic)
    topic_list = tuple(topic_list)
    return topic_list

def topic_category(articles_list):
    ### Classify articles based on their topics ###
    topic_articles_matrix = dict()
    for article in articles_list:
        if article.topic not in topic_articles_matrix.keys():
            value = []
            value.append(article)
            topic_articles_matrix.update({article.topic: value})
        else:
            contained_list = topic_articles_matrix[article.topic]
            contained_list.append(article)
            topic_articles_matrix[article.topic] = contained_list
    return topic_articles_matrix

def training_testing_list(topic_articles_dict):
    training_data_list = []
    testing_data_list = []
    split_para = 0.8
    for key in topic_articles_dict.keys():
        if key != 'N/A':
            topic_all_data_list = topic_articles_dict[key]
            topic_training_data_list = topic_all_data_list[0: int(len(topic_all_data_list) * split_para + 1)]
            topic_testing_data_list = topic_all_data_list[int(len(topic_all_data_list) * split_para + 1):]
            training_data_list.extend(topic_training_data_list)
            testing_data_list.extend(topic_testing_data_list)
    return (training_data_list, testing_data_list)


# NOTE: we need to replace <body> and </body> tags in all *.sgm files
articles_list = read_all_files()
print "len articles_list:", len(articles_list)
topic_articles_dict = topic_category(articles_list)
sample_list = training_testing_list(topic_articles_dict)[0]
print len(sample_list)
# print sample_list
content_FreqDist_generator(sample_list).plot(200)
#content_keywords_vector = content_keywords_generator(sample_content_keywords_generator(), articles_list)
#title_keywords_vector = title_keyword_vector_generator(articles_list)
# print title_keyword_vector_generator(articles_list[0:10])
# print sample_content_keywords_generator()
# print content_keywords_generator(sample_content_keywords_generator(), articles_list[0:1])


