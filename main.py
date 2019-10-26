from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage,PostbackEvent
import os
import json
from funcs import id_check_func ,talk_func ,show_database
import pandas as pd
import requests

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
    return "OK"

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
        date= '"'+new["postback"]["params"]["date"]+'"'
        line_user_id=new["source"]["userId"]
        place=pd.read_csv("http://ik1-334-27288.vs.sakura.ne.jp/hack10/form/"+line_user_id+".csv" ,encoding="UTF").columns[0]
        #時刻と場所から今の予約情報をメッセージに
        x3={ "type": "flex", "altText": "Flex Message", "contents": { "type": "bubble", "direction": "ltr", "header": { "type": "box", "layout": "vertical", "contents": [ { "type": "text", "text": "時刻を選択して 下さい", "align": "center" } ] }, "footer": { "type": "box", "layout": "horizontal", "contents": [ { "type": "button", "action": { "type":"datetimepicker", "label":"Select date", "data":"action=second", "mode":"time" } } ] } } }
        x2=show_database(date, place)
        x1={'type': 'text', 'text':"以下の時間で予約可能です"}
        url="https://api.line.me/v2/bot/message/push"
        token="Bearer zwG2YHzlm8WNyiL1+uApTaUfqplmKV5lWrY/h/yxotjecGtli0p6LeuvG7oygEgVriAq/HsAxs0jwSSSj08/En3DH8yWeSWe5/5PBcMqhXDSe6xJBpDRuMyW35afkhu7+gT/jEbzSN7b95jA01hMWQdB04t89/1O/w1cDnyilFU="
        head = {"Content-Type": "application/json","Authorization" :token }
        r = requests.post(url,headers =head ,json={'to':line_user_id ,'messages':[x1,x2,x3]})
        
    elif new["postback"]["data"]=="action=second":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=texx))
        #DB 書き込み


    
if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)

