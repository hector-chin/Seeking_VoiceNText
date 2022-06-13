from gensim.models import word2vec
from gensim.models import doc2vec
from gensim.models import fasttext
from gensim.similarities import SoftCosineSimilarity
import json

# class Gensimsim():
#     def dct(self):
#         return Dictionary.load(self.DictionaryPath)
#
#     def titleindex(self):
#         with open(self.TitleIndexPath) as f:
#             ti = json.loads(f.read())
#         return ti
#
#     def model(self, use, parameter):
#         if use == 0:
#             return word2vec.Word2Vec.load('./模型/word2vec_ALL_cbow.model') if parameter == 0 else word2vec.Word2Vec.load('./模型/word2vec_ALL_skip-gram.model')
#         elif use == 1:
#             return doc2vec.Doc2Vec.load('./模型/doc2vec_ALL_DBOW.model') if parameter == 0 else doc2vec.Doc2Vec.load('./模型/doc2vec_ALL_dm.model')
#         elif use == 2:
#             return fasttext.FastText.load('./模型/fasttext_ALL_cbow.model')if parameter == 0 else fasttext.FastText.load('./模型/fasttext_ALL_skip-gram.model')
#
#     def wordsim(self, use, parameter, textlist):
#         model = self.model(use=use, parameter=parameter)
#         return model.wv.most_similar(textlist)
#
#     def docsim(self, simindexpath, dictionarypath, textlist, titleindexpath, datafrom=None, top=None):
#         file = simindexpath[-1:-12:-1]
#         use = file[:3]
#         parameter = file[4:5]
#         if use == 'W2V':
#             docsim_index = SoftCosineSimilarity.load(simindexpath) if parameter == 'C' else SoftCosineSimilarity.load(simindexpath)
#         elif use == 'Doc':
#             docsim_index = SoftCosineSimilarity.load(simindexpath) if parameter == 'B' else SoftCosineSimilarity.load(simindexpath)
#         elif use == 'FTT':
#             docsim_index = SoftCosineSimilarity.load(simindexpath) if parameter == 'C' else SoftCosineSimilarity.load(simindexpath)
#         dct = Dictionary.load(dictionarypath)
#         sim = docsim_index[dct.doc2bow(textlist)]
#         with open(titleindexpath) as f:
#             ti = json.loads(f.read())
#         if top is None:
#             top = len(dct)
#         if datafrom == 0:
#             return [(ti[str(document_number)], score) for document_number, score in
#                     sorted(enumerate(sim[:3378]), key=lambda x: x[1], reverse=True)[:top]]
#         elif datafrom == 1:
#             return [(ti[str(document_number + 3378)], score) for document_number, score in
#                     sorted(enumerate(sim[3378:5540]), key=lambda x: x[1], reverse=True)[:top]]
#         elif datafrom == 2:
#             return [(ti[str(document_number + 5540)], score) for document_number, score in
#                     sorted(enumerate(sim[5540:]), key=lambda x: x[1], reverse=True)[:top]]
#         else:
#             return [(ti[str(document_number)], score) for document_number, score in
#                     sorted(enumerate(sim), key=lambda x: x[1], reverse=True)[:top]]


# import json
# with open('./Bow_Corpus.json') as f:
#     bow_corpus = json.loads(f.read())
#
# model = fasttext.FastText.load('./模型/fasttext_ALL_skip-gram.model')
# # print(model.wv.most_similar(['瘦身', '減重']))
#
# from gensim.similarities import WordEmbeddingSimilarityIndex
# termsim_index = WordEmbeddingSimilarityIndex(model.wv)
# from gensim.corpora import Dictionary
# dictionary = Dictionary.load('./TFIDF/TFIDF_Dictionary')
# from gensim.similarities import SoftCosineSimilarity, SparseTermSimilarityMatrix
# similarity_matrix = SparseTermSimilarityMatrix(termsim_index, dictionary)
# docsim_index = SoftCosineSimilarity(bow_corpus, similarity_matrix)
# docsim_index.save('./Word2Vec/FTT_S_Index')
# sims = docsim_index[dictionary.doc2bow(['瘦身', '健康', '減脂'])]
# print(sims)

sim = word2vec.Word2Vec.load('./模型/W2V_C.model')
print(sim.wv.most_similar([]))
