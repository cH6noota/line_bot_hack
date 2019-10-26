from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import os
import json
 
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
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=new))#["source"]["userId"]) )
     


    
if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)

 
