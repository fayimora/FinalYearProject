import glob
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def get_data(path, label):
    print "Generating %s data and labels" % label
    examples = glob.glob(path)
    to_text = lambda fname: open(fname).read()
    examples = map(to_text, examples)
    labels = [label for t in examples]
    return (examples, labels)

print "Extracting relevant and irrelevant examples..."
relevant_examples, relevant_labels = get_data("data/relevant/*", "relevant")
irrelevant_examples, irrelevant_labels = get_data("data/irrelevant/*", "irrelevant")

print "Creating training set..."
train_data = relevant_examples + irrelevant_examples
y_train = np.array(relevant_labels + irrelevant_labels)
Y = np.array(relevant_labels + irrelevant_labels)

vectorizer = CountVectorizer(min_df=1, ngram_range=(1,3), stop_words='english')
print "Generating features with", vectorizer
X_train = vectorizer.fit_transform(train_data)
print "X_train: n_samples: %d, n_features: %d" % X_train.shape
print "y_train: n_samples: %d" % y_train.shape

X_test = vectorizer.transform(train_data[1500:2100])
y_test = y_train[1500:2100]
print "X_test: n_samples: %d, n_features: %d" % X_test.shape
print "y_test: n_samples: %d" % y_test.shape

clf = MultinomialNB()
clf.fit(X_train, y_train)

# from sklearn.metrics import f1_score
# pred = clf.predict(X_test)
# score = f1_score(y_test, pred)
# print("f1-score:   %0.3f" % score)

accuracy = clf.score(X_test, y_test)
print "Accuracy:", accuracy
print()

