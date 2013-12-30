from nltk.classifier import NaiveBayesClassifier

# extract relevant and irrelevant examples
relevant_examples = []
irrelevant_examples = []

training_set = relevant_examples + irrelevant_examples

classifier = NaiveBayesClassifier.train(training_set)

