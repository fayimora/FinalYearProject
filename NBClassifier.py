from nltk.classifier import NaiveBayesClassifier
import glob

def get_data(path):
    examples = glob.glob(path)
    to_text = lambda fname: open(fname).read()
    return map(to_text, examples)

print "Extracting relevant and irrelevant examples..."
relevant_examples = get_data("data/relevant/*")
irrelevant_examples = get_data("data/relevant/*")

print "Creating training set..."
training_set = relevant_examples + irrelevant_examples

print "Training in progress..."
classifier = NaiveBayesClassifier.train(training_set)

