import nltk
from lxml import html
from lxml import etree

# root = html.parse('../reuters/reut2-000.sgmCopy').getroot() # root = [html]
# print "topics 1: ", root.find('body').find('reuters').find('topics').find('d').text
# print "title 1: ", root.find('body').find('reuters').find('text').find('title').text
# print "content 1: ", root.find('body').find('reuters').find('text').find('content').text

# each a is node 'reuters'
# c = root.find('body').getchildren()[0]
# print type(c), len(c), c[0].keys()
# print etree.tostring(root, pretty_print=True)

class RawArticle:
    def __init__(self, title, content, topic):
        self.title = title
        self.content = content
        self.topic = topic


class SgmFile:
    def __init__(self, filename):
        self.articles = []
        def hasTopic(node):
            return node.get('topics').lower() == "yes" and node.find('topics').find('d') != None
        def hasContent(node):
            return node.find('text').find('content') != None
        def hasTitle(node):
            return node.find('text').find('title') != None

        root = html.parse(filename).getroot()

        # print etree.tostring(root, pretty_print=True)

        # the first article is warpped into a 'body' tag
        # so that we need to process it first
        # reuters = root.find('body').getchildren()[0]
        # title = ""
        # content = ""
        # if hasTitle(reuters):
        # 	title = reuters.find('text').find('title').text
        # # else:
        # # 	print "no title, line#:", reuters.sourceline
        # if hasContent(reuters):
        # 	content = reuters.find('text').find('content').text
        # # else:
        # # 	print title
        # ra0 = RawArticle(title, content) # raw article 0
        # # print "topic :", reuters.get('topics')
        # if reuters.get('topics').lower() == "yes":
        # 	topic = reuters.find('topics').find('d').text
        # 	ra0.topic = topic
        # self.articles.append(ra0)

        ras = root.find('body').getchildren() # raw articles
        # print "ras type: ", type(ras), "; len=", len(ras)
        for reuter in ras:
            # print "type reuter: ", type(reuter), "; tag=", reuter.tag
            # if reuter.tag == 'body':
            # 	# the first article is warpped into a 'body' tag
            # 	# so that we need to get its child
            # 	reuter = reuter.getchildren()[0]
            title = ""
            content = ""
            topic = ""
            if hasTitle(reuter):
                title = reuter.find('text').find('title').text
            # else:
            # 	print "no title, line#:", reuter.sourceline
            if hasContent(reuter):
                content = reuter.find('text').find('content').text
            # else:
            # 	print title
            if hasTopic(reuter):
                # this is for the case that only has one topic word
                # topic = reuter.find('topics').find('d').text
                # ra.topic = topic
                # in many cases, there are many words
                for t in reuter.find('topics').itertext():
                    topic = topic + " " + t
                # allTopic = reuter.find('topics').findall('d')
                # print "type allTopic: ", type(allTopic)
            ra = RawArticle(title, content, topic)
            self.articles.append(ra)


# this piece of code shows how to use the above SgmFile class
# sf = SgmFile('../reuters/reut2-000.sgmCopy')
# print "len(sf)=", len(sf.articles)
# print "sf title: ", sf.articles[0].title
# print "sf topic: ", sf.articles[0].topic
# print "sf content: ", sf.articles[0].content

# TODO: article with no title, that has <TEXT TYPE="UNPROC">,
#       which we could do: find('text').text
# TODO: article with no topic, that has <TEXT TYPE="BRIEF">,
#       which we may consider whether use title as content or not
