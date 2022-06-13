from gensim.models import Word2Vec
import json
import numpy as np
import pandas as pd
with open('./分類系統/WordSegmentClassData.json') as f:
    traindata = json.loads(f.read())
alltext = [line[0] for line in traindata]
model = Word2Vec(alltext, vector_size=300, sg=0, window=10, workers=3, min_count=1)
doc = np.array([model.wv[alltext[i]].mean(axis=0) for i in range(len(alltext))])
data = pd.DataFrame(doc)
data['y'] = [line[1] for line in traindata]
data.to_csv('./分類系統/TrainData_W2V.csv', index=False)
model.save('./分類系統/W2V')
# data = pd.read_csv('./分類系統/TrainData_W2V.csv')
# print(data)