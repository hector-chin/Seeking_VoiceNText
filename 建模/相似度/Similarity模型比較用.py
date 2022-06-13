from TFIDF_Similarity import tfidfsim
from Gensim_Similarity import Gensimsim
from glove import Glove
import time

def wordtest(path, text):
    print(path[-11:-6])
    start = time.time()
    gensim = Gensimsim()
    print(gensim.docsim(path, './TFIDF/TFIDF_Dictionary', text, './TFIDF/TitleIndex.json', datafrom=0, top=3))
    print(gensim.docsim(path, './TFIDF/TFIDF_Dictionary', text, './TFIDF/TitleIndex.json', datafrom=1, top=3))
    print(gensim.docsim(path, './TFIDF/TFIDF_Dictionary', text, './TFIDF/TitleIndex.json', datafrom=2, top=3))
    end = time.time()
    print(end - start)


text = ['要不要', '把', '你', '的', '功課', '丟給', '我']
wordtest('./Word2Vec/W2V_C_Index', text)
wordtest('./Word2Vec/W2V_S_Index', text)
wordtest('./Word2Vec/D2V_B_Index', text)
wordtest('./Word2Vec/D2V_M_Index', text)
wordtest('./Word2Vec/FTT_C_Index', text)
wordtest('./Word2Vec/FTT_S_Index', text)

print('TFIDF-Matrix')
start = time.time()
print(tfidfsim('./TFIDF/TFIDF_M', './TFIDF/TFIDF_Dictionary', './TFIDF/TitleIndex.json', text, datafrom=0, top=3))
print(tfidfsim('./TFIDF/TFIDF_M', './TFIDF/TFIDF_Dictionary', './TFIDF/TitleIndex.json', text, datafrom=1, top=3))
print(tfidfsim('./TFIDF/TFIDF_M', './TFIDF/TFIDF_Dictionary', './TFIDF/TitleIndex.json', text, datafrom=2, top=3))
end = time.time()
print(end - start)

print('TFIDF-SparseMatrix')
start = time.time()
print(tfidfsim('./TFIDF/TFIDF_S', './TFIDF/TFIDF_Dictionary', './TFIDF/TitleIndex.json', text, datafrom=0, top=3))
print(tfidfsim('./TFIDF/TFIDF_S', './TFIDF/TFIDF_Dictionary', './TFIDF/TitleIndex.json', text, datafrom=1, top=3))
print(tfidfsim('./TFIDF/TFIDF_S', './TFIDF/TFIDF_Dictionary', './TFIDF/TitleIndex.json', text, datafrom=2, top=3))
end = time.time()
print(end - start)
# glove_model = Glove.load('./模型/glove_ALL/glove.model')
# print(glove_model.most_similar('餛飩湯', 10))


