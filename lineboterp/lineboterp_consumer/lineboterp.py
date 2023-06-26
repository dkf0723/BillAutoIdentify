from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======這裡是呼叫的檔案內容=====
from product.product_preorder import *
from product.buy_now import *
from product.check import *

#======python的函數庫==========
import tempfile, os
import datetime
import time
import requests

#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('2+5H1PGPxcuiHvmd4OJ6aa9w0//wo1Q1XhXX9dx/AT9I3e+u4nEUedXpclarLzV2k3kQ6uoqjfGUnZ+rqCGgt8yrcMUw58r9DREQslLPxWvb03oxdf2AseFYzpdCeWRykWIfjpbcBB2o8LrTzP2LTQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('cc36511a908df2f50e98845cbd8216aa')


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
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global user_id
    global msg
    msg = event.message.text
    user_id = event.source.user_id 
    #-------------------團購商品及2種商品列表----------------------
    if '團購商品' in msg:
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
        alt_text='ConfirmTemplate',
        template=ConfirmTemplate(
                text='請選擇商品狀態：\n【預購商品】或是【現購商品】',
                actions=[
                    MessageAction(
                        label='【預購商品】',
                        text='【預購商品】列表'
                    ),
                    MessageAction(
                        label='【現購商品】',
                        text='【現購商品】列表'
                    )
                ]
            )
        ))
    elif '【預購商品】列表' in msg:
        product_show = product_preorder_list()
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(
        alt_text='【預購商品】列表',
        contents={
            "type": "carousel",
            "contents": product_show      
            } 
        ))
    elif '【現購商品】列表' in msg:
        product_show = product_buynow_list()
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(
        alt_text='【現購商品】列表',
        contents={
            "type": "carousel",
            "contents": product_show      
            } 
        ))
    #-------------------0----------------------
    elif '訂單查詢' in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='訂單查詢'))
    elif '營業資訊' in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='營業資訊'))
    elif '商品廠家' in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='商品廠家'))
    #-------------------執行購買或預購----------------------
    elif '【立即購買】' in msg:
        product['product'] = msg[6:]
        Order_buynow_text = Order_buynow()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=Order_buynow_text))
    elif '【手刀預購】' in msg:
        product['product'] = msg[6:]
        Order_preorder_text = Order_preorder()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=Order_preorder_text))
    #-------------------檢查購買或預購數量----------------------
    elif user_state[user_id] != 'normal':
        check_text = product_check()
        line_bot_api.reply_message(event.reply_token, check_text)
    elif '【加入購物車】' in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='【加入購物車】'))
    elif '查看購物車' in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='查看購物車'))
    #-------------------非上方功能的所有回覆----------------------
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text= '您的問題：\n「'+msg+'」\n無法立即回覆！\n已將問題發送至客服人員，請稍後！'))
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
