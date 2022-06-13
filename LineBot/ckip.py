from ckiptagger import construct_dictionary, WS


def ckipword(event, mtext):
    ws = WS('./static/data')
    path_CIS_dict = './static/worddict.txt'
    with open(path_CIS_dict, encoding='utf-8') as f:
        emphasize = f.read().split('\n')

    # 將list轉成dict型態，這邊每個權重都設為1
    dict_for_CKIP = {i: 1 for i in emphasize}

    # construct_dictionary的格式轉換
    dict_for_CKIP = construct_dictionary(dict_for_CKIP)

    word_sentence_list_content = ws([mtext], recommend_dictionary = dict_for_CKIP)  # words in this dictionary are encouraged)
    return word_sentence_list_content




