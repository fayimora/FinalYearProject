require 'mongo'

remoteCollection = Mongo::Connection.new("", 27017).db("tweets")["apple_tweets"]
localCollection = Mongo::Connection.new("localhost", 27017).db("tweets")["apple_tweets"]

remoteCollection.find({}, {limit: 500000}).each do |doc|
  localCollection.insert(doc)
end

