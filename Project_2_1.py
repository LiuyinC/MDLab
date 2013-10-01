__author__ = 'Liuyin'


from proprocesser_token_stem import *
from lab1_sgm import *
from nltk import FreqDist
import nltk
import key_word_list
import Topic_keywords_dict
from text.classifiers import NaiveBayesClassifier



class Article:
    def __init__(self,text_id,title,content, topic):
        self.text_id = text_id
        self.title = title
        self.content = content
        if topic != "":
            self.topic = nltk.word_tokenize(topic)
        else:
            topic_na = []
            topic_na.append('N/A')
            self.topic = topic_na
    def title_keywords(self):
        return set(preprocess(self.title))
    def content_freqDist(self):
        return count_words(self.content)
    def content_keywords(self):
        token_con = set(preprocess(self.content))
        content_keywords = []
        for word in token_con:
            if word in key_word_list.key_words():
                content_keywords.append(word)
        return list(content_keywords)
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
    tokens_set = set(tokens)
    # here we want to try to set the tokens
    # tokens = list(set(preprocess(data)))

    fdist = FreqDist(tokens_set) #input is a list of string
    # vocabulary = fdist.keys() 
    # print vocabulary[:50]
    # print fdist.tabulate()
    # FreqDist: http://nltk.googlecode.com/svn/trunk/doc/api/nltk.probability.FreqDist-class.html
    return fdist

def read_all_files():
    articles_list = []
    for i in xrange(1):
        filename = "./rawdata/reut2-" + str(i).zfill(3) + ".sgm"
        articles_list += article_reader(filename, i)
    return articles_list

def sample_content_keywords_generator(sample_list):
    ### generate sample content keywords from sample list ###
    sample_fdist = content_FreqDist_generator(sample_list)
    relative_word_list = []
    for word, word_fdist in sample_fdist.items():
        if word_fdist <=1000 and word_fdist >= 100:
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
        content_relative_word_vector.update({article_id: article_relative_word_counter})
    return content_relative_word_vector

def generate_topics_list(articles_list):
    ### Generate topics list ###
    topic_list = []
    for article in articles_list:
        topic_list.extend(article.topic)
    topic_list = set(topic_list)
    topic_list = tuple(topic_list)
    return topic_list

def topic_category(articles_list):
    ### Classify articles based on their topics ###
    topic_articles_matrix = dict()
    for article in articles_list:
        for topic in article.topic:
            if topic not in topic_articles_matrix.keys():
                value = []
                value.append(article)
                topic_articles_matrix.update({topic: value})
            else:
                contained_list = topic_articles_matrix[topic]
                contained_list.append(article)
                topic_articles_matrix[topic] = contained_list
    return topic_articles_matrix

def training_testing_list(topic_articles_dict):
    ### Split all articles with topic into two categories: training and testing ###
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

def training_dict(topic_articles_dict):
    training_dict = {}
    for key, value in topic_articles_dict.items():
        if key != 'N/A':
            value = value[0: int(len(value) * 0.8) + 1]
            training_dict.update({key: value})
    return training_dict

def testing_dict(topic_articles_dict):
    testing_dict = {}
    for key, value in topic_articles_dict.items():
        if key != 'N/A':
            value = value[ int(len(value) * 0.8) + 1:]
            testing_dict.update({key: value})
    return testing_dict

def training_topic_keywords_generate(topic_articles_dict):
    split_para = 0.8
    topic_keyword_dict = {}
    for key in topic_articles_dict.keys(): #Generate topic keywords#
        topic_keywords = []
        if key != 'N/A':
            for item in preprocess(key):   # Include topic into keywords list #
                topic_keywords.append(item)
            topic_all_data_list = topic_articles_dict[key]
            topic_training_data_list = topic_all_data_list[0: int(len(topic_all_data_list) * split_para + 1)] #split training data
            for article in topic_training_data_list:
                topic_keywords.extend(article.content_keywords())
            topic_keywords = set(topic_keywords)
            topic_keywords = list(topic_keywords)
            topic_keyword_dict.update({key: topic_keywords})
    return topic_keyword_dict



def predict_topic_DT (article, topic_keywords_dict, keyword_list):
    ### Predict Topic by Decision Tree ###
    content = preprocess(article.content)
    content_keywords = set(content) & set(keyword_list)
    tid = article.text_id
    pred_topic = []
    for key in topic_keywords_dict.keys():
        occurance = 0
        for keyword in list(content_keywords):
            if keyword in topic_keywords_dict[key]:
                occurance += 1
        if len(content_keywords) != 0:
            if (occurance / len(content_keywords)) >= 0.8:
                pred_topic.append(key)
    return (tid, pred_topic)

def calculate_accuracy_DT(testing_list):
    cumu_acc = 0
    for article in testing_list:
        predicted_topics = predict_topic_DT(article, Topic_keywords_dict.topic_keywords_dict(), key_word_list.key_words())[1]
        if set(predicted_topics) >= set(article.topic):
            item_acc = 1
            if len(set(predicted_topics) - set(article.topic)) >= 2:
                item_acc = 0.5
        else:
            item_acc = 0
        cumu_acc += item_acc
    return (cumu_acc / len(testing_list))

def contradiction_list(article_list):
    contra_list = []
    for article in article_list:
        cont_kw = article.content_keywords()
        if article.topic == ['N/A']:
            if cont_kw != []:
                item = (cont_kw, 'N/A')
                contra_list.append(item)
    return contra_list

def classifier_NB(training_dict, contro_list):
    classifier_list = {}
    for topic in training_dict.keys():
        train_topic = []
        train_topic.extend(contro_list)
        for article in training_dict[topic]:
            cont_kw = article.content_keywords()
            if cont_kw != []:
                item = (cont_kw, topic)
                train_topic.append(item)
        if train_topic != []:
            topic_cl = NaiveBayesClassifier(train_topic)
            classifier_list.update({topic: topic_cl})
    return classifier_list  # return (key, value) = (topic, topic classifier)

def predict_topic_NB(article, classifier_list):
    text_cont = article.content_keywords()
    predicted_topics = []
    if text_cont != []:
        for topic in classifier_list.keys():
            if classifier_list[topic].classify(text_cont) == topic:
                predicted_topics.append(topic)
    return predicted_topics


# NOTE: we need to replace <body> and </body> tags in all *.sgm files
articles_list = read_all_files()
print "len articles_list:", len(articles_list)


topic_articles_dict = topic_category(articles_list)
#training_list = training_testing_list(topic_articles_dict)[0]
testing_list = training_testing_list(topic_articles_dict)[1]
contro_list = contradiction_list(articles_list[0:50])

test_dict = testing_dict(topic_articles_dict)
#classifiers = classifier_NB(test_dict,contro_list)
#for article in testing_list:
#    print "predicted topics:", predict_topic_NB(article,classifiers)
#    print "real topics", article.topic






#

# print calculate_accuracy_DT(testing_list)
#print predict_topic(testing_list[0], Topic_keywords_dict.topic_keywords_dict(), key_word_list.key_words())


#for article in testing_list:
 #  print 'predicted topic', predict_topic_DT(article, Topic_keywords_dict.topic_keywords_dict(), key_word_list.key_words())
  # print 'real topic', article.topic
# print sample_list
#content_FreqDist_generator(set(sample_list)).plot(200)
#print articles_list[942].topic, type(articles_list[1].topic)

#### Print topic keyword dictionary by fuctions###
#topic_keyword_dict = training_topic_keywords_generate(topic_articles_dict,key_word_list.key_words())
#print topic_keyword_dict


#print predict_topic(testing_list[0],topic_keyword_dict)
#print testing_list[0].topic

#### print topic keywords by sample articles list #####
#print sample_content_keywords_generator(sample_list)


# content_FreqDist_generator(sample_list).plot()


#content_keywords_vector = content_keywords_generator(sample_content_keywords_generator(), articles_list)
#title_keywords_vector = title_keyword_vector_generator(articles_list)
# print title_keyword_vector_generator(articles_list[0:10])
# print sample_content_keywords_generator()
# print content_keywords_generator(sample_content_keywords_generator(), articles_list[0:1])


