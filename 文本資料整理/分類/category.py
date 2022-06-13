import json
import pandas as pd
with open('./YoutubeData.json') as f:
    youdata = json.loads(f.read())
with open('./PodcastData.json') as f:
    poddata = json.loads(f.read())
# z = {'政治':'1', '投資':'2', "健康":'3', "公共議題":'4', "商業":'5', "故事":'6', "育兒":'7', "寵物":'8', "小智慧":'9'}

with open('./NewYoutubeData_v1.json') as f:
    newyou = json.loads(f.read())

with open('./NewPodcastData_v1.json') as f:
    newpod = json.loads(f.read())
catedict = {}
danyou = pd.read_csv('./新分類/youtube分類.csv')
for x in range(len(danyou)):
    catedict.update({danyou.iloc[x,0][:-9]: danyou.iloc[x,1]})
laryou = pd.read_csv('./youtube集數連結_1123之後_Larry.csv', names=["Title", "Url", "Cate"])
for x in range(len(laryou)):
    catedict.update({laryou.iloc[x,0][:-9]: laryou.iloc[x,2]})
danpod = pd.read_csv('./新分類/podcast分類.csv')
for x in range(len(danpod)):
    catedict.update({danpod.iloc[x,0][:-9]: danpod.iloc[x,1]})
larpod = pd.read_csv('./podcast集數連結_1123之後_Larry.csv', names=["Title", "Url", "Cate"])
for x in range(len(larpod)):
    catedict.update({larpod.iloc[x,0][:-9]: larpod.iloc[x,2]})
with open('./cateshang.json') as f:
    shang = json.loads(f.read())
catedict.update(shang)
phoebe = pd.read_excel('./標題分類.xlsx', header=None)
for x in range(len(phoebe)):
    catedict.update({phoebe.iloc[x,0][:-9]: phoebe.iloc[x,1]})

for x in newyou:
    try:
        x.update({'Category': catedict[x['Title']]})
    except:
        x.update({'Category': '寵物'})

for x in newpod:
    try:
        x.update({'Category': catedict[x['Title']]})
    except:
        x.update({'Category': '寵物'})
youdata.extend(newyou)
poddata.extend(newpod)
print(len(youdata))
print(len(poddata))
with open('./YoutubeData_v1.json', 'w') as f:
    json.dump(youdata, f)
with open('./PodcastData_v1.json', 'w') as f:
    json.dump(poddata, f)