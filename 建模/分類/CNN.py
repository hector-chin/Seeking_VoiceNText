import json
import numpy as np
with open('./分類系統/WordSegmentClassData.json') as f:
    data = json.loads(f.read())

alltext = [x[0] for x in data]
c = ['商業', '投資', '政治', '公共', '寵物', '育兒', '知識', '健康', '故事']
y = []
for i in data:
    for j, k in enumerate(c):
        if i[1] == k:
            y.append(j)
            break
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
from tensorflow.keras.layers import Convolution1D
from tensorflow.keras.layers import MaxPool1D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import BatchNormalization
model = Sequential()
model.add(Embedding(len(dct)+1, 300, input_length=X.shape[1]))
model.add(Convolution1D(128, 3, padding='same'))
model.add(MaxPool1D(3, 3, padding='same'))
model.add(Convolution1D(64, 3, padding='same'))
model.add(MaxPool1D(3, 3, padding='same'))
model.add(Convolution1D(32, 3, padding='same'))
model.add(Flatten())
model.add(Dropout(0.1))
model.add(BatchNormalization()) # (批)規範化層
model.add(Dense(125, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(9, activation='softmax'))
model.summary()
model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

model.fit(x=X_train, y=y_train, validation_split=0.1, epochs=100, verbose=1)
model.evaluate(X_test, y_test, batch_size=10)
model.save('./分類系統/CNN')
