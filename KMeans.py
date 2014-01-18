import glob, os, re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn import metrics

def get_data(path):
    examples = glob.glob(path)
    to_text = lambda fname: (re.sub(r"data/(ir)?relevant/", "" ,fname), open(fname).read())
    return map(to_text, examples)

categories = None

print("Aggregating data")
data = get_data("data/relevant/*") + get_data("data/irrelevant/*")
dataset = map(lambda (fname, text): text, data)
ids = map(lambda (fname, text): fname, data)

vectorizer = TfidfVectorizer(max_df=0.5, max_features=10, stop_words='english', use_idf=True)
X = vectorizer.fit_transform(dataset)
print("n_samples: %d, n_features: %d" % X.shape)

K = 10
# kmeans = MiniBatchKMeans(n_clusters=K, init='k-means++', max_iter=200, n_init=5, verbose=True, n_jobs=-1)
kmeans = KMeans(n_clusters=K, init='k-means++', max_iter=200, n_init=1, verbose=True, n_jobs=-1)
print("Clustering data with %s" % kmeans)

kmeans.fit_predict(X)
print('Done fitting.')

if os.path.exists("output"):
  print('Backing up old output folder')
  os.system("mv -f output output-backup")

print('Writing result to output folder')
for id, label, tweet in zip(ids, kmeans.labels_, dataset):
  location = "output/%s/" % label
  if not os.path.exists(location):
    os.makedirs(location)
  output = location + id
  f = open(output, 'w')
  f.write(tweet)
  f.close()

print("Write complete.")
