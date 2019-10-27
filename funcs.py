import pandas as pd
import requests
import json
import pymysql.cursors
import datetime
import random


def create_pass(line_user_id):
    passwd = str(random.randint(1000000,3000000))[1:4]
    #サーバにget書き込み
    url ="http://ik1-334-27288.vs.sakura.ne.jp/hack10/pass/pass.php?line_user_id="+line_user_id+"&passwd="+passwd
    r = requests.get(url)
    return passwd

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
        x1={ "type": "text", "text": "地点登録が完了しました" }
        x2={ "type": "flex", "altText": "Flex Message", "contents": { "type": "bubble", "direction": "ltr", "header": { "type": "box", "layout": "vertical", "contents": [ { "type": "text", "text": "日付を選択してください", "align": "center", "color": "#221815" } ] }, "footer": { "type": "box", "layout": "horizontal", "contents": [ { "type": "button", "action": { "type":"datetimepicker", "label":"日付を選択", "data":"action=first", "mode":"date" },"color": "#E5370A", "height": "md", "style": "primary" } ] } } }
        r = requests.post(url,headers =head ,json={'to':line_user_id ,'messages':[x1,x2]})
        return "non"
    elif data=="予約ok":
        #場所選択のメッセージ
        url="https://api.line.me/v2/bot/message/push"
        token="Bearer zwG2YHzlm8WNyiL1+uApTaUfqplmKV5lWrY/h/yxotjecGtli0p6LeuvG7oygEgVriAq/HsAxs0jwSSSj08/En3DH8yWeSWe5/5PBcMqhXDSe6xJBpDRuMyW35afkhu7+gT/jEbzSN7b95jA01hMWQdB04t89/1O/w1cDnyilFU="
        head = {"Content-Type": "application/json","Authorization" :token } 
        #yを可変にする
        y={ "type": "template", "altText": "this is a buttons template", "template": { "type": "buttons", "actions": [ { "type": "message", "label": "中央区", "text": "21" }, { "type": "message", "label": "北区", "text": "21" }, { "type": "message", "label": "東区", "text": "21" }, { "type": "message", "label": "南区", "text": "21" } ], "title": "避難場所確認", "text": "避難場所を選択してください" } }
        r = requests.post(url,headers =head ,json={'to':line_user_id ,'messages':[y]})
        return "non"
    elif data=="dbwrite":
        url ="http://ik1-334-27288.vs.sakura.ne.jp/hack10/final_insert.php"
        r = requests.get(url)
        x=create_pass(line_user_id)
        url="https://api.line.me/v2/bot/message/push"
        token="Bearer zwG2YHzlm8WNyiL1+uApTaUfqplmKV5lWrY/h/yxotjecGtli0p6LeuvG7oygEgVriAq/HsAxs0jwSSSj08/En3DH8yWeSWe5/5PBcMqhXDSe6xJBpDRuMyW35afkhu7+gT/jEbzSN7b95jA01hMWQdB04t89/1O/w1cDnyilFU="
        head = {"Content-Type": "application/json","Authorization" :token }
        xx={ "type": "text", "text": "パスワードはこの数字です\n"+x }
        r = requests.post(url,headers =head ,json={'to':line_user_id ,'messages':[xx]})
    elif data=="nayami":
        url="https://api.line.me/v2/bot/message/push"
        token="Bearer zwG2YHzlm8WNyiL1+uApTaUfqplmKV5lWrY/h/yxotjecGtli0p6LeuvG7oygEgVriAq/HsAxs0jwSSSj08/En3DH8yWeSWe5/5PBcMqhXDSe6xJBpDRuMyW35afkhu7+gT/jEbzSN7b95jA01hMWQdB04t89/1O/w1cDnyilFU="
        head = {"Content-Type": "application/json","Authorization" :token }
        xx={ "type": "text", "text": "お悩みをメッセージでください" }
        r = requests.post(url,headers =head ,json={'to':line_user_id ,'messages':[xx]})
    elif data=="nayami_get": 
        url="https://api.line.me/v2/bot/message/push"
        token="Bearer zwG2YHzlm8WNyiL1+uApTaUfqplmKV5lWrY/h/yxotjecGtli0p6LeuvG7oygEgVriAq/HsAxs0jwSSSj08/En3DH8yWeSWe5/5PBcMqhXDSe6xJBpDRuMyW35afkhu7+gT/jEbzSN7b95jA01hMWQdB04t89/1O/w1cDnyilFU="
        head = {"Content-Type": "application/json","Authorization" :token }
        xx={ "type": "text", "text": "ありがとうございます。\nこの情報は皆様の支援のために利用されます。" }
        r = requests.post(url,headers =head ,json={'to':line_user_id ,'messages':[xx]})
        mental_db(message,line_user_id, 21)
    else:
        return "テストok"

def show_database(date,place):
    conn = pymysql.connect(
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
            box=""
            h_list=[]
            ans =[]
            for r in result:
                t = datetime.datetime.strptime(r['res_time'], '%H:%M')
                h_list.append(t.hour)
            print(h_list)
            #8時以降
            for i in range(8,20):
                flag=True
                for j in h_list:
                        if j==i+1:
                                flag=False
                if flag:
                        x=str(i+1)+":00"
                        ans.append(x)
            for h in ans:
                if box=="":
                        box=box+h
                else:
                        box=box+"\n"+h
            x={ "type": "text", "text": box}
            return x


    finally:
        conn.close()

def csv_date(date, line_user_id):
    url ="http://ik1-334-27288.vs.sakura.ne.jp/hack10/form/form_data2.php?line_user_id="+line_user_id+"&date="+date
    r = requests.get(url)


def db_write (line_user_id, place ,date,tt):
    conn = pymysql.connect(
        host='153.126.197.42',
        user='testuser',
        password='knct0wireless',
        db='kumamon5',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO pre_reserve (user_id,  place, res_date,res_time) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (line_user_id, place, date, tt))
        conn.commit()
    finally:
        conn.close()

def mental_db(message ,line_user_id ,place):
    conn = pymysql.connect(
        host='153.126.197.42',
        user='testuser',
        password='knct0wireless',
        db='kumamon5',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO mental_data (user_id, message, place) VALUES (%s, %s, %s)"
            cursor.execute(sql, (line_user_id, message ,place))
        conn.commit()
    finally:
        conn.close()

def checker(num ,date ,place):
    num=int(num)
    if num==0 or num==1 or num==2 or num==3 or num==4 or num==5 or num==6 or num==7 or num==8 or num==21 or num==22 or num==23:
        return False
    conn = pymysql.connect(
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
            box=""
            h_list=[]
            ans =[]
            for r in result:
                t = datetime.datetime.strptime(r['res_time'], '%H:%M')
                h_list.append(t.hour)
            for h in h_list:
                if h==str(num):
                    return False
    finally:
        conn.close()
        return True



