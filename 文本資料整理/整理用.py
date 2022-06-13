import json
with open('./NewYoutubeWordSegment.json') as f:
    newyou = json.loads(f.read())

from ckiptagger import construct_dictionary, WS
ws = WS(r'C:\Users\Tibame_T14\Desktop\CFI101_AIproject\data')
with open(r'C:\Users\Tibame_T14\Desktop\CFI101_AIproject\worddict.txt', encoding='utf-8') as f:
    worddict = f.read().split('\n')
word_to_weight = {}
for i in worddict:
    word_to_weight.update({i:1})
dictionary = construct_dictionary(word_to_weight)

# with open('./NewYoutubeData.json') as f:
#     youdata = json.loads(f.read())
#
# NewYoutubeWordSegment = []
#
# for ep in youdata:
#     wordlist = []
#     wordlist.extend(ws([ep['Title']], recommend_dictionary = dictionary))
#     content = ep['Content'].split('_')
#     contentseglist = ws(content, recommend_dictionary = dictionary)
#     contentseg = []
#     for i in contentseglist:
#         contentseg.extend(i)
#     wordlist.append(contentseg)
#     NewYoutubeWordSegment.append({'Title': ep['Title'], 'WordSegment': wordlist, 'Url': ep['Url'], 'Date': ep['Date']})
#
# with open('./NewYoutubeWordSegment.json', 'w') as f:
#     json.dump(NewYoutubeWordSegment,f)
#
# with open('./NewPodcastData.json') as f:
#     poddata = json.loads(f.read())
#
# NewPodcastWordSegment = []
#
# for ep in poddata:
#     wordlist = []
#     wordlist.extend(ws([ep['Title']], recommend_dictionary=dictionary))
#     content = ep['Content'].split('_')
#     contentseglist = ws(content, recommend_dictionary=dictionary)
#     contentseg = []
#     for i in contentseglist:
#         contentseg.extend(i)
#     wordlist.append(contentseg)
#     NewPodcastWordSegment.append({'Title': ep['Title'], 'WordSegment': wordlist, 'Url': ep['Url'], 'Date': ep['Date']})
#
# with open('./NewPodcastWordSegment.json', 'w') as f:
#     json.dump(NewPodcastWordSegment, f)

with open('./NewYoutubeData_Shang.json') as f:
    syoudata = json.loads(f.read())

NewYoutubeWordSegmentS = []

for ep in syoudata:
    wordlist = []
    wordlist.extend(ws([ep['Title']], recommend_dictionary=dictionary))
    content = ep['Content'].split('_')
    contentseglist = ws(content, recommend_dictionary=dictionary)
    contentseg = []
    for i in contentseglist:
        contentseg.extend(i)
    wordlist.append(contentseg)
    NewYoutubeWordSegmentS.append({'Title': ep['Title'], 'WordSegment': wordlist, 'Url': ep['Url'], 'Date': ep['Date']})
    newyou.append({'Title': ep['Title'], 'WordSegment': wordlist, 'Url': ep['Url'], 'Date': ep['Date']})

with open('./NewYoutubeWordSegment_v1.json', 'w') as f:
    json.dump(newyou, f)

with open('./NewYoutubeWordSegment_Shang.json', 'w') as f:
    json.dump(NewYoutubeWordSegmentS, f)