import nltk, glob, random, argparse
from nltk.classify import NaiveBayesClassifier
from sklearn import cross_validation
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures as BAM
from itertools import chain

parser = argparse.ArgumentParser(description = "Naive Bayes Classifier")
parser.add_argument('--bigrams', action='store_true', default=False, help="Use BigramCollocationFinder for feature extaction")
args = parser.parse_args()

def get_data(path, label):
    examples = glob.glob(path)
    to_text = lambda fname: (features(open(fname).read()), label)
    return map(to_text, examples)

def features(sentence):
    words = sentence.lower().split()
    if not args.bigrams:
        return dict((w, True) for w in words)
    else:
        bigram_finder = BigramCollocationFinder.from_words(words)
        bigrams = bigram_finder.nbest(BAM.chi_sq, 200)
        return dict((bg, True) for bg in chain(words, bigrams))

print "Extracting relevant and irrelevant examples..."
relevant_examples = get_data("data/relevant/*", "relevant")
irrelevant_examples = get_data("data/irrelevant/*", "irrelevant")

print "Creating training set..."
featuresets = relevant_examples + irrelevant_examples

print "Shuffling training set"
random.shuffle(featuresets)

print "Featuresets: " + str(len(featuresets))

# N = int(len(featuresets) * 0.85)
# train_set, test_set = featuresets[:N], featuresets[N:]

# print "Train set: " + str(len(train_set))
# print "Test set: " + str(len(test_set))

# print "Training in progress..."
# classifier = NaiveBayesClassifier.train(train_set)
# print "Finished training!"

# classifier.show_most_informative_features(20)
# accuracy = nltk.classify.util.accuracy(classifier, test_set)
# print "Accuracy: " + str(accuracy)

print "\nBegin Cross validation"
cv = cross_validation.KFold(len(featuresets), n_folds=10, indices=True, shuffle=True,
        random_state=None, k=None)

accuracies = []
for traincv, testcv in cv:
    classifier = NaiveBayesClassifier.train(featuresets[traincv[0]:traincv[len(traincv)-1]])
    accuracy = nltk.classify.util.accuracy(classifier, featuresets[testcv[0]:testcv[len(testcv)-1]])
    accuracies.append(accuracy)

print "Accuracies:", accuracies
print "Avg. Accuracy:", sum(accuracies)/len(accuracies)

