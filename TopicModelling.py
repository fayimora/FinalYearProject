import logging
import glob
import re
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from itertools import imap

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


def to_features(tweet):
    stop_words = ['iphone', 'ipod', 'ipad', 'mac', 'imac', 'rt', 'apple', 'amp']
    stop_words = ENGLISH_STOP_WORDS.union(stop_words)
    vectorizer = CountVectorizer(min_df=1, ngram_range=(1, 2), stop_words=stop_words)
    tweet = rm_usernames(rm_links(tweet))
    try:
        vectorizer.fit_transform([tweet])
        return vectorizer.get_feature_names()
    except ValueError:
        return ['']


def rm_usernames(tweet):
    return re.sub('@[a-zA-Z0-9]+ ?', '', tweet)


def rm_links(tweet):
    return re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?', '', tweet)


def prettify(topics):
    return map(lambda ts: re.sub("\\s\+", ",", ts), map(lambda t: re.sub("(\d*\.\d*\*)", "", t), topics))


def get_params(files):
    print "Converting data to features..."
    tweets = imap(lambda f: open(f).read(), files)
    features = [to_features(tweet) for tweet in tweets]
    # features = json.load(open("models/lda_features.json"))

    print "Converting features to bag of words..."
    dictionary = corpora.Dictionary(features)
    corpus = [dictionary.doc2bow(text) for text in features]
    # corpus = json.load(open("models/lda_corpus.json"))

    return corpus, features, dictionary


if __name__ == "__main__":
    print "Loading file names..."
    files = glob.glob("../tweets/*")
    corpus, features, dictionary = get_params(files)

    print "Creating LDA Model..."
    lda = LdaModel(corpus, id2word=dictionary, num_topics=30, iterations=1000, alpha='auto', chunksize=50)
    lda_topic_distribution = [l for l in lda[corpus]]

    print "Saving model..."
    lda.save("lda_model_unigrams.dat")

    print "Saving distribution..."
    f = open("lda_topic_distribution.json", 'w')
    json.dump(lda_topic_distribution, f)
    f.close()
