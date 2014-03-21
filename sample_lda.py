import glob, logging
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from gensim import corpora, models
from gensim.models.ldamodel import LdaModel

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


def to_features(vect, doc):
    vect.fit_transform([doc])
    return vect.get_feature_names()


documents = ['Human machine interface for lab abc computer applications',
             'A survey of user opinion of computer system response time',
             'The EPS user interface management system',
             'System and human system engineering testing of EPS',
             'Relation of user perceived response time to error measurement',
             'The generation of random binary unordered trees',
             'The intersection graph of paths in trees',
             'Graph minors IV Widths of trees and well quasi ordering',
             'Graph minors A survey']

files = glob.glob("data_3600/relevant/*")
documents = map(lambda f: open(f).read(), files)

stop_words = ENGLISH_STOP_WORDS.union(['iphone', 'ipod', 'ipad', 'http', 'rt', 'apple'])
vectorizer = CountVectorizer(min_df=1, ngram_range=(1, 1), stop_words=stop_words)
texts = [to_features(vectorizer, document) for document in documents]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=50, passes=10, iterations=1000, update_every=10)
corpus_lda = lda[corpus]
preds = [l for l in corpus_lda]