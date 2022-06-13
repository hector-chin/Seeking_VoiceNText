import pymysql

config = {
}

def query_mysql(event):    # 查詢功能設定
    userid = event.source.user_id

    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql_cmd_1 = "select FUNC_SETTING, SEARCH_SETTING from FUNC where USERID='" + str(userid) + "';"  # sql語法: 從FUNC資料表查詢該使用者ID上次儲存的搜尋功能
    cursor.execute(sql_cmd_1)
    FUNC_SETTING, SEARCH_SETTING= cursor.fetchone()
    db.close()
    return FUNC_SETTING, SEARCH_SETTING



def insert1_mysql(event):   # 當userid不存在, 插入userid, 並設定使用功能為精準搜尋
    userid = event.source.user_id

    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql_cmd_2 = "insert into FUNC (USERID, FUNC_SETTING) values('" + str(userid) + "', '1');"  # 當查詢不到使用者ID資料, 就新增
    cursor.execute(sql_cmd_2)
    db.commit()
    db.close()
    return

def insert2_mysql(event):   # 當userid不存在, 插入userid, 並設定使用功能為關聯搜尋
    userid = event.source.user_id

    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql_cmd_2 = "insert into FUNC (USERID, FUNC_SETTING) values('" + str(userid) + "', '2');"  # 當查詢不到使用者ID資料, 就新增
    cursor.execute(sql_cmd_2)
    db.commit()
    db.close()
    return

def update1_mysql(event):   # 更新設定使用功能為精準搜尋
    userid = event.source.user_id

    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql_cmd_3 = "update FUNC set FUNC_SETTING = '1' where USERID= '" + str(userid) + "';"  #
    cursor.execute(sql_cmd_3)
    db.commit()
    db.close()
    return

def update2_mysql(event):    # 更新設定使用功能為關聯搜尋
    userid = event.source.user_id

    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql_cmd_3 = "update FUNC set FUNC_SETTING = '2' where USERID= '" + str(userid) + "';"  #
    cursor.execute(sql_cmd_3)
    db.commit()
    db.close()
    return

def update3_mysql_title(event):   # 更新設定精準搜尋的範圍為標題
    userid = event.source.user_id

    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql_cmd = "update FUNC set SEARCH_SETTING = '1' where USERID= '" + str(userid) + "';"  #
    cursor.execute(sql_cmd)
    db.commit()
    db.close()
    return

def update3_mysql_content(event):   # 更新設定精準搜尋的範圍為內文
    userid = event.source.user_id

    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql_cmd = "update FUNC set SEARCH_SETTING = '2' where USERID= '" + str(userid) + "';"  #
    cursor.execute(sql_cmd)
    db.commit()
    db.close()
    return

def update3_mysql_all(event):   # 更新設定精準搜尋的範圍為全文
    userid = event.source.user_id

    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql_cmd = "update FUNC set SEARCH_SETTING = '3' where USERID= '" + str(userid) + "';"  #
    cursor.execute(sql_cmd)
    db.commit()
    db.close()
    return

def query_search_record(event):   # 查詢之前搜尋的主題以及次數並回傳
    userid = event.source.user_id

    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql_cmd_4 = "select FUNC_SETTING, SEARCH_SETTING, SEARCH_TEXT_RECORD, YT_RECORD, PC_RECORD, BK_RECORD from FUNC where USERID='" + str(userid) + "';"  # sql語法: 從FUNC資料表查詢該使用者ID上次儲存的搜尋功能
    cursor.execute(sql_cmd_4)
    FUNC_SETTING, SEARCH_SETTING, SEARCH_TEXT_RECORD, YT_RECORD, PC_RECORD, BK_RECORD = cursor.fetchone()
    db.close()
    return FUNC_SETTING, SEARCH_SETTING, SEARCH_TEXT_RECORD, YT_RECORD, PC_RECORD, BK_RECORD

def update0_mysql(event):  # 當次收到文字訊息要搜尋主題, 將主題記錄修改成當次主題, 並修改各類次數紀錄為0
    userid = event.source.user_id
    mtext = event.message.text

    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql_cmd_5 = "update FUNC set SEARCH_TEXT_RECORD='"+mtext+"', YT_RECORD='0', PC_RECORD='0', BK_RECORD='0' where USERID= '" + str(userid) + "';"  #
    cursor.execute(sql_cmd_5)
    db.commit()
    db.close()
    return

def update0_mysql_2(event, mtext_ckip):  # 先斷詞後, 再將主題記錄修改成當次主題, 並修改各類次數紀錄為0
    userid = event.source.user_id
    mtext_ckip_string = ' '.join(mtext_ckip)


    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql_cmd_5 = "update FUNC set SEARCH_TEXT_RECORD='"+mtext_ckip_string+"', YT_RECORD='0', PC_RECORD='0', BK_RECORD='0' where USERID= '" + str(userid) + "';"  #
    cursor.execute(sql_cmd_5)
    db.commit()
    db.close()
    return


def update_YT_mysql(event,NEW_YT_RECORD):  # 當次搜尋主題跟之前相同時, 修改YT次數紀錄為+1
    userid = event.source.user_id

    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql_cmd_6 = "update FUNC set YT_RECORD="+str(NEW_YT_RECORD)+" where USERID= '" + str(userid) + "';"  #
    cursor.execute(sql_cmd_6)
    db.commit()
    db.close()
    return

def update_PC_mysql(event,NEW_PC_RECORD):  # 當次搜尋主題跟之前相同時, 修改PC次數紀錄為+1
    userid = event.source.user_id

    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql_cmd_6 = "update FUNC set PC_RECORD="+str(NEW_PC_RECORD)+" where USERID= '" + str(userid) + "';"  #
    cursor.execute(sql_cmd_6)
    db.commit()
    db.close()
    return

def update_BK_mysql(event,NEW_BK_RECORD):  # 當次搜尋主題跟之前相同時, 修改BK次數紀錄為+1
    userid = event.source.user_id

    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql_cmd_6 = "update FUNC set BK_RECORD="+str(NEW_BK_RECORD)+" where USERID= '" + str(userid) + "';"  #
    cursor.execute(sql_cmd_6)
    db.commit()
    db.close()
    return

