# from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer
from gensim import corpora, models
from gensim.models import ldamodel


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


# texts = [[word for word in document.lower().split() if word not in
#           ENGLISH_STOP_WORDS] for document in documents]

vectorizer = CountVectorizer(min_df=1, ngram_range=(1, 2))
texts = [to_features(vectorizer, document) for document in documents]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

lda = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=10)
corpus_lda = lda[corpus]