import pandas as pd
import requests
import json
import pymysql.cursors





def id_check_func(line_user_id):
    df = pd.read_csv("http://ik1-334-27288.vs.sakura.ne.jp/hack10/user_data.csv",encoding="SHIFT-JIS")
    i=0
    for x in df["line_id"]:
        if line_user_id == x  :
            return df["repl_id"][i]
        i=i+1
    apikey="z1frsJuv5oyEjoFYiHTPQP79WZvthvysGEAQ24bW"
    url = "https://api.repl-ai.jp/v1/registration"
    header={"Content-Type":"application/json", "x-api-key":apikey}
    body = {'botId':'sample'}
    r = requests.post(url,headers=header, json=body)
    appUserId = json.loads(r.text)['appUserId']
    url ="http://ik1-334-27288.vs.sakura.ne.jp/hack10/test.php?line_user_id="+line_user_id+"&appUserId="+appUserId
    r = requests.get(url)
    return appUserId
def talk_func(line_user_id, appUserId , message):
    

    url="https://api.repl-ai.jp/v1/dialogue"
    apikey="z1frsJuv5oyEjoFYiHTPQP79WZvthvysGEAQ24bW"

    header={"Content-Type":"application/json", "x-api-key":apikey}
    body = {"appUserId":appUserId , 'botId':'sample' ,"voiceText": message, "initTalkingFlag":False ,"initTopicId":"s4vycabs2zko0dk" }

    r = requests.post(url,headers=header, json=body)
    data = json.loads(r.text)["systemText"]['expression']
    if len(data.split("%%"))>1:
        data=data.split("%%")
        send=""
        for i in data:
            if send=="":
                send=send+i
            else:
                send=send+"\n"+i
        return send
    if data=="場所ok":
        #一時保管用 CSV
        url ="http://ik1-334-27288.vs.sakura.ne.jp/hack10/form/form_data1.php?line_user_id="+line_user_id+"&plase="+message
        r = requests.get(url)
        url="https://api.line.me/v2/bot/message/push"
        token="Bearer zwG2YHzlm8WNyiL1+uApTaUfqplmKV5lWrY/h/yxotjecGtli0p6LeuvG7oygEgVriAq/HsAxs0jwSSSj08/En3DH8yWeSWe5/5PBcMqhXDSe6xJBpDRuMyW35afkhu7+gT/jEbzSN7b95jA01hMWQdB04t89/1O/w1cDnyilFU="
        head = {"Content-Type": "application/json","Authorization" :token } 
        x1=x={ "type": "text", "text": "地点登録が完了しました" }
        x2={ "type": "flex", "altText": "Flex Message", "contents": { "type": "bubble", "direction": "ltr", "header": { "type": "box", "layout": "vertical", "contents": [ { "type": "text", "text": "Header", "align": "center" } ] }, "footer": { "type": "box", "layout": "horizontal", "contents": [ { "type": "button", "action": { "type":"datetimepicker", "label":"Select date", "data":"action=date", "mode":"date" } } ] } } }
        r = requests.post(url,headers =head ,json={'to':line_user_id ,'messages':[x1,x2]})
        return "non"
    elif data=="ここで予約情報表示":
        url ="http://ik1-334-27288.vs.sakura.ne.jp/hack10/form/form_data2.php?line_user_id="+line_user_id+"&date=test"
        r = requests.get(url)
        return "時間"
    elif data=="予約ok":
        #場所選択のメッセージ
        url="https://api.line.me/v2/bot/message/push"
        token="Bearer zwG2YHzlm8WNyiL1+uApTaUfqplmKV5lWrY/h/yxotjecGtli0p6LeuvG7oygEgVriAq/HsAxs0jwSSSj08/En3DH8yWeSWe5/5PBcMqhXDSe6xJBpDRuMyW35afkhu7+gT/jEbzSN7b95jA01hMWQdB04t89/1O/w1cDnyilFU="
        head = {"Content-Type": "application/json","Authorization" :token } 
        #yを可変にする
        y={ "type": "template", "altText": "this is a buttons template", "template": { "type": "buttons", "actions": [ { "type": "message", "label": "中央区", "text": "中央区" }, { "type": "message", "label": "北区", "text": "北区" }, { "type": "message", "label": "東区", "text": "東区" }, { "type": "message", "label": "南区", "text": "南区" } ], "title": "避難場所確認", "text": "避難場所を選択してください" } }
        r = requests.post(url,headers =head ,json={'to':line_user_id ,'messages':[y]})
        return "non"

    else:
        return "テストok"

def show_database(date,place):
    """conn = pymysql.connect(
    host='153.126.197.42',
    user='testuser',
    password='knct0wireless',
    db='kumamon5',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:
            sql = "SELECT res_time FROM pre_reserve where res_date =" + date + " and place =" + place
            cursor.execute(sql, ())
            result = cursor.fetchall()
            send=""
            for r in result:
                if send=="":
                    send=r['res_time']
                else:
                    send=send+"\n"+r['res_time']
            return send
    finally:
        conn.close()"""
    return place


    


