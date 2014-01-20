import glob, os, re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn import metrics

def get_data(path):
    examples = glob.glob(path)
    to_text = lambda fname: (re.sub(r"data/(ir)?relevant/", "" ,fname), open(fname).read())
    return map(to_text, examples)

def plot(kmeans, dataset):
    kmeans.fit(dataset)
    h = 0.1
    x_min, x_max = dataset[:, 0].min() + 1, dataset[:, 0].max() - 1
    y_min, y_max = dataset[:, 1].min() + 1, dataset[:, 1].max() - 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    pl.figure(1)
    pl.clf()

    pl.plot(dataset[:, 0], dataset[:, 1], 'k.', markersize=2)
    # Plot the centroids as a white X
    centroids = kmeans.cluster_centers_
    pl.scatter(centroids[:, 0], centroids[:, 1], marker='x', s=20, linewidths=3, color='r', zorder=10)
    pl.title('K-means clustering on tweets')
    pl.xlim(x_min, x_max)
    pl.ylim(y_min, y_max)
    pl.xticks(())
    pl.yticks(())
    pl.show()

categories = None

print("Aggregating data")
data = get_data("data/relevant/*") + get_data("data/irrelevant/*")
dataset = map(lambda (fname, text): text, data)
ids = map(lambda (fname, text): fname, data)

vectorizer = TfidfVectorizer(max_df=0.5, max_features=10, stop_words='english', use_idf=True)
X = vectorizer.fit_transform(dataset)
print("n_samples: %d, n_features: %d" % X.shape)

K = 50
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
