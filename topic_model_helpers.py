import glob
import re
from gensim.models.ldamodel import LdaModel
from TopicModelling import get_params


class TopicModelHelpers:
    def __init__(self, fnames):
        """`fnames` is an array of files for [lda_model, distribution]"""
        print "Accumulating tweets..."
        files = glob.glob("data/relevant/*")
        self.tweets = map(lambda f: open(f).read(), files)

        print "Loding topic model..."
        self.lda = LdaModel.load(fnames[0])

        self.corpus, self.features, self.dictionary = get_params(files)

        print "Loading tweet distribution..."
        self.tweet_dist = [l for l in self.lda[self.corpus]]
        tmp = lambda dist: sorted(dist, key=lambda arr: arr[1], reverse=True)
        self.tweet_dist = map(lambda dist: tmp(dist), self.tweet_dist)
        # self.tweet_dist = json.load(open(fnames[1]))

        tmp = map(lambda t: re.sub("(\d*\.\d*\*)", "", t), self.lda.show_topics(-1))
        self.topics = map(lambda ts: re.sub("\\s\+", ",", ts), tmp)
        self.topics.reverse()

    def get_tweets_in_topic(self, topic_id, threshold=0.20):
        tweet_ids = []
        for i, topic_dist in enumerate(self.tweet_dist):
            for topic, per in topic_dist:
                if topic == topic_id and per >= threshold:
                    tweet_ids.append((i, per))
                    break

        res = map(lambda (i, per): (per, self.tweets[i]), tweet_ids)
        return res

    def filter_tweets(self, token, topic_id):
        """ This function takes a token and a topic_id. It returns the tweets
        that have a proportion of the argument topic and contains the argument token."""
        return filter(lambda s: token in s[1].lower(), self.get_tweets_in_topic(topic_id))
