from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.similarities import MatrixSimilarity
from gensim.similarities import SparseMatrixSimilarity
import json

with open('./專題資料/BookData.json') as f:
    book = json.loads(f.read())
with open('./專題資料/新資料/新分類/YoutubeData_v1.json') as f:
    youtube = json.loads(f.read())
# with open('./專題資料/新資料/NewYoutubeWordSegment_v1.json') as f:
#     youtube.extend(json.loads(f.read()))
with open('./專題資料/新資料/新分類/PodcastData_v1.json') as f:
    podcast = json.loads(f.read())
# with open('./專題資料/新資料/NewPodcastWordSegment_v1.json') as f:
#     podcast.extend(json.loads(f.read()))
print(len(book))
print(len(youtube))
print(len(podcast))
titleindexdict = {}
alltext = []
index = 0
for i in book:
    titleindexdict.update({index: {'Title': i['Title'], 'Url': i['Url']}})
    index += 1
    textlist = []
    # textlist.extend(i['WordSegment'][0])
    # textlist.extend(i['WordSegment'][1])
    # alltext.append(textlist)
for i in youtube:
    titleindexdict.update({index: {'Title': i['Title'], 'Url': i['Url'], 'Date': i['Date']}})
    index += 1
    textlist = []
    # textlist.extend(i['WordSegment'][0])
    # textlist.extend(i['WordSegment'][1])
    # alltext.append(textlist)
for i in podcast:
    titleindexdict.update({index: {'Title': i['Title'], 'Url': i['Url'], 'Date': i['Date']}})
    index += 1
    textlist = []
    # textlist.extend(i['WordSegment'][0])
    # textlist.extend(i['WordSegment'][1])
    # alltext.append(textlist)

with open('./專題資料/newmodel/DataIndexDict.json', 'w') as f:
    json.dump(titleindexdict, f)

# with open('./專題資料/newmodel/AllDataSegment', 'w') as f:
#     json.dump(alltext, f)
#
# print(len(titleindexdict))
# print(len(alltext))
# dct = Dictionary(alltext)  # fit dictionary
# dct.save('./專題資料/newmodel/Dictionary')
# corpus = [dct.doc2bow(line) for line in alltext]
# model = TfidfModel(corpus)
# model.save('./專題資料/newmodel/TFIDF_Model')
# index_tmpfile = dct
# # index = MatrixSimilarity(model[corpus], num_features=len(dct))
# # index.save('./TFIDF/TFIDF_MatrixSimilarityIndex')
# index2 = SparseMatrixSimilarity(model[corpus], num_features=len(dct))
# index2.save('./專題資料/newmodel/TFIDF_S')
