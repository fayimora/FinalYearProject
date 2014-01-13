import nltk
from nltk.classify import NaiveBayesClassifier
import glob

def get_data(path, label):
    examples = glob.glob(path)
    to_text = lambda fname: (features(open(fname).read()), label)
    return map(to_text, examples)

def features(sentence):
    words = sentence.lower().split()
    return dict((w, True) for w in words)

print "Extracting relevant and irrelevant examples..."
relevant_examples = get_data("data/relevant/*", "relevant")
irrelevant_examples = get_data("data/irrelevant/*", "irrelevant")

print "Creating training set..."
featuresets = relevant_examples + irrelevant_examples
print "Featuresets: " + str(len(featuresets))

N = 100000
train_set, test_set = featuresets[N:], featuresets[:N]
print "Train set: " + str(len(train_set))
print "Test set: " + str(len(test_set))

print "Training in progress..."
classifier = NaiveBayesClassifier.train(train_set)
print "Finished training!"

classifier.show_most_informative_features()
accuracy = nltk.classify.util.accuracy(classifier, test_set)
print "Accuracy: " + str(accuracy)
