import json

with open('./專題資料/BookWordSegment.json') as f:
    book = json.loads(f.read())
with open('./專題資料/YoutubeWordSegment.json') as f:
    youtube = json.loads(f.read())
with open('./專題資料/新資料/NewYoutubeWordSegment_v1.json') as f:
    youtube.extend(json.loads(f.read()))
with open('./專題資料/PodcastWordSegment.json') as f:
    podcast = json.loads(f.read())
with open('./專題資料/新資料/NewPodcastWordSegment_v1.json') as f:
    podcast.extend(json.loads(f.read()))

from gensim.models import word2vec

alltext = []
for x in book:
    se = []
    se.extend(x['WordSegment'][0])
    se.extend(x['WordSegment'][1])
    alltext.append(se)
for x in youtube:
    se = []
    se.extend(x['WordSegment'][0])
    se.extend(x['WordSegment'][1])
    alltext.append(se)
for x in podcast:
    se = []
    se.extend(x['WordSegment'][0])
    se.extend(x['WordSegment'][1])
    alltext.append(se)
print(len(alltext))

model = word2vec.Word2Vec(alltext, vector_size=300, sg=0, window=10, workers=4, min_count=1)

model.save("./專題資料/newmodel/W2V_C.model")

print(model.wv.most_similar('VR'))