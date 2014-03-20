from pymongo import *
import pickle, numpy, os, glob
from joblib import Parallel, delayed

def get_collection(db_name, coll):
    print "Connecting to the database..."
    client = MongoClient(os.environ['FYP_MONGO_HOST'], 27017)
    db = client[db_name]
    collection = db[coll]
    return collection


def create_train_instances():
    apple_tweets = get_collection('tweets', 'apple_tweets')
    print "Fetching data from the database..."
    labelled_data = apple_tweets.find({"relevant": {"$exists": True}})

    print "Now creating instances..."
    for tweet in labelled_data:
        loc = "data/"
        if(tweet['relevant']):
            loc = loc + "relevant/" + str(tweet['_id'])
        else:
            loc = loc + "irrelevant/" + str(tweet['_id'])

        f = open(loc, 'w')
        f.write(tweet['text'].encode("utf-8"))
        f.close()

    print "Done creating instances!"


def create_instances():
    apple_tweets = get_collection('tweets', 'apple_tweets')
    labelled_data = apple_tweets.find()

    clf = pickle.load(open('nb_tweets_classifier.dat', 'r'))

    print "Creating instances..."

    for tweet in labelled_data:
        loc = "tweets/%s.txt" % str(tweet['_id'])
        status = tweet['text'].encode("utf-8")
        pred = clf.predict([status])

        if pred == 1:
            f = open(loc, 'w')
            f.write(status)
            f.close()
            
    print "Finished creating instances!"


def try_open(path):
    try:
        f = open(path).read()
        f.flush()
        f.close()
    except(IOError):
        print path


if __name__ == '__main__':
    # create_instances()
    Parallel(n_jobs=-1)(delayed(try_open)(path) for path in glob.glob("../tweets/apple/*"))
