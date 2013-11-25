
###
Module dependencies.
###
express = require("express")
http    = require("http")
path    = require("path")
mongo   = require('mongodb')
engine = require('ejs-locals')

app    = express()
# all environments
app.set "port", process.env.PORT or 3000
app.set "views", path.join(__dirname, "views")
app.engine('ejs', engine)
app.set "view engine", "ejs"
app.use express.favicon()
app.use express.logger("dev")
app.use express.json()
app.use express.urlencoded()
app.use express.methodOverride()
app.use app.router
app.use express.static(path.join(__dirname, "public"))

# development only
app.use express.errorHandler()  if "development" is app.get("env")

title = "Data Labeller"
app.get "/", (req, res) ->
  getTweets (tweets) ->
    res.render "list", {title: title, tweets: tweets}

app.post "/update", (req, res) ->
  updatedTweets = req.body
  updateTweets(updatedTweets)
  res.redirect "thanks"

app.get "/thanks", (req, res) ->
  console.log req
  res.render "thanks", {title: title}

dbHost = "127.0.0.1"
dbPort = mongo.Connection.DEFAULT_PORT
db     = new mongo.Db("tweets", new mongo.Server(dbHost, dbPort, {}))

tweetsCollection = undefined
tweetsCollectionName = "apple_tweets"

collectionCount = process.env.FYP_COLLECTION_COUNT
db.open (err) ->
  console.log("We are connected! " + dbHost + ":" + dbPort)

  db.collection tweetsCollectionName, (err, collection) ->
    tweetsCollection = collection

getTweets = (callback) ->
  # tweetsCollection.count( (err, count) -> num = count )
  tweetsCollection.find({relevant: {$exists: false}},{limit: 20, skip: getRandomInt(0, collectionCount) }, (error, cursor) ->
    cursor.toArray((error, tweets) ->
      callback(tweets);
    )
  )

updateTweets = (data) ->
  console.log tweetsCollection
  ObjectID = mongo.ObjectID
  for key, value of data
    relevance = if value == "relevant" then true else false
    tweetsCollection.update {_id: new ObjectID(key)}, {$set: {"relevant": relevance}}, false, true,
    (error, cursor) ->

getRandomInt =  (min, max) ->
  Math.floor(Math.random() * (max-min + 1)) + min

http.createServer(app).listen app.get("port"), ->
  console.log "Express server listening on port " + app.get("port")

