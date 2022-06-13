from TFIDF_Similarity import tfidfsim

print(tfidfsim('./TFIDF/TFIDF_M', './TFIDF/TFIDF_Dictionary', './TFIDF/TitleIndex.json', ['薪資', 'ETF'], 0, 3))
print(tfidfsim('./TFIDF/TFIDF_M', './TFIDF/TFIDF_Dictionary', './TFIDF/TitleIndex.json', ['薪資', 'ETF'], 1, 3))
print(tfidfsim('./TFIDF/TFIDF_M', './TFIDF/TFIDF_Dictionary', './TFIDF/TitleIndex.json', ['薪資', 'ETF'], 2, 3))
print(tfidfsim('./TFIDF/TFIDF_S', './TFIDF/TFIDF_Dictionary', './TFIDF/TitleIndex.json', ['薪資', 'ETF'], 0, 3))
print(tfidfsim('./TFIDF/TFIDF_S', './TFIDF/TFIDF_Dictionary', './TFIDF/TitleIndex.json', ['薪資', 'ETF'], 1, 3))
print(tfidfsim('./TFIDF/TFIDF_S', './TFIDF/TFIDF_Dictionary', './TFIDF/TitleIndex.json', ['薪資', 'ETF'], 2, 3))