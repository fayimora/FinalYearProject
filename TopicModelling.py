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
    stop_words = ['iphone', 'ipod', 'ipad', 'mac', 'imac', 'http', 'https', 'rt', 'apple']
    stop_words = ENGLISH_STOP_WORDS.union(stop_words)
    vectorizer = CountVectorizer(min_df=1, ngram_range=(1, 2), stop_words=stop_words)
    tweet = rm_usernames(rm_links(tweet))
    try:
        vectorizer.fit_transform([tweet])
        return vectorizer.get_feature_names()
    except ValueError, e:
        return ['']


def rm_usernames(tweet):
    return re.sub('@[a-zA-Z0-9]+ ?', '', tweet)


def rm_links(tweet):
    return re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?', '', tweet)


def prettify(topics):
    return map(lambda ts: re.sub("\\s\+", ",", ts), map(lambda t: re.sub("(\d*\.\d*\*)", "", t), lda.show_topics(-1)))


def get_params(files):
    tweets = imap(lambda f: open(f).read(), files)

    print "Converting data to features..."
    features = [to_features(tweet) for tweet in tweets]

    print "Converting features to bag of words..."
    dictionary = corpora.Dictionary(features)
    corpus = [dictionary.doc2bow(text) for text in features]
    return corpus, features, dictionary


if __name__ == "__main__":
    print "Accumulating data..."
    files = glob.glob("../tweets/*")
    corpus, features, dictionary = get_params(files)

    print "Creating LDA Model..."
    lda = LdaModel(corpus, id2word=dictionary, num_topics=20, iterations=1000, alpha='auto')
    lda_corpus = [l for l in lda[corpus]]

    print "Saving model..."
    lda.save("lda_model_unigrams.dat")

    print "Saving distribution..."
    json.dump(lda_corpus, open("lda_corpus.json"))
