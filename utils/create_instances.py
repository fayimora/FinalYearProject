from pymongo import *

print "Connecting to the database..."
client = MongoClient('146.185.155.128', 27017)
db = client.tweets
apple_tweets = db.apple_tweets

print "Fetching data from the database..."
labelled_data = apple_tweets.find({"relevant": {"$exists": True}}).limit(50)

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

