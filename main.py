from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage,PostbackEvent
import os
import json
from funcs import id_check_func ,talk_func ,show_database,csv_date,db_write ,checker
import pandas as pd
import requests
import datetime

app=Flask(__name__)
#環境変数の取得
YOUR_CHANNEL_ACCESS_TOKEN="zwG2YHzlm8WNyiL1+uApTaUfqplmKV5lWrY/h/yxotjecGtli0p6LeuvG7oygEgVriAq/HsAxs0jwSSSj08/En3DH8yWeSWe5/5PBcMqhXDSe6xJBpDRuMyW35afkhu7+gT/jEbzSN7b95jA01hMWQdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET="901848e5ad6dc80b58b18ed866f44b27"
line_bot_api=LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback",methods=["POST"])
def callback():
    signature=request.headers["X-Line-Signature"]
    
    body=request.get_data(as_text=True)
    app.logger.info("Request body"+body)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return "ok"

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    texx=str(event)
    new = json.loads(texx)
    #repl ユーザid　取得
    line_user_id = new["source"]["userId"]
    app_id = id_check_func(line_user_id)
    # 会話を取得
    send_message = talk_func(line_user_id,app_id,new["message"]["text"])
    if send_message !="non":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=send_message))

@handler.add(PostbackEvent)
def handle_post(event):
    texx=str(event)
    new = json.loads(texx)
    if new["postback"]["data"]=="action=first":
        now = datetime.datetime.now() + datetime.timedelta(hours=-13)
        r_d=datetime.datetime.strptime(new["postback"]["params"]["date"], '%Y-%m-%d')
        if r_d >=now:
            date= '"'+new["postback"]["params"]["date"]+'"'
            line_user_id=new["source"]["userId"]
            csv_date(new["postback"]["params"]["date"], line_user_id)

            place=pd.read_csv("http://ik1-334-27288.vs.sakura.ne.jp/hack10/form/"+line_user_id+".csv" ,encoding="UTF").columns[0]
            #時刻と場所から今の予約情報をメッセージに
            x3={ "type": "flex", "altText": "Flex Message", "contents": { "type": "bubble", "direction": "ltr", "header": { "type": "box", "layout": "vertical", "contents": [ { "type": "text", "text": "時刻を選択して下さい", "align": "center", "color": "#221815" } ] }, "footer": { "type": "box", "layout": "horizontal", "contents": [ { "type": "button", "action": { "type":"datetimepicker", "label":"時刻を選択", "data":"action=second", "mode":"time" },"color": "#E5370A", "height": "md", "style": "primary" } ] } } }
            x2=show_database(date, place)
            x1={'type': 'text', 'text':"以下の時間で予約可能です"}
            url="https://api.line.me/v2/bot/message/push"
            token="Bearer zwG2YHzlm8WNyiL1+uApTaUfqplmKV5lWrY/h/yxotjecGtli0p6LeuvG7oygEgVriAq/HsAxs0jwSSSj08/En3DH8yWeSWe5/5PBcMqhXDSe6xJBpDRuMyW35afkhu7+gT/jEbzSN7b95jA01hMWQdB04t89/1O/w1cDnyilFU="
            head = {"Content-Type": "application/json","Authorization" :token }
            r = requests.post(url,headers =head ,json={'to':line_user_id ,'messages':[x1,x2,x3]})
        else :
            url="https://api.line.me/v2/bot/message/push"
            line_user_id=new["source"]["userId"]
            token="Bearer zwG2YHzlm8WNyiL1+uApTaUfqplmKV5lWrY/h/yxotjecGtli0p6LeuvG7oygEgVriAq/HsAxs0jwSSSj08/En3DH8yWeSWe5/5PBcMqhXDSe6xJBpDRuMyW35afkhu7+gT/jEbzSN7b95jA01hMWQdB04t89/1O/w1cDnyilFU="
            head = {"Content-Type": "application/json","Authorization" :token } 
            x1={ "type": "text", "text": "正しい日付を選択してください" }
            x2={ "type": "flex", "altText": "Flex Message", "contents": { "type": "bubble", "direction": "ltr", "header": { "type": "box", "layout": "vertical", "contents": [ { "type": "text", "text": "日付を選択してください", "align": "center", "color": "#221815" } ] }, "footer": { "type": "box", "layout": "horizontal", "contents": [ { "type": "button", "action": { "type":"datetimepicker", "label":"日付を選択", "data":"action=first", "mode":"date" },"color": "#E5370A", "height": "md", "style": "primary" } ] } } }
            r = requests.post(url,headers =head ,json={'to':line_user_id ,'messages':[x1,x2]})

    elif new["postback"]["data"]=="action=second":

        line_user_id=new["source"]["userId"]
        tt=new["postback"]["params"]["time"]
        place=pd.read_csv("http://ik1-334-27288.vs.sakura.ne.jp/hack10/form/"+line_user_id+".csv" ,encoding="UTF").columns[0]
        date =pd.read_csv("http://ik1-334-27288.vs.sakura.ne.jp/hack10/form/"+line_user_id+".csv" ,encoding="UTF").columns[1]
        if checker(datetime.datetime.strptime(tt, '%H:%M').strftime('%H') ,date,place ):
            tt = datetime.datetime.strptime(tt, '%H:%M').strftime('%H:00')
            #DB 書き込み
            db_write(line_user_id,place ,date,tt)
            #予約かくにんメッセ
            y={ "type": "flex", "altText": "Flex Message", "contents": { "type": "bubble", "direction": "ltr", "hero": { "type": "image", "url": "https://kn46itblog.com/static/yoyaku.png", "size": "full", "aspectRatio": "20:13", "aspectMode": "fit" }, "body": { "type": "box", "layout": "vertical", "contents": [ { "type": "box", "layout": "vertical", "contents": [ { "type": "text", "text": "ご予約ありがとうございます。", "margin": "xl", "align": "start", "gravity": "top", "color": "#E5370A" }, { "type": "spacer" } ] }, { "type": "text", "text": "ピカチュウとお話ししましょう！", "align": "start", "weight": "bold" }, { "type": "separator", "margin": "md", "color": "#D8D7D6" }, { "type": "box", "layout": "horizontal", "margin": "lg", "contents": [ { "type": "text", "text": date, "margin": "xxl", "color": "#969696" }, { "type": "text", "text": tt, "margin": "xl", "align": "end", "color": "#969696" } ] } ] } } }
            url="https://api.line.me/v2/bot/message/push"
            token="Bearer zwG2YHzlm8WNyiL1+uApTaUfqplmKV5lWrY/h/yxotjecGtli0p6LeuvG7oygEgVriAq/HsAxs0jwSSSj08/En3DH8yWeSWe5/5PBcMqhXDSe6xJBpDRuMyW35afkhu7+gT/jEbzSN7b95jA01hMWQdB04t89/1O/w1cDnyilFU="
            head = {"Content-Type": "application/json","Authorization" :token }
            r = requests.post(url,headers =head ,json={'to':line_user_id,'messages':[y]}) 
        else:
            url="https://api.line.me/v2/bot/message/push"
            line_user_id=new["source"]["userId"]
            token="Bearer zwG2YHzlm8WNyiL1+uApTaUfqplmKV5lWrY/h/yxotjecGtli0p6LeuvG7oygEgVriAq/HsAxs0jwSSSj08/En3DH8yWeSWe5/5PBcMqhXDSe6xJBpDRuMyW35afkhu7+gT/jEbzSN7b95jA01hMWQdB04t89/1O/w1cDnyilFU="
            x1={ "type": "text", "text": "その時間では予約はできません" }
            date= '"'+date+'"'
            x2=show_database(date, place)
            x3={ "type": "flex", "altText": "Flex Message", "contents": { "type": "bubble", "direction": "ltr", "header": { "type": "box", "layout": "vertical", "contents": [ { "type": "text", "text": "時刻を選択して下さい", "align": "center", "color": "#221815" } ] }, "footer": { "type": "box", "layout": "horizontal", "contents": [ { "type": "button", "action": { "type":"datetimepicker", "label":"時刻を選択", "data":"action=second", "mode":"time" },"color": "#E5370A", "height": "md", "style": "primary" } ] } } }
            head = {"Content-Type": "application/json","Authorization" :token }
            r = requests.post(url,headers =head ,json={'to':line_user_id ,'messages':[x1,x2,x3]})

    
if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)

