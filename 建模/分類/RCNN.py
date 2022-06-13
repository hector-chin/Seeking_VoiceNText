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

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

X_train_padded_seqs = sequence.pad_sequences(X_train, padding='post', maxlen=max([len(x) for x in X]), value=len(dct))
X_test_padded_seqs = sequence.pad_sequences(X_test, padding='post', maxlen=max([len(x) for x in X]), value=len(dct))

left_train_word_ids = [[len(dct)] + x[:-1] for x in X_train]
left_test_word_ids = [[len(dct)] + x[:-1] for x in X_test]
right_train_word_ids = [x[1:] + [len(dct)] for x in X_train]
right_test_word_ids = [x[1:] + [len(dct)] for x in X_test]

# 分別對左邊和右邊的詞進行編碼
left_train_padded_seqs = sequence.pad_sequences(left_train_word_ids, padding='post', maxlen=max([len(x) for x in X]), value=len(dct))
left_test_padded_seqs = sequence.pad_sequences(left_test_word_ids, padding='post', maxlen=max([len(x) for x in X]), value=len(dct))
right_train_padded_seqs = sequence.pad_sequences(right_train_word_ids, padding='post', maxlen=max([len(x) for x in X]), value=len(dct))
right_test_padded_seqs = sequence.pad_sequences(right_test_word_ids, padding='post', maxlen=max([len(x) for x in X]), value=len(dct))

from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import concatenate
from tensorflow.keras.layers import TimeDistributed
from tensorflow.keras.layers import Lambda
from tensorflow.keras import backend
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Model

# 模型共有三個輸入，分別是左詞，右詞和中心詞
document = Input(shape = (None, ))
left_context = Input(shape = (None, ))
right_context = Input(shape = (None, ))

# 構建詞向量
embedder = Embedding(len(dct) + 1, 300, input_length = max([len(x) for x in X]))
doc_embedding = embedder(document)
l_embedding = embedder(left_context)
r_embedding = embedder(right_context)

forward = LSTM(256, return_sequences = True)(l_embedding)
backward = LSTM(256, return_sequences = True, go_backwards = True)(r_embedding)
together = concatenate([forward, doc_embedding, backward], axis = 2)

semantic = TimeDistributed(Dense(128, activation = "tanh"))(together)

pool_rnn = Lambda(lambda x: backend.max(x, axis = 1), output_shape = (128, ))(semantic)
output = Dense(9, activation = "softmax")(pool_rnn)
model = Model(inputs = [document, left_context, right_context], outputs = output)
model.summary()
model.compile(loss="sparse_categorical_crossentropy",optimizer="adam",metrics=["accuracy"])

model.fit([X_train_padded_seqs, left_train_padded_seqs, right_train_padded_seqs], y_train, validation_split=0.1, epochs=20, verbose=1)
model.evaluate([X_test_padded_seqs, left_test_padded_seqs, right_test_padded_seqs], y_test ,batch_size=10)
model.save('./分類系統/RCNN')