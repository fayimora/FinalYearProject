## Description
This repository contains every line of code I wrote for my BSc project.

`NBClassifier.py` can be used to train a NaiveBayes classifier.
`TopicModelling.py` is used to detect themes in the dataset using gensim.
`topic_model_helpery.py` contains a few helper functions for analysing topic models
`utils/` contains utility scripts used during the project



## Usage
To train a naive Bayes classifier, run `python NBClassifier.py`. It requires that the training set be in folders `data/relevant` and `data/irrelevant`.

For the topic model, run `python TopicModelling`. It trains topics using LDA and saves the model to a file. The dataset
should be in a directory called tweets.

The `models/` directory contains the models used in this study. To use them, 
open a python console(preferably [IPython](http://ipython.org/)) and load the `topic_model_helpers.py` script. An example 
run would be:

````python
tmh = TopicModelHelpers(["models/lda_unigrams_30.dat"]) # load the 30 topics model
tmh.topics # returns a list of topics and their token distribution
tmh.get_tweets_in_topic(28) # show tweets with a proportion of topic 28
tmh.filter_tweets("android", 19) # show tweets that have a proportion of topic 19 and have token android in them
````


`data_3600.zip` contains sample data that can be used in the above models.
