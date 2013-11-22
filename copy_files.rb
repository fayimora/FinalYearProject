require "FileUtils"
files = Dir.entries("tweets").take(5003).drop(3)

files.each do |file|
  FileUtils.cp "tweets/#{file}", "5000_tweets/#{file}"
end
