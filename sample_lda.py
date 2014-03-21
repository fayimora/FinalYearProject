import glob, logging
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

texts = [[word for word in document.lower().split()] for document in documents]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

lda = LdaModel(corpus, id2word=dictionary, num_topics=5, passes=5, iterations=100, update_every=1)
corpus_lda = lda[corpus]
preds = [l for l in corpus_lda]