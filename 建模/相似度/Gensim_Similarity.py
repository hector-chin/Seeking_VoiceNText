from gensim.models import word2vec
from gensim.models import doc2vec
from gensim.models import fasttext
from gensim.similarities import SoftCosineSimilarity
from gensim.corpora import Dictionary
import json

class Gensimsim():
    def wordsim(self, modelpath, textlist):
        file = modelpath[-11:]
        use = file[:3]
        if use == 'W2V':
            return word2vec.Word2Vec.load(modelpath).wv.most_similar(textlist)
        elif use == 'D2V':
            return doc2vec.Doc2Vec.load(modelpath).wv.most_similar(textlist)
        elif use == 'FTT':
            return fasttext.FastText.load(modelpath).wv.most_similar(textlist)

    def docsim(self, simindexpath, dictionarypath, textlist, titleindexpath, datafrom=None, top=None):
        docsim_index = SoftCosineSimilarity.load(simindexpath)
        dct = Dictionary.load(dictionarypath)
        sim = docsim_index[dct.doc2bow(textlist)]
        with open(titleindexpath) as f:
            ti = json.loads(f.read())
        if top is None:
            top = len(dct)
        if datafrom == 0:
            return [(ti[str(document_number)], score) for document_number, score in
                    sorted(enumerate(sim[:3378]), key=lambda x: x[1], reverse=True)[:top] if score > 0]
        elif datafrom == 1:
            return [(ti[str(document_number + 3378)], score) for document_number, score in
                    sorted(enumerate(sim[3378:5540]), key=lambda x: x[1], reverse=True)[:top] if score > 0]
        elif datafrom == 2:
            return [(ti[str(document_number + 5540)], score) for document_number, score in
                    sorted(enumerate(sim[5540:]), key=lambda x: x[1], reverse=True)[:top] if score > 0]
        else:
            return [(ti[str(document_number)], score) for document_number, score in
                    sorted(enumerate(sim), key=lambda x: x[1], reverse=True)[:top] if score > 0]
