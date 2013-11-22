require 'mongo'

collection = Mongo::Connection.new("localhost", 27017).db("tweets")["apple_tweets"]

collection.find({}).each do |doc|
  File.open("tweets/#{doc["_id"]}.txt", "w") { |f| f.write(doc["text"]) }
end
