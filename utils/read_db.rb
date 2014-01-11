require 'mongo'

remoteCollection = Mongo::Connection.new("146.185.155.128", 27017).db("tweets")["apple_tweets"]
localCollection = Mongo::Connection.new("localhost", 27017).db("tweets")["apple_tweets"]

localCollection.find().each do |doc|
  remoteCollection.insert(doc)
end

# remoteCollection.find({}, {limit: 500000}).each do |doc|
#   localCollection.insert(doc)
# end
# 
