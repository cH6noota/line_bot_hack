import pandas as pd
import requests
import json

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
    if data=="場所_ok":
        #一時保管用 CSV
        url ="http://ik1-334-27288.vs.sakura.ne.jp/hack10/form/form_data1.php?line_user_id="+line_user_id+"&plase="+message
        r = requests.get(url)
        return "場所の入力が完了しました"
    elif data=="時間_ok":
        url ="http://ik1-334-27288.vs.sakura.ne.jp/hack10/form/form_data1.php?line_user_id="+line_user_id+"&date="+message
        r = requests.get(url)
        return "時間"
    else:
        return "ok"

def show_database(get_date):
    date=get_date


    


