import nltk, glob, random, argparse
from nltk.classify import NaiveBayesClassifier
from sklearn import cross_validation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.utils import shuffle

parser = argparse.ArgumentParser(description = "Naive Bayes Classifier")
parser.add_argument('--bigrams', action='store_true', default=False, help="Use BigramCollocationFinder for feature extaction")
args = parser.parse_args()

def get_data(path, label):
    examples = glob.glob(path)
    to_text = lambda fname: (features(open(fname).read()), label)
    return map(to_text, examples)

def features(sentence):
    vectorizer = CountVectorizer(min_df=1, ngram_range=(1,3), stop_words='english')
    X = vectorizer.fit_transform([ sentence ])
    return dict((featx, True) for featx in vectorizer.get_feature_names())

print "Extracting relevant and irrelevant examples..."
relevant_examples = get_data("data/relevant/*", "relevant")
irrelevant_examples = get_data("data/irrelevant/*", "irrelevant")

print "Creating training set..."
featuresets = relevant_examples + irrelevant_examples

print "Shuffling training set"
random.shuffle(featuresets)

print "Featuresets: " + str(len(featuresets))
print "\nBegin Cross validation"
cv = cross_validation.KFold(len(featuresets), n_folds=10, indices=True, shuffle=True,
        random_state=None, k=None)

accuracies = []
for traincv, testcv in cv:
    shuffle(featuresets)
    classifier = NaiveBayesClassifier.train(featuresets[traincv[0]:traincv[len(traincv)-1]])
    classifier.show_most_informative_features()
    accuracy = nltk.classify.util.accuracy(classifier, featuresets[testcv[0]:testcv[len(testcv)-1]])
    accuracies.append(accuracy)

print "Accuracies:", accuracies
print "Avg. Accuracy:", sum(accuracies)/len(accuracies)

