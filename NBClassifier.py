import glob, random
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import cross_validation
from sklearn.metrics import precision_recall_curve, auc
from sklearn.pipeline import Pipeline
import numpy as np

def get_data(path, label):
    key = {1: 'relevant', -1: 'irrelevant'}
    print "Generating %s's data and labels" % key[label]
    examples = glob.glob(path)
    to_pair = lambda fname: (open(fname).read(), label)
    examples = map(to_pair, examples)
    # random.shuffle(examples)

    tweets, labels = [],[]
    for t, l in examples:
        tweets.append(t)
        labels.append(l)
    return (tweets, labels)

print "Extracting relevant and irrelevant examples..."
relevant_examples, relevant_labels = get_data("data/relevant/*", 1)
irrelevant_examples, irrelevant_labels = get_data("data/irrelevant/*", -1)

print "Creating training set..."
train_data = np.asarray(relevant_examples + irrelevant_examples)
Y = np.asarray(relevant_labels + irrelevant_labels)
y_train = Y

vectorizer = CountVectorizer(min_df=1, ngram_range=(1,2), stop_words='english')
clf = Pipeline([('vect', vectorizer), ('clf', MultinomialNB())])

cv = cross_validation.ShuffleSplit(n=len(train_data), n_iter=10, test_size=0.20, indices=True,
        random_state=0)

scores, pr_scores = [], []
for train_idx, test_idx in cv:
    X_train, y_train = train_data[train_idx], Y[train_idx]
    X_test, y_test = train_data[test_idx], Y[test_idx]

    clf.fit(X_train, y_train)

    score = clf.score(X_test, y_test)
    scores.append(score)

    proba = clf.predict_proba(X_test)
    precision, recall, pr_thresholds = precision_recall_curve(y_test, proba[:,1])
    pr_scores.append(auc(recall, precision))
    summary = (np.mean(scores), np.std(scores), np.mean(pr_scores), np.std(pr_scores))
    print "%.4f\t%.4f\t%.4f\t%.4f" % summary


