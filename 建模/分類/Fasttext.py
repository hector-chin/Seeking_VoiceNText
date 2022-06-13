import json
import numpy as np
with open('./分類系統/WordSegmentClassData.json') as f:
    data = json.loads(f.read())
# 2-gram
alltext = []
for i in data:
    tl = i[0]
    if len(i[0]) > 1:
        tl2 = []
        for x in range(len(i[0]) - 1):
            tl2.append(' '.join(i[0][x:x + 2]))
        tl.extend(tl2)
    alltext.append(tl)
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
from tensorflow.keras.layers import GlobalAveragePooling1D

print('Build model...')
model = Sequential()
# 我們從一個有效的嵌入層（embedding layer）開始，它將我們的詞彙索引（vocab indices ）映射到詞向量的維度上.
model.add(Embedding(len(dct) + 1, 150, input_length=X.shape[1]))
# 我們增加 GlobalAveragePooling1D, 這將平均計算文檔中所有詞彙的的詞嵌入
model.add(GlobalAveragePooling1D())
# 我們投射到單個單位的輸出層上
model.add(Dense(9, activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy',
              optimizer="adam",
              metrics=['accuracy'])
model.summary()
model.fit(x=X_train, y=y_train, validation_split=0.1, epochs=150, verbose=1)
model.evaluate(X_test, y_test ,batch_size=10)
model.save('./分類系統/FastText')