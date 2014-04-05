import glob
import json
from gensim.models.ldamodel import LdaModel


class TopicModelHelpers:
    def __init__(self, fnames):
        """`fnames` is an array of files for [lda_model, distribution]"""
        print "Accumulating tweets..."
        self.tweets = map(lambda f: open(f).read(), glob.glob("../tweets/*"))

        print "Loding topic model..."
        self.lda = LdaModel.load(fnames[0])

        # self.corpus = json.load("")

        print "Loading tweet distribution..."
        self.tweet_dist = json.load(open(fnames[1]))

    def get_tweets_in_topic(self, topic_id):
        tweet_ids = []
        for i, topic_dist in enumerate(self.tweet_dist):
            for topic, per in topic_dist:
                if topic == topic_id and per >= 0.20:
                    tweet_ids.append((i, per))

        res = map(lambda (i, per): str(per)+" => "+self.tweets[i], tweet_ids)
        return res
