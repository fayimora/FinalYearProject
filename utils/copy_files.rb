require "FileUtils"
N = 10000
files = Dir.entries("tweets").take(N+3).drop(3)

files.each do |file|
  FileUtils.cp "tweets/#{file}", "#{N}_tweets/#{file}"
end
