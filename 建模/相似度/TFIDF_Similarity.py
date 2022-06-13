from gensim.corpora import Dictionary
from gensim.similarities import MatrixSimilarity
from gensim.similarities import SparseMatrixSimilarity
import json


def tfidfsim(indexpath, dictionarypath, titleindexpath, textlist, datafrom=None, top=None):
    index = MatrixSimilarity.load(indexpath) if indexpath[-1] == 'M' else SparseMatrixSimilarity.load(indexpath)
    dct = Dictionary.load(dictionarypath)
    query = dct.doc2bow(textlist)
    with open(titleindexpath) as f:
        ti = json.loads(f.read())
    sim = index[query]
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



