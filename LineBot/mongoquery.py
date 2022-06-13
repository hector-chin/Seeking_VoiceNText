import pymongo
import re

#### 連接位於 IP 位置的  mongodb
myclient = pymongo.MongoClient()
dblist = myclient.list_database_names()

# use 'test_1' 資料庫
test_1 = myclient['test_1']

# 指定 collections
test_1_youtube = test_1['youtubeData']
test_1_podcast = test_1['podcastData']
test_1_book = test_1['bookData']

# def mongo_youtube_query(event, mtext):
#     regx = re.compile(mtext, re.IGNORECASE)
#
#     youtubedata = test_1_youtube.find({"$or":[{'Title':regx,'Content':regx}]},{'_id':0,'Content':0}).limit(3).sort('Date',-1)
#     youtube_query_data = [i for i in youtubedata]
#
#     return youtube_query_data

def mongo_youtube_query(event, mtext, SEARCH_SETTING):
    ss = mtext.split(" ")
    if len(ss) == 1:
        regx = [re.compile(ss[0], re.IGNORECASE)]
    elif len(ss) == 2:
        regx = [re.compile(ss[0], re.IGNORECASE), re.compile(ss[1], re.IGNORECASE)]
    else:
        regx = [re.compile(ss[0], re.IGNORECASE), re.compile(ss[1], re.IGNORECASE), re.compile(ss[2], re.IGNORECASE)]

    if SEARCH_SETTING == 1:
        youtubedata = test_1_youtube.find({'Title': {'$all': regx}},{'_id': 0, 'Content': 0, 'Date': 0}).limit(3).sort('Date', -1)

    elif SEARCH_SETTING == 2:
        youtubedata = test_1_youtube.find({'Content': {'$all': regx}},{'_id': 0, 'Content': 0, 'Date': 0}).limit(3).sort('Date', -1)

    elif SEARCH_SETTING == 3:
        youtubedata = test_1_youtube.find({"$or": [{'Content': {"$all": regx}}, {'Title': {"$all": regx}}]},{'_id': 0, 'Content': 0, 'Date': 0}).limit(3).sort('Date', -1)

    youtube_query_data = [i for i in youtubedata]

    return youtube_query_data

# def mongo_youtube_query(event, mtext):
#     ss = mtext.split(" ")
#     if len(ss) == 1:
#         regx = [re.compile(ss[0], re.IGNORECASE)]
#     elif len(ss) == 2:
#         regx = [re.compile(ss[0], re.IGNORECASE), re.compile(ss[1], re.IGNORECASE)]
#     else:
#         regx = [re.compile(ss[0, re.IGNORECASE]), re.compile(ss[1], re.IGNORECASE), re.compile(ss[2], re.IGNORECASE)]
#
#     youtube_query_data=[]
#
#     # 1.標題跟內文都有
#     for data in test_1_youtube.find({"$and": [{'Title': {"$all": regx}, 'Content': {"$all": regx}}]},{'_id': 0, 'Content': 0, 'Date': 0}).limit(20).sort('Date', -1):
#         youtube_query_data.append(data)
#
#         if len(youtube_query_data) <= 20:
#             # 2.標題都有
#             for data in test_1_youtube.find({'Title': {"$all": regx}}, {'_id': 0, 'Content': 0, 'Date': 0}).limit(20).sort('Date', -1):
#                 if data not in youtube_query_data:
#                     youtube_query_data.append(data)
#         else:
#             pass
#
#     if len(youtube_query_data) <= 20:
#         # 4.標題有
#         for data in test_1_youtube.find({'Title': {"$in": regx}}, {'_id': 0, 'Content': 0, 'Date': 0}).limit(20).sort('Date', -1):
#             if data not in youtube_query_data:
#                 youtube_query_data.append(data)
#     else:
#         pass
#
#     if len(youtube_query_data) <= 20:
#         # 3.內文都有
#         for data in test_1_youtube.find({'Content': {"$all": regx}}, {'_id': 0, 'Content': 0, 'Date': 0}).limit(20).sort('Date', -1):
#             if data not in youtube_query_data:
#                 youtube_query_data.append(data)
#     else:
#         pass
#
#     if len(youtube_query_data) <= 20:
#         # 5.內文有
#         for data in test_1_youtube.find({'Content': {"$in": regx}}, {'_id': 0, 'Content': 0, 'Date': 0}).limit(20).sort('Date', -1):
#             if data not in youtube_query_data:
#                 youtube_query_data.append(data)
#     else:
#         pass
#
#     return youtube_query_data
#
#
def mongo_podcast_query(event, mtext, SEARCH_SETTING):
    ss = mtext.split(" ")
    if len(ss) == 1:
        regx = [re.compile(ss[0], re.IGNORECASE)]
    elif len(ss) == 2:
        regx = [re.compile(ss[0], re.IGNORECASE), re.compile(ss[1], re.IGNORECASE)]
    else:
        regx = [re.compile(ss[0], re.IGNORECASE), re.compile(ss[1], re.IGNORECASE), re.compile(ss[2], re.IGNORECASE)]

    if SEARCH_SETTING == 1:
        podcastdata = test_1_podcast.find({'Title': {'$all': regx}}, {'_id': 0, 'Content': 0, 'Date': 0}).limit(3).sort('Date', -1)

    elif SEARCH_SETTING == 2:
        podcastdata = test_1_podcast.find({'Content': {'$all': regx}}, {'_id': 0, 'Content': 0, 'Date': 0}).limit(3).sort('Date', -1)

    elif SEARCH_SETTING == 3:
        podcastdata = test_1_podcast.find({"$or": [{'Content': {"$all": regx}}, {'Title': {"$all": regx}}]},{'_id': 0, 'Content': 0, 'Date': 0}).limit(3).sort('Date', -1)

    podcast_query_data = [i for i in podcastdata]

    return podcast_query_data

def mongo_book_query(event,mtext, SEARCH_SETTING):
    ss = mtext.split(" ")
    if len(ss) == 1:
        regx = [re.compile(ss[0], re.IGNORECASE)]
    elif len(ss) == 2:
        regx = [re.compile(ss[0], re.IGNORECASE), re.compile(ss[1], re.IGNORECASE)]
    else:
        regx = [re.compile(ss[0], re.IGNORECASE), re.compile(ss[1], re.IGNORECASE), re.compile(ss[2], re.IGNORECASE)]

    if SEARCH_SETTING == 1:
        bookdata = test_1_book.find({'Title': {'$all': regx}}, {'_id': 0, 'Content': 0}).limit(3)

    elif SEARCH_SETTING == 2:
        bookdata = test_1_book.find({'Content': {'$all': regx}}, {'_id': 0, 'Content': 0}).limit(3)

    elif SEARCH_SETTING == 3:
        bookdata = test_1_book.find({"$or": [{'Content': {"$all": regx}}, {'Title': {"$all": regx}}]},{'_id': 0, 'Content': 0}).limit(3)

    book_query_data = [i for i in bookdata]

    return book_query_data


###################################################################################看更多
def mongo_youtube_query_re(event, SEARCH_TEXT_RECORD, NEW_YT_RECORD, SEARCH_SETTING):

    ss = SEARCH_TEXT_RECORD.split(" ")
    if len(ss) == 1:
        regx = [re.compile(ss[0], re.IGNORECASE)]
    elif len(ss) == 2:
        regx = [re.compile(ss[0], re.IGNORECASE), re.compile(ss[1], re.IGNORECASE)]
    else:
        regx = [re.compile(ss[0], re.IGNORECASE), re.compile(ss[1], re.IGNORECASE), re.compile(ss[2], re.IGNORECASE)]

    if SEARCH_SETTING == 1:
        youtubedata = test_1_youtube.find({'Title': {'$all': regx}},{'_id': 0, 'Content': 0, 'Date': 0}).limit(3).sort('Date', -1).skip(NEW_YT_RECORD*3).limit(3).sort('Date',-1)

    elif SEARCH_SETTING == 2:
        youtubedata = test_1_youtube.find({'Content': {'$all': regx}},{'_id': 0, 'Content': 0, 'Date': 0}).limit(3).sort('Date', -1).skip(NEW_YT_RECORD*3).limit(3).sort('Date',-1)

    elif SEARCH_SETTING == 3:
        youtubedata = test_1_youtube.find({"$or": [{'Content': {"$all": regx}}, {'Title': {"$all": regx}}]},{'_id': 0, 'Content': 0, 'Date': 0}).skip(NEW_YT_RECORD*3).limit(3).sort('Date',-1)

    youtube_query_data = [i for i in youtubedata]
    return youtube_query_data

def mongo_podcast_query_re(event, SEARCH_TEXT_RECORD, NEW_PC_RECORD, SEARCH_SETTING):
    ss = SEARCH_TEXT_RECORD.split(" ")
    if len(ss) == 1:
        regx = [re.compile(ss[0], re.IGNORECASE)]
    elif len(ss) == 2:
        regx = [re.compile(ss[0], re.IGNORECASE), re.compile(ss[1], re.IGNORECASE)]
    else:
        regx = [re.compile(ss[0], re.IGNORECASE), re.compile(ss[1], re.IGNORECASE), re.compile(ss[2], re.IGNORECASE)]

    if SEARCH_SETTING == 1:
        podcastdata = test_1_podcast.find({'Title': {'$all': regx}}, {'_id': 0, 'Content': 0, 'Date': 0}).limit(3).sort('Date', -1).skip(NEW_PC_RECORD*3).limit(3).sort('Date', -1)

    elif SEARCH_SETTING == 2:
        podcastdata = test_1_podcast.find({'Content': {'$all': regx}}, {'_id': 0, 'Content': 0, 'Date': 0}).limit(3).sort('Date', -1).skip(NEW_PC_RECORD*3).limit(3).sort('Date', -1)

    elif SEARCH_SETTING == 3:
        podcastdata = test_1_podcast.find({"$or": [{'Content': {"$all": regx}}, {'Title': {"$all": regx}}]},{'_id': 0, 'Content': 0, 'Date': 0}).skip(NEW_PC_RECORD*3).limit(3).sort('Date', -1)

    podcast_query_data = [i for i in podcastdata]

    return podcast_query_data

def mongo_book_query_re(event, SEARCH_TEXT_RECORD,NEW_BK_RECORD, SEARCH_SETTING):

    ss = SEARCH_TEXT_RECORD.split(" ")
    if len(ss) == 1:
        regx = [re.compile(ss[0], re.IGNORECASE)]
    elif len(ss) == 2:
        regx = [re.compile(ss[0], re.IGNORECASE), re.compile(ss[1], re.IGNORECASE)]
    else:
        regx = [re.compile(ss[0], re.IGNORECASE), re.compile(ss[1], re.IGNORECASE), re.compile(ss[2], re.IGNORECASE)]

    if SEARCH_SETTING == 1:
        bookdata = test_1_book.find({'Title': {'$all': regx}}, {'_id': 0, 'Content': 0}).skip(NEW_BK_RECORD*3).limit(3)

    elif SEARCH_SETTING == 2:
        bookdata = test_1_book.find({'Content': {'$all': regx}}, {'_id': 0, 'Content': 0}).skip(NEW_BK_RECORD*3).limit(3)

    elif SEARCH_SETTING == 3:
        bookdata = test_1_book.find({"$or": [{'Content': {"$all": regx}}, {'Title': {"$all": regx}}]},{'_id': 0, 'Content': 0}).skip(NEW_BK_RECORD*3).limit(3)

    book_query_data = [i for i in bookdata]

    return book_query_data
###################################################################################看更多
