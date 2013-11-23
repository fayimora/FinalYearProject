twitter = require('ntwitter')
mongo  = require('mongodb')
user = process.env.MONGO_USER
password = process.env.MONGO_PASSWORD
dbHost = "127.0.0.1"
dbPort = mongo.Connection.DEFAULT_PORT
db     = new mongo.Db("tweets", new mongo.Server(dbHost, dbPort, {}))

auth = new twitter(
  consumer_key: '',
  consumer_secret: '',
  access_token_key: '',
  access_token_secret: ''
)
console.log "Done authenticating with Twitter!"

tweetsCollection = ""

db.open (err) ->
  db.collection "apple_tweets", (err, collection) ->
    console.log "Connected to #{dbHost}:#{dbPort}"
    tweetsCollection = collection

console.log "tweetsCollection is #{tweetsCollection}"

auth.stream 'statuses/filter',
  'track': ['apple', 'ipad', 'ipod', 'mac', 'imac', 'iphone'], (stream) ->
    stream.on "data", (data) ->
      if data.lang == "en"
        tweetsCollection.insert data, (error) ->
          console.log error if error
