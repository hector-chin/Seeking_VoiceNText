from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,QuickReply, QuickReplyButton, MessageAction

from sqlsetting import query_mysql, insert1_mysql, insert2_mysql, update1_mysql, update2_mysql, query_search_record, update0_mysql, update_YT_mysql, update_PC_mysql, update_BK_mysql, update0_mysql_2, update3_mysql_all, update3_mysql_content, update3_mysql_title
from mongoquery import mongo_book_query, mongo_youtube_query, mongo_podcast_query, mongo_youtube_query_re, mongo_podcast_query_re, mongo_book_query_re

from ckiptagger import construct_dictionary, WS
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity
from gensim.models import word2vec
import json
import threading

line_bot_api = LineBotApi('')
handler = WebhookHandler('')

baseurl = ''

# def getmodel():
#     global index, dct, ti, wordsim
default_1 = './static/model_data/TFIDF_S'
default_2 = './static/model_data/Dictionary'
default_3 = './static/model_data/DataIndexDict.json'
default_4 = './W2V_C.model'

index = SparseMatrixSimilarity.load(default_1)
dct = Dictionary.load(default_2)

with open(default_3, 'r') as f:
    ti = json.load(f)

wordsim = word2vec.Word2Vec.load(default_4)
print('model load ok')

# thread0 = threading.Thread(target=getmodel)
# thread0.start()

# def ckipword():
#     global ws, path_CIS_dict, dict_for_CKIP
ws = WS('./static/data')
path_CIS_dict = './static/worddict.txt'
with open(path_CIS_dict, encoding='utf-8') as f:
    emphasize = f.read().split('\n')

# 將list轉成dict型態，這邊每個權重都設為1
dict_for_CKIP = {i: 1 for i in emphasize}

# construct_dictionary的格式轉換
dict_for_CKIP = construct_dictionary(dict_for_CKIP)
print('ckip load ok')

# thread1 = threading.Thread(target=ckipword)
# thread1.start()


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)   # 設定收到文字訊息時要做的回應
def handle_message(event):
    mtext = event.message.text   # 本次傳進來的文字訊息
    mtext_ckip = ws([mtext], recommend_dictionary = dict_for_CKIP)[0]
    if mtext in ['@精準搜尋','@其他精準搜尋']:    # 當收到'@精準搜尋', 連到資料庫查詢當前設定, 並修改設定為1
        # try:
        FUNC_SETTING = query_mysql(event)  # 查詢mysql資料庫
        if FUNC_SETTING == None:
            insert1_mysql(event)
        elif FUNC_SETTING[0] == '1':
            pass
        elif FUNC_SETTING[0] == '2':
            update1_mysql(event)

        message = TextSendMessage(text="請輸入要精準搜尋的範圍:",
                                      quick_reply=QuickReply(
                                          items=[QuickReplyButton(action=MessageAction(label="找標題", text="@找標題")),
                                                 QuickReplyButton(action=MessageAction(label="找內文", text="@找內文")),
                                                 QuickReplyButton(action=MessageAction(label="找標題+內文", text="@找全文"))]
                                      )
                                      )

        line_bot_api.reply_message(event.reply_token, message)
        # except:
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext in ['@找標題', '@找內文', '@找全文']:
        # try:
        # FUNC_SETTING = query_mysql(event)  # 查詢mysql資料庫
        if mtext == '@找標題':
            update3_mysql_title(event)
        elif mtext == '@找內文':
            update3_mysql_content(event)
        elif mtext == '@找全文':
            update3_mysql_all(event)

        message = TextSendMessage(text='請輸入要精準搜尋"'+ mtext[-2:] +'"的詞彙:')

        line_bot_api.reply_message(event.reply_token, message)
        # except:
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext == '@關聯搜尋' or mtext == '@其他關聯搜尋':    # 當收到'@關聯搜尋', 連到資料庫查詢當前設定, 並修改設定為2
        try:
            FUNC_SETTING = query_mysql(event)  # 查詢資料庫

            if FUNC_SETTING == None:
                insert2_mysql(event)
            elif FUNC_SETTING[0] == '1':
                update2_mysql(event)
            elif FUNC_SETTING[0] == '2':
                pass

            message = TextSendMessage(text="請輸入要關聯搜尋的詞彙:")
            line_bot_api.reply_message(event.reply_token, message)

        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

#######################################################################################################################

    elif mtext.startswith('@') == False :    # 當收到非'@'開頭文字, 讀取資料庫查詢要執行的服務
        # try:
        FUNC_SETTING, SEARCH_SETTING = query_mysql(event)  # 查詢資料庫的FUNC設定

        if FUNC_SETTING == None:
            message = TextSendMessage(text="請先選擇要使用的服務!")


########################################################################################################## 第一次精準搜尋▼
        elif FUNC_SETTING[0] == '1':        # 將 mtext 做精準搜尋
            update0_mysql(event)

            youtube_query_data = mongo_youtube_query(event, mtext, SEARCH_SETTING)
            podcast_query_data = mongo_podcast_query(event, mtext, SEARCH_SETTING)
            book_query_data = mongo_book_query(event, mtext, SEARCH_SETTING)

            if len(youtube_query_data) == 0:
                youtube_text = "查無相關結果\n可嘗試其他搜尋方式\n"
            elif len(youtube_query_data) == 1:
                youtube_text = "{}\n{}".format(
                    youtube_query_data[0]["Title"],
                    youtube_query_data[0]["Url"])
            elif len(youtube_query_data) == 2:
                youtube_text = "{}\n{}\n{}\n{}".format(
                    youtube_query_data[0]["Title"],
                    youtube_query_data[0]["Url"],
                    youtube_query_data[1]["Title"],
                    youtube_query_data[1]["Url"])
            elif len(youtube_query_data) == 3:
                youtube_text = "{}\n{}\n{}\n{}\n{}\n{}".format(
                    youtube_query_data[0]["Title"],
                    youtube_query_data[0]["Url"],
                    youtube_query_data[1]["Title"],
                    youtube_query_data[1]["Url"],
                    youtube_query_data[2]["Title"],
                    youtube_query_data[2]["Url"])

            if len(podcast_query_data) == 0:
                podcast_text = "查無相關結果\n可嘗試其他搜尋方式\n"
            elif len(podcast_query_data) == 1:
                podcast_text = "{}\n{}".format(
                    podcast_query_data[0]["Title"],
                    podcast_query_data[0]["Url"])
            elif len(podcast_query_data) == 2:
                podcast_text = "{}\n{}\n{}\n{}".format(
                    podcast_query_data[0]["Title"],
                    podcast_query_data[0]["Url"],
                    podcast_query_data[1]["Title"],
                    podcast_query_data[1]["Url"])
            elif len(podcast_query_data) == 3:
                podcast_text = "{}\n{}\n{}\n{}\n{}\n{}".format(
                    podcast_query_data[0]["Title"],
                    podcast_query_data[0]["Url"],
                    podcast_query_data[1]["Title"],
                    podcast_query_data[1]["Url"],
                    podcast_query_data[2]["Title"],
                    podcast_query_data[2]["Url"])

            if len(book_query_data) == 0:
                book_text = "查無相關結果\n可嘗試其他搜尋方式\n"
            elif len(book_query_data) == 1:
                book_text = "{}\n{}".format(
                    book_query_data[0]["Title"],
                    book_query_data[0]["Url"])
            elif len(book_query_data) == 2:
                book_text = "{}\n{}\n{}\n{}".format(
                    book_query_data[0]["Title"],
                    book_query_data[0]["Url"],
                    book_query_data[1]["Title"],
                    book_query_data[1]["Url"])
            elif len(book_query_data) == 3:
                book_text = "{}\n{}\n{}\n{}\n{}\n{}".format(
                    book_query_data[0]["Title"],
                    book_query_data[0]["Url"],
                    book_query_data[1]["Title"],
                    book_query_data[1]["Url"],
                    book_query_data[2]["Title"],
                    book_query_data[2]["Url"])

            message = [  # 串列
                TextSendMessage(text ="📺 Youtube 搜尋結果為: \n\n"+ youtube_text),
                TextSendMessage(text ="📻 Podcast 搜尋結果為: \n\n"+ podcast_text),
                TextSendMessage(text ="📚 書籍 搜尋結果為: \n\n" + book_text,
                                quick_reply=QuickReply(
                                    items=[QuickReplyButton(action=MessageAction(label="其他搜尋", text= "@其他精準搜尋")),
                                           QuickReplyButton(action=MessageAction(label="更多Youtube結果", text= "@更多Youtube")),
                                           QuickReplyButton(action=MessageAction(label="更多Podcast結果", text= "@更多Podcast")),
                                           QuickReplyButton(action=MessageAction(label="更多書籍結果", text="@更多書籍"))]
                                ))
            ]
############################################################################################ 第一次關聯搜尋▼
        elif FUNC_SETTING[0] == '2':   # 將 mtext 拿去做關聯搜尋
            update0_mysql_2(event, mtext_ckip)

            # datafrom 資料來源
            # books => 0
            # youtube => 1
            # podcast => 2
            # top 前n筆高相關

            query = dct.doc2bow(mtext_ckip)
            sim = index[query]
            top = 10
            # if top is None:
            #     top =len(dct)

            ############################################################################################ 第一次關聯搜尋▼書籍
            books_result = [(ti[str(document_number)]['Title'], score, ti[str(document_number)]['Url'])
                            for document_number, score in sorted(enumerate(sim[:3378]),
                                                                 key=lambda x: x[1],
                                                                 reverse=True)[:top] if score > 0.3]

            if len(books_result) < 3:
                try:
                    new_text = [x[0] for x in wordsim.wv.most_similar(mtext_ckip)[:3]]
                    new_query = dct.doc2bow(new_text)
                    new_sim = index[new_query]

                    new_result = [(ti[str(document_number)]['Title'], score, ti[str(document_number)]['Url'])
                                  for document_number, score in sorted(enumerate(new_sim[:3378]),
                                                                       key=lambda x: x[1],
                                                                reverse=True)[:top] if score > 0]
                    for z in new_result:
                        if z[0] in [i[0] for i in books_result]:
                            continue
                        else:
                            books_result.append(z)
                except:
                    pass
            books_result = books_result[0:3]


            ############################################################################################ 第一次關聯搜尋▼youtube
            youtube_result = [(ti[str(document_number + 3378)]['Title'], score, ti[str(document_number + 3378)]['Url'])
                              for document_number, score in sorted(enumerate(sim[3378:6086]),
                                                                   key=lambda x: (x[1], int(ti[str(x[0] + 3378)]['Date'])),
                                                                   reverse=True)[:top] if score > 0.3]

            if len(youtube_result) < 3:
                try:
                    new_text = [x[0] for x in wordsim.wv.most_similar(mtext_ckip)[:3]]
                    new_query = dct.doc2bow(new_text)
                    new_sim = index[new_query]
                    new_result = [(ti[str(document_number + 3378)]['Title'], score, ti[str(document_number + 3378)]['Url'])
                                  for document_number, score in sorted(enumerate(new_sim[3378:6086]),
                                                                       key=lambda x: (x[1], int(ti[str(x[0] + 3378)]['Date'])),
                                                                       reverse=True)[:top] if score > 0]
                    for z in new_result:
                        if z[0] in [i[0] for i in youtube_result]:
                            continue
                        else:
                            youtube_result.append(z)
                except:
                    pass

            youtube_result = youtube_result[0:3]

            ############################################################################################ 第一次關聯搜尋▼podcast

            podcast_result = [(ti[str(document_number + 6086)]['Title'], score, ti[str(document_number + 6086)]['Url'])
                              for document_number, score in sorted(enumerate(sim[6086:]),
                                                                   key=lambda x: (x[1], int(ti[str(x[0] + 6086)]['Date'])),
                                                                   reverse=True)[:top] if score > 0.3]

            if len(podcast_result) < 3:
                try:
                    new_text = [x[0] for x in wordsim.wv.most_similar(mtext_ckip)[:3]]
                    new_query = dct.doc2bow(new_text)
                    new_sim = index[new_query]
                    new_result = [(ti[str(document_number + 5540)]['Title'], score, ti[str(document_number + 5540)]['Url'])
                                  for document_number, score in sorted(enumerate(new_sim[5540:]),
                                                                       key=lambda x: (x[1], int(ti[str(x[0] + 5540)]['Date'])),
                                                                       reverse=True)[:top] if score > 0]
                    for z in new_result:
                        if z[0] in [i[0] for i in podcast_result]:
                            continue
                        else:
                            podcast_result.append(z)
                except:
                    pass

            podcast_result = podcast_result[0:3]

            ## 呈現
            if len(youtube_result) == 0:
                youtube_text = "查無相關結果\n可嘗試其他搜尋方式\n"
            elif len(youtube_result) == 1:
                youtube_text = "{}\n{}".format(
                    youtube_result[0][0],
                    youtube_result[0][2])
            elif len(youtube_result) == 2:
                youtube_text = "{}\n{}\n{}\n{}".format(
                    youtube_result[0][0],
                    youtube_result[0][2],
                    youtube_result[1][0],
                    youtube_result[1][2])
            elif len(youtube_result) == 3:
                youtube_text = "{}\n{}\n{}\n{}\n{}\n{}".format(
                    youtube_result[0][0],
                    youtube_result[0][2],
                    youtube_result[1][0],
                    youtube_result[1][2],
                    youtube_result[2][0],
                    youtube_result[2][2])

            if len(podcast_result) == 0:
                podcast_text = "查無相關結果\n可嘗試其他搜尋方式\n"
            elif len(podcast_result) == 1:
                podcast_text = "{}\n{}".format(
                    podcast_result[0][0],
                    podcast_result[0][2])
            elif len(podcast_result) == 2:
                podcast_text = "{}\n{}\n{}\n{}".format(
                    podcast_result[0][0],
                    podcast_result[0][2],
                    podcast_result[1][0],
                    podcast_result[1][2])
            elif len(podcast_result) == 3:
                podcast_text = "{}\n{}\n{}\n{}\n{}\n{}".format(
                    podcast_result[0][0],
                    podcast_result[0][2],
                    podcast_result[1][0],
                    podcast_result[1][2],
                    podcast_result[2][0],
                    podcast_result[2][2])

            if len(books_result) == 0:
                book_text = "查無相關結果\n可嘗試其他搜尋方式\n"
            elif len(books_result) == 1:
                book_text = "{}\n{}".format(
                    books_result[0][0],
                    books_result[0][2])
            elif len(books_result) == 2:
                book_text = "{}\n{}\n{}\n{}".format(
                    books_result[0][0],
                    books_result[0][2],
                    books_result[1][0],
                    books_result[1][2])
            elif len(books_result) == 3:
                book_text = "{}\n{}\n{}\n{}\n{}\n{}".format(
                    books_result[0][0],
                    books_result[0][2],
                    books_result[1][0],
                    books_result[1][2],
                    books_result[2][0],
                    books_result[2][2])

            message = [  # 串列
                TextSendMessage(text ="📺 Youtube 搜尋結果為: \n\n"+ youtube_text),
                TextSendMessage(text ="📻 Podcast 搜尋結果為: \n\n"+ podcast_text),
                TextSendMessage(text ="📚 書籍 搜尋結果為: \n\n" + book_text,
                                quick_reply=QuickReply(
                                    items=[QuickReplyButton(action=MessageAction(label="其他搜尋", text= "@其他關聯搜尋")),
                                           QuickReplyButton(action=MessageAction(label="更多Youtube結果", text= "@更多Youtube")),
                                           QuickReplyButton(action=MessageAction(label="更多Podcast結果", text= "@更多Podcast")),
                                           QuickReplyButton(action=MessageAction(label="更多書籍結果", text="@更多書籍"))]
                                ))
            ]

            # word_sentence_list_content = ckipword(event, mtext, baseurl)

            # message = TextSendMessage(
            #     text= "youtube結果如下: \n"+ youtube_result[0][0]+ podcast_result[0][0]+ books_result[0][0])

        line_bot_api.reply_message(event.reply_token, message)

        # except:
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))
    #################################################################################################### 第一次關聯搜尋▲

    #################################################################################################### 看更多▼

    elif mtext == "@更多Youtube":  # 當收到@更多Youtube訊息, 讀取資料庫查詢要執行的服務
        try:
            FUNC_SETTING, SEARCH_SETTING, SEARCH_TEXT_RECORD, YT_RECORD, PC_RECORD, BK_RECORD = query_search_record(event)  # 查詢資料庫

            if FUNC_SETTING == '1':    # 將 mtext 做精準搜尋
                NEW_YT_RECORD = YT_RECORD + 1            # 這次的次數等於上次的次數+1
                update_YT_mysql(event, NEW_YT_RECORD)    # 將這次的次數寫回mysql
                youtube_query_data = mongo_youtube_query_re(event, SEARCH_TEXT_RECORD,NEW_YT_RECORD, SEARCH_SETTING)

                if len(youtube_query_data) == 0:
                    youtube_text = "查無相關結果\n可嘗試其他搜尋方式\n"
                elif len(youtube_query_data) == 1:
                    youtube_text = "{}\n{}".format(
                        youtube_query_data[0]["Title"],
                        youtube_query_data[0]["Url"])
                elif len(youtube_query_data) == 2:
                    youtube_text = "{}\n{}\n{}\n{}".format(
                        youtube_query_data[0]["Title"],
                        youtube_query_data[0]["Url"],
                        youtube_query_data[1]["Title"],
                        youtube_query_data[1]["Url"])
                elif len(youtube_query_data) == 3:
                    youtube_text = "{}\n{}\n{}\n{}\n{}\n{}".format(
                        youtube_query_data[0]["Title"],
                        youtube_query_data[0]["Url"],
                        youtube_query_data[1]["Title"],
                        youtube_query_data[1]["Url"],
                        youtube_query_data[2]["Title"],
                        youtube_query_data[2]["Url"])

                message = [  # 串列
                    TextSendMessage(text="📺 Youtube 搜尋結果為: \n\n" + youtube_text,
                                    quick_reply=QuickReply(
                                        items=[QuickReplyButton(action=MessageAction(label="其他搜尋", text="@其他精準搜尋")),
                                               QuickReplyButton(action=MessageAction(label="更多Youtube結果", text="@更多Youtube")),
                                               QuickReplyButton(action=MessageAction(label="更多Podcast結果", text="@更多Podcast")),
                                               QuickReplyButton(action=MessageAction(label="更多書籍結果", text="@更多書籍"))]
                                    ))
                ]

            elif FUNC_SETTING == '2':    # 將 mtext 做精準搜尋
                NEW_YT_RECORD = YT_RECORD + 1            # 這次的次數等於上次的次數+1
                update_YT_mysql(event, NEW_YT_RECORD)    # 將這次的次數寫回mysql
                SEARCH_TEXT_RECORD = SEARCH_TEXT_RECORD.split(' ')

                # datafrom 資料來源
                # books => 0
                # youtube => 1
                # podcast => 2
                # top 前n筆高相關

                query = dct.doc2bow(SEARCH_TEXT_RECORD)
                sim = index[query]
                top = 10
                # if top is None:
                #     top =len(dct)

                youtube_result = [(ti[str(document_number + 3378)]['Title'], score, ti[str(document_number + 3378)]['Url'])
                                  for document_number, score in sorted(enumerate(sim[3378:6086]),
                                                                       key=lambda x: (x[1], int(ti[str(x[0] + 3378)]['Date'])),
                                                                       reverse=True)[:top] if score > 0.3]

                if len(youtube_result) < 3:
                    try:
                        new_text = [x[0] for x in wordsim.wv.most_similar(SEARCH_TEXT_RECORD)[:3]]
                        new_query = dct.doc2bow(new_text)
                        new_sim = index[new_query]
                        new_result = [(ti[str(document_number + 3378)]['Title'], score, ti[str(document_number + 3378)]['Url'])
                                      for document_number, score in sorted(enumerate(new_sim[3378:6086]),
                                                                           key=lambda x: (x[1], int(ti[str(x[0] + 3378)]['Date'])),
                                                                           reverse=True)[:top] if score > 0]
                        for z in new_result:
                            if z[0] in [i[0] for i in youtube_result]:
                                continue
                            else:
                                youtube_result.append(z)
                    except:
                        pass

                youtube_result = youtube_result[NEW_YT_RECORD*3:NEW_YT_RECORD*3+3]

                if len(youtube_result) == 0:
                    youtube_text = "查無相關結果\n可嘗試其他搜尋方式\n"
                elif len(youtube_result) == 1:
                    youtube_text = "{}\n{}".format(
                        youtube_result[0][0],
                        youtube_result[0][2])
                elif len(youtube_result) == 2:
                    youtube_text = "{}\n{}\n{}\n{}".format(
                        youtube_result[0][0],
                        youtube_result[0][2],
                        youtube_result[1][0],
                        youtube_result[1][2])
                elif len(youtube_result) == 3:
                    youtube_text = "{}\n{}\n{}\n{}\n{}\n{}".format(
                        youtube_result[0][0],
                        youtube_result[0][2],
                        youtube_result[1][0],
                        youtube_result[1][2],
                        youtube_result[2][0],
                        youtube_result[2][2])

                message = [  # 串列
                    TextSendMessage(text="📺 Youtube 搜尋結果為: \n\n" + youtube_text,
                                    quick_reply=QuickReply(
                                        items=[QuickReplyButton(action=MessageAction(label="其他搜尋", text="@其他精準搜尋")),
                                               QuickReplyButton(action=MessageAction(label="更多Youtube結果", text="@更多Youtube")),
                                               QuickReplyButton(action=MessageAction(label="更多Podcast結果", text="@更多Podcast")),
                                               QuickReplyButton(action=MessageAction(label="更多書籍結果", text="@更多書籍"))]
                                    ))
                ]

            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext == "@更多Podcast":
        try:
            FUNC_SETTING, SEARCH_SETTING, SEARCH_TEXT_RECORD, YT_RECORD, PC_RECORD, BK_RECORD = query_search_record(event)  # 查詢資料庫

            if FUNC_SETTING == '1':    # 將 mtext 做精準搜尋
                NEW_PC_RECORD = PC_RECORD + 1            # 這次的次數等於上次的次數+1
                update_PC_mysql(event, NEW_PC_RECORD)    # 將這次的次數寫回mysql

                podcast_query_data = mongo_podcast_query_re(event, SEARCH_TEXT_RECORD,NEW_PC_RECORD, SEARCH_SETTING)

                if len(podcast_query_data) == 0:
                    podcast_text = "查無相關結果\n可嘗試其他搜尋方式\n"
                elif len(podcast_query_data) == 1:
                    podcast_text = "{}\n{}".format(
                        podcast_query_data[0]["Title"],
                        podcast_query_data[0]["Url"])
                elif len(podcast_query_data) == 2:
                    podcast_text = "{}\n{}\n{}\n{}".format(
                        podcast_query_data[0]["Title"],
                        podcast_query_data[0]["Url"],
                        podcast_query_data[1]["Title"],
                        podcast_query_data[1]["Url"])
                elif len(podcast_query_data) == 3:
                    podcast_text = "{}\n{}\n{}\n{}\n{}\n{}".format(
                        podcast_query_data[0]["Title"],
                        podcast_query_data[0]["Url"],
                        podcast_query_data[1]["Title"],
                        podcast_query_data[1]["Url"],
                        podcast_query_data[2]["Title"],
                        podcast_query_data[2]["Url"])

                message = [  # 串列
                    TextSendMessage(text="📻 Podcast 搜尋結果為:\n\n" + podcast_text,
                                    quick_reply=QuickReply(
                                        items=[QuickReplyButton(action=MessageAction(label="其他搜尋", text="@其他精準搜尋")),
                                               QuickReplyButton(action=MessageAction(label="更多Youtube結果", text="@更多Youtube")),
                                               QuickReplyButton(action=MessageAction(label="更多Podcast結果", text="@更多Podcast")),
                                               QuickReplyButton(action=MessageAction(label="更多書籍結果", text="@更多書籍"))]
                                    ))
                ]

            elif FUNC_SETTING == '2':    # 將 mtext 做精準搜尋
                NEW_PC_RECORD = PC_RECORD + 1            # 這次的次數等於上次的次數+1
                update_PC_mysql(event, NEW_PC_RECORD)    # 將這次的次數寫回mysql
                SEARCH_TEXT_RECORD = SEARCH_TEXT_RECORD.split(' ')

                # datafrom 資料來源
                # books => 0
                # youtube => 1
                # podcast => 2
                # top 前n筆高相關

                query = dct.doc2bow(SEARCH_TEXT_RECORD)
                sim = index[query]
                top = 10
                # if top is None:
                #     top =len(dct)

                podcast_result = [
                    (ti[str(document_number + 6086)]['Title'], score, ti[str(document_number + 6086)]['Url'])
                    for document_number, score in sorted(enumerate(sim[6086:]),
                                                         key=lambda x: (x[1], int(ti[str(x[0] + 6086)]['Date'])),
                                                         reverse=True)[:top] if score > 0.3]

                if len(podcast_result) < 3:
                    try:
                        new_text = [x[0] for x in wordsim.wv.most_similar(SEARCH_TEXT_RECORD)[:3]]
                        new_query = dct.doc2bow(new_text)
                        new_sim = index[new_query]
                        new_result = [
                            (ti[str(document_number + 6086)]['Title'], score, ti[str(document_number + 6086)]['Url'])
                            for document_number, score in sorted(enumerate(new_sim[6086:]),
                                                                 key=lambda x: (x[1], int(ti[str(x[0] + 6086)]['Date'])),
                                                                 reverse=True)[:top] if score > 0]
                        for z in new_result:
                            if z[0] in [i[0] for i in podcast_result]:
                                continue
                            else:
                                podcast_result.append(z)
                    except:
                        pass

                podcast_result = podcast_result[PC_RECORD*3:PC_RECORD*3+3]

                if len(podcast_result) == 0:
                    podcast_text = "查無相關結果\n可嘗試其他搜尋方式\n"
                elif len(podcast_result) == 1:
                    podcast_text = "{}\n{}".format(
                        podcast_result[0][0],
                        podcast_result[0][2])
                elif len(podcast_result) == 2:
                    podcast_text = "{}\n{}\n{}\n{}".format(
                        podcast_result[0][0],
                        podcast_result[0][2],
                        podcast_result[1][0],
                        podcast_result[1][2])
                elif len(podcast_result) == 3:
                    podcast_text = "{}\n{}\n{}\n{}\n{}\n{}".format(
                        podcast_result[0][0],
                        podcast_result[0][2],
                        podcast_result[1][0],
                        podcast_result[1][2],
                        podcast_result[2][0],
                        podcast_result[2][2])

                message = [  # 串列
                    TextSendMessage(text="📻 Podcast 搜尋結果為:\n\n" + podcast_text,
                                    quick_reply=QuickReply(
                                        items=[QuickReplyButton(action=MessageAction(label="其他搜尋", text="@其他精準搜尋")),
                                               QuickReplyButton(action=MessageAction(label="更多Youtube結果", text="@更多Youtube")),
                                               QuickReplyButton(action=MessageAction(label="更多Podcast結果", text="@更多Podcast")),
                                               QuickReplyButton(action=MessageAction(label="更多書籍結果", text="@更多書籍"))]
                                    ))
                ]


            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext == "@更多書籍":
        try:
            FUNC_SETTING, SEARCH_SETTING, SEARCH_TEXT_RECORD, YT_RECORD, PC_RECORD, BK_RECORD = query_search_record(event)  # 查詢資料庫

            if FUNC_SETTING == '1':    # 將 mtext 做精準搜尋
                NEW_BK_RECORD = BK_RECORD + 1            # 這次的次數等於上次的次數+1
                update_BK_mysql(event, NEW_BK_RECORD)    # 將這次的次數寫回mysql

                book_query_data = mongo_book_query_re(event, SEARCH_TEXT_RECORD,NEW_BK_RECORD, SEARCH_SETTING)

                if len(book_query_data) == 0:
                    book_text = "查無相關結果\n可嘗試其他搜尋方式\n"
                elif len(book_query_data) == 1:
                    book_text = "{}\n{}".format(
                        book_query_data[0]["Title"],
                        book_query_data[0]["Url"])
                elif len(book_query_data) == 2:
                    book_text = "{}\n{}\n{}\n{}".format(
                        book_query_data[0]["Title"],
                        book_query_data[0]["Url"],
                        book_query_data[1]["Title"],
                        book_query_data[1]["Url"])
                elif len(book_query_data) == 3:
                    book_text = "{}\n{}\n{}\n{}\n{}\n{}".format(
                        book_query_data[0]["Title"],
                        book_query_data[0]["Url"],
                        book_query_data[1]["Title"],
                        book_query_data[1]["Url"],
                        book_query_data[2]["Title"],
                        book_query_data[2]["Url"])

                message = [  # 串列
                    TextSendMessage(text="📚 書籍 搜尋結果為: \n\n" + book_text,
                                    quick_reply=QuickReply(
                                        items=[QuickReplyButton(action=MessageAction(label="其他搜尋", text="@其他精準搜尋")),
                                               QuickReplyButton(action=MessageAction(label="更多Youtube結果", text="@更多Youtube")),
                                               QuickReplyButton(action=MessageAction(label="更多Podcast結果", text="@更多Podcast")),
                                               QuickReplyButton(action=MessageAction(label="更多書籍結果", text="@更多書籍"))]
                                    ))
                ]
                line_bot_api.reply_message(event.reply_token, message)

            elif FUNC_SETTING == '2':  # 將 mtext 做精準搜尋
                NEW_BK_RECORD = BK_RECORD + 1  # 這次的次數等於上次的次數+1
                update_BK_mysql(event, NEW_BK_RECORD)  # 將這次的次數寫回mysql
                SEARCH_TEXT_RECORD = SEARCH_TEXT_RECORD.split(' ')

                # datafrom 資料來源
                # books => 0
                # youtube => 1
                # podcast => 2
                # top 前n筆高相關

                query = dct.doc2bow(SEARCH_TEXT_RECORD)
                sim = index[query]
                top = 10
                # if top is None:
                #     top =len(dct)

                books_result = [(ti[str(document_number)]['Title'], score, ti[str(document_number)]['Url'])
                                for document_number, score in sorted(enumerate(sim[:3378]),
                                                                     key=lambda x: x[1],
                                                                     reverse=True)[:top] if score > 0.3]
                if len(books_result) < 3:
                    try:
                        new_text = [x[0] for x in wordsim.wv.most_similar(SEARCH_TEXT_RECORD)[:3]]
                        new_query = dct.doc2bow(new_text)
                        new_sim = index[new_query]

                        new_result = [(ti[str(document_number)]['Title'], score, ti[str(document_number)]['Url'])
                                      for document_number, score in sorted(enumerate(new_sim[:3378]),
                                                                           key=lambda x: x[1],
                                                                           reverse=True)[:top] if score > 0]
                        for z in new_result:
                            if [i[0] for i in books_result]:
                                continue
                            else:
                                books_result.append(z)
                    except:
                        pass

                books_result = books_result[NEW_BK_RECORD*3:NEW_BK_RECORD*3+3]

                if len(books_result) == 0:
                    book_text = "查無相關結果\n可嘗試其他搜尋方式\n"
                elif len(books_result) == 1:
                    book_text = "{}\n{}".format(
                        books_result[0][0],
                        books_result[0][2])
                elif len(books_result) == 2:
                    book_text = "{}\n{}\n{}\n{}".format(
                        books_result[0][0],
                        books_result[0][2],
                        books_result[1][0],
                        books_result[1][2])
                elif len(books_result) == 3:
                    book_text = "{}\n{}\n{}\n{}\n{}\n{}".format(
                        books_result[0][0],
                        books_result[0][2],
                        books_result[1][0],
                        books_result[1][2],
                        books_result[2][0],
                        books_result[2][2])

                message = [  # 串列
                    TextSendMessage(text="📚 書籍 搜尋結果為: \n\n" + book_text,
                                    quick_reply=QuickReply(
                                        items=[QuickReplyButton(action=MessageAction(label="其他搜尋", text="@其他關聯搜尋")),
                                               QuickReplyButton(action=MessageAction(label="更多Youtube結果", text="@更多Youtube")),
                                               QuickReplyButton(action=MessageAction(label="更多Podcast結果", text="@更多Podcast")),
                                               QuickReplyButton(action=MessageAction(label="更多書籍結果", text="@更多書籍"))]
                                    ))
                ]
                line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

    ############################################################################################################# 看更多▲

    elif mtext == '@熱門討論':   # 當收到'@熱門討論', 跳出快速選單, 選項是@+類別
        try:
            message = TextSendMessage(
                text="請選擇類別與區間產出文字雲！",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="政治", text="@政治")),
                        QuickReplyButton(action=MessageAction(label="投資", text="@投資")),
                        QuickReplyButton(action=MessageAction(label="健康", text="@健康")),
                        QuickReplyButton(action=MessageAction(label="公共議題", text="@公共議題")),
                        QuickReplyButton(action=MessageAction(label="商業", text="@商業")),
                        QuickReplyButton(action=MessageAction(label="故事", text="@故事")),
                        QuickReplyButton(action=MessageAction(label="育兒", text="@育兒")),
                        QuickReplyButton(action=MessageAction(label="寵物", text="@寵物")),
                        QuickReplyButton(action=MessageAction(label="小智慧", text="@小智慧")),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext in ['@政治', '@投資', "@健康", "@公共議題", "@商業", "@故事", "@育兒", "@寵物", "@小智慧"]:     # 當收到'@'+類別將再跳出時間區間的快速選單, 最後使用者輸入會變成@+類別+區間+熱點
        try:
            message = TextSendMessage(
                text='請選擇時間區間',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="1周內", text= mtext + "1周內熱點")),
                        QuickReplyButton(action=MessageAction(label="2周內", text= mtext + "2周內熱點")),
                        QuickReplyButton(action=MessageAction(label="1個月內", text= mtext + "1月內熱點")),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext.startswith('@') == True and mtext.endswith('熱點') == True:     # 當收到'@'開頭, '熱點'結尾的文字, 回覆"將提供..."(之後應改為連線資料庫產出文字雲圖示)

        try:
            catalog_num = {'政治':'1', '投資':'2', "健康":'3', "公共議題":'4', "商業":'5', "故事":'6', "育兒":'7', "寵物":'8', "小智慧":'9'}
            time_num = {'1周內熱點':'1','2周內熱點':'2','1月內熱點':'3'}
            photo_num = catalog_num[mtext[1:-5]] + time_num[mtext[-5:]]

            message = [  # 串列
                TextSendMessage(text="以下是" + mtext[1:]+'文字雲:'),
                ImageSendMessage(
                    original_content_url= baseurl + 'cloudphoto/' + photo_num + '.png',
                    preview_image_url= baseurl + 'cloudphoto/' + photo_num + '.png'
                )
            ]

            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

if __name__ == '__main__':
    app.run()
