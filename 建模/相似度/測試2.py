from Gensim_Similarity import Gensimsim

gensim = Gensimsim()
#
# print(gensim.wordsim('./模型/FTT_S.model', ['薪資', 'ETF']))

print(gensim.docsim('./Word2Vec/W2V_C_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=0, top=3))
print(gensim.docsim('./Word2Vec/W2V_C_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=1, top=3))
print(gensim.docsim('./Word2Vec/W2V_C_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=2, top=3))
print(gensim.docsim('./Word2Vec/W2V_S_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=0, top=3))
print(gensim.docsim('./Word2Vec/W2V_S_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=1, top=3))
print(gensim.docsim('./Word2Vec/W2V_S_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=2, top=3))
print(gensim.docsim('./Word2Vec/D2V_B_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=0, top=3))
print(gensim.docsim('./Word2Vec/D2V_B_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=1, top=3))
print(gensim.docsim('./Word2Vec/D2V_B_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=2, top=3))
print(gensim.docsim('./Word2Vec/D2V_M_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=0, top=3))
print(gensim.docsim('./Word2Vec/D2V_M_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=1, top=3))
print(gensim.docsim('./Word2Vec/D2V_M_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=2, top=3))
print(gensim.docsim('./Word2Vec/FTT_C_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=0, top=3))
print(gensim.docsim('./Word2Vec/FTT_C_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=1, top=3))
print(gensim.docsim('./Word2Vec/FTT_C_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=2, top=3))
print(gensim.docsim('./Word2Vec/FTT_S_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=0, top=3))
print(gensim.docsim('./Word2Vec/FTT_S_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=1, top=3))
print(gensim.docsim('./Word2Vec/FTT_S_Index', './TFIDF/TFIDF_Dictionary', ['薪資', 'ETF'], './TFIDF/TitleIndex.json', datafrom=2, top=3))







# from gensim.corpora import Dictionary
# dct = Dictionary.load('./TFIDF/TFIDF_Dictionary')
# y = [x[0] for x in dct.doc2bow(['今天', '餛', '天氣'])]
# print([dct[x] for x in y])
