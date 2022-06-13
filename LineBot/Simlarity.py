from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity
from gensim.models import word2vec
import json


class Sim:
    def __init__(self, indexpath, dictionarypath, titleindexpath, modelpath):
        self.indexpath = indexpath
        self.dictionarypath = dictionarypath
        self.titleindexpath = titleindexpath
        self.modelpath = modelpath

    def dct(self):
        return Dictionary.load(self.dictionarypath)

    def sparse(self, textlist, datafrom=None, top=None):
        index = SparseMatrixSimilarity.load(self.indexpath)
        dct = self.dct()
        query = dct.doc2bow(textlist)
        with open(self.titleindexpath) as f:
            ti = json.loads(f.read())
        sim = index[query]
        if top is None:
            top = len(dct)
        if datafrom == 0:
            return [(ti[str(document_number)]['Title'], score, ti[str(document_number)]['Url']) for
                    document_number, score in
                    sorted(enumerate(sim[:3378]), key=lambda x: x[1], reverse=True)[:top]
                    if score > 0]
        elif datafrom == 1:
            return [(ti[str(document_number + 3378)]['Title'], score, ti[str(document_number + 3378)]['Url']) for
                    document_number, score in
                    sorted(enumerate(sim[3378:5540]), key=lambda x: (x[1], int(ti[str(x[0] + 3378)]['Date'])),
                           reverse=True)[:top] if score > 0]
        elif datafrom == 2:
            return [(ti[str(document_number + 5540)]['Title'], score, ti[str(document_number + 5540)]['Url']) for
                    document_number, score in
                    sorted(enumerate(sim[5540:]), key=lambda x: (x[1], int(ti[str(x[0] + 5540)]['Date'])),
                           reverse=True)[:top] if score > 0]
        else:
            return [(ti[str(document_number)]['Title'], score, ti[str(document_number)]['Url']) for document_number, score in
                    sorted(enumerate(sim), key=lambda x: x[1], reverse=True)[:top] if
                    score > 0]

    def wordsim(self, textlist):
        return word2vec.Word2Vec.load(self.modelpath).wv.most_similar(textlist)

    def sim(self, textlist, datafrom=None, top=None):
        recommend = self.sparse(textlist, datafrom=datafrom, top=top)
        if top is None:
            top = len(self.dct())
        if len(recommend) < 3:
            newrecommend = [x[0] for x in self.wordsim(textlist)[:3]]
            recommend.extend(self.sparse(newrecommend, datafrom=datafrom, top=top))
            return recommend[:top]
        else:
            return recommend
