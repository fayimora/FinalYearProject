import logging, glob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from gensim import corpora, models
from gensim.models.ldamodel import LdaModel

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


def to_features(vect, doc):
    vect.fit_transform([doc])
    return vect.get_feature_names()

print "Accumulating data..."
files = glob.glob("data_3600/relevant/*")
documents = map(lambda f: open(f).read(), files)

print "Converting data to features..."
stop_words = ENGLISH_STOP_WORDS#.union(['iphone', 'ipod', 'ipad', 'http', 'https', 'rt', 'apple'])
vectorizer = CountVectorizer(min_df=1, ngram_range=(1, 1), stop_words=stop_words)
texts = [to_features(vectorizer, document) for document in documents]

print "Converting texts to bag of words..."
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

print "Creating LDA Model..."
lda = LdaModel(corpus, id2word=dictionary, num_topics=10, passes=10, iterations=1000, update_every=1)
corpus_lda = [l for l in lda[corpus]]