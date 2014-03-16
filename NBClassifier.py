import glob, random, re
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import cross_validation
from sklearn.metrics import precision_recall_curve, auc, f1_score
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
import numpy as np
from matplotlib import pylab


def rm_links(s):
    return re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?', '', s)


def get_data(path, label):
    key = {1: 'relevant', -1: 'irrelevant'}
    print "Generating %s's data and labels" % key[label]
    examples = glob.glob(path)
    to_pair = lambda fname: (rm_links(open(fname).read()), label)
    examples = map(to_pair, examples)
    random.shuffle(examples)

    tweets, labels = [], []
    for t, l in examples:
        tweets.append(t)
        labels.append(l)
    return (tweets, labels)


def show_most_informative_features(vectorizer, clf, n=20):
    """Prints the n most informative features"""
    c_f = sorted(zip(clf.coef_[0], vectorizer.get_feature_names()))
    top = zip(c_f[:n], c_f[:-(n + 1):-1])
    for (c1, f1), (c2, f2) in top:
        print "\t[%.4f\t%-15s]\t\t[%.4f\t%-15s]" % (c1, f1, c2, f2)


def grid_search_model(clf_factory, X, Y):
    """Searches fo the best model given a comination of hyper parameters"""
    cv = cross_validation.ShuffleSplit(n=X.size, n_iter=10, test_size=0.20,
                                       indices=True, random_state=0)

    param_grid = dict(vect__ngram_range=[(1, 1), (2, 2), (1, 2), (1, 3)],
                      vect__min_df=[0, 0.5, 1, 1.5, 2],
                      vect__stop_words=[None, 'english'],
                      vect__norm=[None, 'l1', 'l2'],
                      vect__use_idf=[False, True],
                      vect__sublinear_tf=[False, True],
                      vect__binary=[False, True],
                      clf__alpha=[0, 0.01, 0.05, 0.1, 0.5, 1],
                      )

    grid_search = GridSearchCV(clf_factory, param_grid=param_grid, cv=cv,
                               score_func=f1_score, verbose=100, n_jobs=4)

    print "Searching for best model..."
    grid_search.fit(X, Y)
    clf = grid_search.best_estimator_

    print "Found best Estimator!"
    print clf
    return clf


def train_model(clf, X, Y):
    cv = cross_validation.ShuffleSplit(n=X.size, n_iter=10, test_size=0.20,
                                       indices=True, random_state=0)

    print clf
    print cv
    scores, pr_scores = [], []
    precisions, recalls, thresholds = [], [], []

    print "%4s\t%4s\t%4s\t%4s" % ("score", "std", "auc", "std")
    for train_idx, test_idx in cv:
        X_train, y_train = X[train_idx], y[train_idx]
        X_test, y_test = X[test_idx], y[test_idx]

        clf.fit(X_train, y_train)

        score = clf.score(X_test, y_test)
        scores.append(score)

        proba = clf.predict_proba(X_test)
        precision, recall, pr_thresholds = precision_recall_curve(y_test,
                                                                  proba[:, 1])

        precisions.append(precision)
        recalls.append(recall)
        thresholds.append(pr_thresholds)
        pr_scores.append(auc(recall, precision))

        summary = (np.mean(scores), np.std(scores), np.mean(pr_scores),
                   np.std(pr_scores))
        print "%.4f\t%.4f\t%.4f\t%.4f" % summary

    scores_to_sort = pr_scores
    median = np.argsort(scores_to_sort)[len(scores_to_sort) / 2]
    name = "NB Tweets Classifier"

    plot_pr(pr_scores[median], name, "04", precisions[median], recalls[median],
            label=name)


def get_best_classifier():
    classifier = MultinomialNB(alpha=0.01, class_prior=None, fit_prior=True)
    vectorizer = TfidfVectorizer(analyzer='word', binary=True, charset=None,
                                 charset_error=None, max_df=1.0, min_df=1,
                                 ngram_range=(2, 2), norm='l2',
                                 smooth_idf=True, stop_words=None,
                                 sublinear_tf=False, use_idf=False)

    clf = Pipeline([('vect', vectorizer), ('clf', classifier)])
    return clf


def plot_pr(auc_score, name, phase, precision, recall, label=None):
    """This function plots the ROC curve"""
    pylab.clf()
    pylab.figure(num=None, figsize=(10, 6))
    pylab.grid(True)
    pylab.fill_between(recall, precision, alpha=0.5)
    pylab.plot(recall, precision, lw=1)
    pylab.xlim([0.0, 1.0])
    pylab.ylim([0.0, 1.0])
    pylab.xlabel('Recall')
    pylab.ylabel('Precision')
    pylab.title('P/R curve (AUC=%0.2f) / %s' % (auc_score, label))
    filename = name.replace(" ", "_")
    # pylab.show()
    # pylab.savefig(os.path.join(".", "pr_%s_%s.png"%(filename, phase))
    pylab.savefig("pr_%s_%s.png" % (filename, phase))


if __name__ == '__main__':
    print "Extracting relevant and irrelevant examples..."
    relevant_examples, relevant_labels = get_data("data/relevant/*", 1)
    irrelevant_examples, irrelevant_labels = get_data("data/irrelevant/*", -1)

    print "Creating training set..."
    X = np.asarray(relevant_examples + irrelevant_examples)
    y = np.asarray(relevant_labels + irrelevant_labels)

    # vectorizer = CountVectorizer(min_df=1, ngram_range=(1, 2))
    # vectorizer = CountVectorizer(min_df=1, ngram_range=(1, 2),
    #                              stop_words='english')
    vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1, 2),
                                 stop_words='english')
    classifier = MultinomialNB()
    clf = Pipeline([('vect', vectorizer), ('clf', classifier)])

    # train_model(clf, X, y)
    train_model(get_best_classifier(), X, y)
    # best_clf = grid_search_model(clf, X, y)
