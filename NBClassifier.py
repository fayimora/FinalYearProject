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
relevant_examples = get_data("data/relevant/*", "relevant")[:1500]
irrelevant_examples = get_data("data/irrelevant/*", "irrelevant")[:1500]

print "Creating training set..."
training_set = relevant_examples + irrelevant_examples

print "Training in progress..."
classifier = NaiveBayesClassifier.train(training_set)
print "Finished training!"

classifier.show_most_informative_features()

