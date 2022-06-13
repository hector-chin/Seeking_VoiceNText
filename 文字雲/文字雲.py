import json
import numpy as np
from PIL import Image
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

with open('./專題資料/新資料/新分類/YoutubeWordSegment_v1.json') as f:
    youdata = json.loads(f.read())
with open('./專題資料/新資料/新分類/PodcastWordSegment_v1.json') as f:
    poddata = json.loads(f.read())

cate10 = []
# 政治
# 投資
# 健康
# 公共議題
# 商業
# 故事
# 育兒
# 寵物
# 小智慧
# 20211214
# 20211207
# 20211121

for x in poddata:
    if x['Category'] == '小智慧' and 20211121 <= int(x['Date']) < 20211221:
        cate10.extend(x['WordSegment'])
for x in youdata:
    if x['Category'] == '小智慧' and 20211121 <= int(x['Date']) < 20211221:
        cate10.extend(x['WordSegment'])

seg_counter = Counter([i for x in cate10 for i in x])
clouddict = {}
with open('./AllStopword.txt', encoding='utf-8') as f:
    stop = f.read().split('\n')
for x, y in seg_counter.items():
    if x not in stop:
        if x in clouddict:
            clouddict[x] += y
        else:
            clouddict[x] = y
font_path = 'jf-openhuninn-1.1.ttf'  # 設定字體格式
mask = np.array(Image.open('./cloudmask.png'))
wc = WordCloud(background_color='white', font_path=font_path, min_font_size=40, max_words=100, mask=mask,
               random_state=1)
wc.generate_from_frequencies(clouddict)
plt.imshow(wc)
plt.axis("off")
plt.show()
wc.to_file('./文字雲/93.png')
