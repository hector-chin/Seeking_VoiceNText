import json
import numpy as np

with open('./專題資料/YoutubeWordSegment.json') as f:
    youdata = json.loads(f.read())

alltext = [x['WordSegment'][0] for x in youdata]

c = {'商業':0 , '投資': 1, '政治': 2, '公共': 3, '寵物': 4, '育兒': 5, '知識': 6, '健康': 7, '故事': 8}
y = []
for i in youdata:
    y.append(c[i['Category']])

with open('./專題資料/PodcastWordSegment.json') as f:
    poddata = json.loads(f.read())

alltext.extend([x['WordSegment'][0] for x in poddata])

for i in poddata:
    y.append(c[i['Category']])
y = np.array(y)

from gensim.corpora import Dictionary
dct = Dictionary(alltext)
from tensorflow.keras.preprocessing import sequence

X = [dct.doc2idx(txt) for txt in alltext]
X = sequence.pad_sequences(X, padding='post', value=len(dct))
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Bidirectional
from keras_self_attention import SeqSelfAttention


model = Sequential()
model.add(Embedding(len(dct)+1,300,input_length=X.shape[1]))
model.add(Bidirectional(LSTM(128, return_sequences=True)))
model.add(SeqSelfAttention())
model.add(LSTM(128))
model.add(Dense(9,activation='softmax'))
model.summary()
model.compile(loss="sparse_categorical_crossentropy",optimizer="adam",metrics=["accuracy"])

model.fit(x=X_train,y=y_train, validation_split=0.1, epochs=20, verbose=1)
model.evaluate(X_test, y_test ,batch_size=10)
model.save('./分類系統/BiLSTM_Attention')