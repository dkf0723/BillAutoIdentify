from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======這裡是呼叫的檔案內容=====
from inventory import *

#======python的函數庫==========
import tempfile, os
import datetime
import time
import requests

#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('J7jADxRSi/3p4vlG5H9lqvFqZgKcdU5aceIQMGAuNF8oemiPxX1JgpBYi1Js8KXci2NfFnT2DuXzyHFFPS5/3OQaWZYVbxFMqjDTBDc4dAieb4Q3bvvLQn3B45bCYZfSEm/2ozasOtrDTcsV5hrcDAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('7bba6e253457f394cb56d7e4b7adfc39')


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


#-------------------儲存使用者狀態----------------------
global user_state
user_state = {}
global product
product = {}
global dict_data
dict_data = {}
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global user_id
    global msg
    msg = event.message.text
    user_id = event.source.user_id 

    if '顧客取貨' in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='顧客取貨'))
    elif '商品管理' in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='商品管理'))
    elif '未取名單' in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='未取名單'))
    elif '報表管理' in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='報表管理'))
    elif '顧客QA' in msg:
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
        alt_text='ConfirmTemplate',
        template=ConfirmTemplate(
                text='請選擇查詢顧客QA回覆狀態：\n【已回覆】或是【未回覆】',
                actions=[
                    MessageAction(
                        label='【已回覆】',
                        text='【QA】已回覆',
                    ),
                    MessageAction(
                        label='【未回覆】',
                        text='【QA】未回覆'
                    )
                ]
            )
        ))
    elif '【QA】' in msg:
        if msg[4:] == '已回覆':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='已回覆'))
        elif msg[4:] == '未回覆':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='未回覆'))
    elif '庫存管理' in msg: 
        message = TextSendMessage(text='請點選以下操作功能',
                            quick_reply=QuickReply(items=[
                            QuickReplyButton(action=MessageAction(label="新增商品", text="新增商品")),
                            QuickReplyButton(action=MessageAction(label="出售商品", text="出售商品")),
                            QuickReplyButton(action=MessageAction(label="查詢個別商品資訊", text="查詢個別商品資訊")),
                            QuickReplyButton(action=MessageAction(label="查詢所有商品資訊", text="查詢所有商品資訊")),
                    ]))
        line_bot_api.reply_message(event.reply_token, message)
    elif '新增商品' in msg:
        message = add_goods()
        line_bot_api.reply_message(event.reply_token, message)
    elif '出售商品' in msg:
        message = sell_goods()
        line_bot_api.reply_message(event.reply_token, message)
    elif '查詢個別商品資訊' in msg:
        message = select_goods()
        line_bot_api.reply_message(event.reply_token, message)
    elif '查詢所有商品資訊' in msg:
        message = select_all_goods()
        line_bot_api.reply_message(event.reply_token, message)

    #-------------------非上方功能的所有回覆----------------------
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text= '您的回覆：「'+msg+'」\n不在功能編號中！\n請重新輸入。'))
    #return user_id,user_state


@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)