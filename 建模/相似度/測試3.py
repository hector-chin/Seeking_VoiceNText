from Simlarity import Sim

sim = Sim('./模型資料/TFIDF_S', './模型資料/Dictionary', './模型資料/DataIndexDict.json', './模型資料/W2V_C.model')
# datafrom 資料來源
# books => 0
# youtube => 1
# podcast => 2
# top 前n筆高相關
print(sim.sim(textlist=['餛飩湯'], datafrom=1, top=5))

