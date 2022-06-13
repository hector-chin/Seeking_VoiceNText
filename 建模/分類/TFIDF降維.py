import pickle
import json
from sklearn.decomposition import PCA
import pandas as pd
tfidf = pickle.load(open("./分類系統/x_result.pkl", "rb"))
final = tfidf.toarray()
pca = PCA(n_components=300)
pca.fit(final)
final = pca.transform(final)
with open('./分類系統/pca.pkl', 'wb') as pickle_file:
    pickle.dump(pca, pickle_file)
data = pd.DataFrame(final)
with open('./分類系統/WordSegmentClassData.json') as f:
    traindata = json.loads(f.read())
y = [line[1] for line in traindata]
data['y'] = y
data.to_csv('./分類系統/TrainData_TFIDF.csv', index=False)
