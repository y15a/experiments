#coding: utf-8

import json, time
import MeCab as mecab

from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans

def parser(text):
    tagger = mecab.Tagger()
    text = unicode(text)
    encoded_text = text.encode('utf-8')

    node = tagger.parseToNode(encoded_text)
    while node:
        yield node.surface
        node = node.next


words_dict = dict()


f = open('data.txt', 'r')
lines = '\n'.join(f.readlines())
obj = json.loads(lines)
texts = [o['text'] for o in obj]


hasher = HashingVectorizer(tokenizer=parser)
vectorizer = make_pipeline(hasher, TfidfTransformer())

X = vectorizer.fit_transform(texts)
svd = TruncatedSVD(10)
lsa = make_pipeline(svd, Normalizer(copy=False))

X = lsa.fit_transform(X)

true_k = 10

km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)

print("Clustering sparse data with %s" % km)
t0 = time.time()
km.fit(X)
print("done in %0.3fs" % (time.time() - t0))

print("Top terms per cluster:")
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i)
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind])
    print()


