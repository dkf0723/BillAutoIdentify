from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======這裡是呼叫的檔案內容=====
from database import *
from test_check import *
from relevant_information import *
#======python的函數庫==========
import tempfile, os
import datetime
import time
import requests
import datetime

#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
linebotdata = linebotinfo()
# Channel Access Token
line_bot_api = LineBotApi(linebotdata['LineBotApidata'])
# Channel Secret
handler = WebhookHandler(linebotdata['WebhookHandlerdata'])


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
global user_state1
user_state1 = {}
global product
product = {}
global duplicate_save
duplicate_save = {}
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global user_id
    global msg
    msg = event.message.text
    user_id = event.source.user_id 
    if user_id not in user_state:
        user_state[user_id] = 'normal'
    #-------------------確認使用者狀態進行處理----------------------
    #使用者狀態不屬於normal，不允許進行其他動作
    if user_state[user_id] != 'normal':
        check_text = inventory_check()
        line_bot_api.reply_message(event.reply_token, check_text)
    else:
        if '顧客取貨' in msg:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text='取貨選擇',
                template=ConfirmTemplate(
                    text='請選擇取貨方式：\n【手機後三碼】或是【訂單編號】',
                    actions=[
                        MessageAction(
                            label='【後三碼】',
                            text='【取貨】手機後三碼',
                        ),
                        MessageAction(
                            label='【訂單編號】',
                            text='【取貨】訂單編號'
                        )
                    ]
                )
            ))
        elif '【取貨】' in msg:
            if msg[4:] == '手機後三碼':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='顯示顧客購買商品選單'))
            elif msg[4:] == '訂單編號':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='顯示顧客購買商品選單'))
        elif '商品管理' in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='商品管理'))
        elif '未取名單' in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='未取名單'))
        elif '報表管理' in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='報表管理'))
        elif '廠商管理' in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='廠商管理'))
               #-------------------庫存管理及功能選擇按鈕----------------------
        elif '庫存管理' in msg: 
            message = TextSendMessage(text='請點選以下操作功能',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="新增進貨商品", text="新增進貨商品")),
                                    QuickReplyButton(action=MessageAction(label="查詢商品庫存", text="查詢商品庫存")),
                                    QuickReplyButton(action=MessageAction(label="查看進貨紀錄", text="查看進貨紀錄")),
                            ]))
            line_bot_api.reply_message(event.reply_token, message)
            #--------------------------第一分支----------------------------------
        elif '新增進貨商品' in msg:
            send_product_query_menu(event, line_bot_api)
        elif '【商品查詢】' in msg:
            if msg[6:] == '類別':
                send_category_selection(event, line_bot_api)
            elif msg[6:] == '廠商':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='列出所有廠商名稱'))
            else:
                send_product_query_menu(event, line_bot_api)
            #--------------------------第二分支----------------------------------
        elif '查詢商品庫存' in msg:
            send_product_query_menu(event, line_bot_api)
        elif '【商品查詢】' in msg:
            if msg[6:] == '類別':
                send_category_selection(event, line_bot_api)
            elif msg[6:] == '廠商':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='列出所有廠商名稱'))
            else:
                send_product_query_menu(event, line_bot_api)
            #--------------------------第三分支----------------------------------
        elif '查看進貨紀錄' in msg:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text='商品查詢選擇',
                template=ButtonsTemplate(
                    text='請選擇商品查詢方式：',
                    actions=[
                        MessageAction(
                            label='【依類別】',
                            text='【商品查詢】類別',
                        ),
                        MessageAction(
                            label='【依廠商】',
                            text='【商品查詢】廠商'
                        ),
                        MessageAction(
                            label='【依時間】',
                            text='【商品查詢】時間'
                        )
                    ]
                )
            ))
        elif '【商品查詢】' in msg:
            if msg[6:] == '類別':
                send_category_selection(event, line_bot_api)
            elif msg[6:] == '廠商':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='列出所有廠商名稱'))
            elif msg[6:] == '時間':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='列出依照時間範圍所有廠商名稱'))
       
            #-------------------資料庫測試----------------------
        elif '資料庫' in msg:
            databasetest_msg = databasetest()['databasetest_msg']
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='【資料庫連線測試】\n結果：%s' %(databasetest_msg)))
        elif '測試' in msg:
            datasearch = test_datasearch()
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='【資料庫測試】提取資料測試：\n%s' %(datasearch)))
            #-------------------非上方功能的所有回覆----------------------
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text= '您的回覆：「'+msg+'」\n不在功能中！\n請重新輸入。'))
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

def send_product_query_menu(event, line_bot_api):
                message = TemplateSendMessage(
                alt_text='商品查詢選擇',
                template= ButtonsTemplate(
                    text='請選擇商品查詢方式：\n【類別】或是【廠商】',
                    actions=[
                        MessageAction(
                            label='【依類別】',
                            text='【商品查詢】類別',
                        ),
                        MessageAction(
                            label='【依廠商】',
                            text='【商品查詢】廠商'
                        )
                    ]
                )
            )
                line_bot_api.reply_message(event.reply_token, message)
def send_category_selection(event, line_bot_api):
                message = TextSendMessage(text='請點選查詢類別',
                        quick_reply=QuickReply(items=[
                            QuickReplyButton(action=MessageAction(label="冷凍食品", text="frozen")),
                            QuickReplyButton(action=MessageAction(label="日常用品", text="dailyuse")),
                            QuickReplyButton(action=MessageAction(label="甜點", text="dessert")),
                            QuickReplyButton(action=MessageAction(label="地方特產", text="local")),
                            QuickReplyButton(action=MessageAction(label="主食", text="staplefood")),
                            QuickReplyButton(action=MessageAction(label="常溫食品", text="generally")),
                            QuickReplyButton(action=MessageAction(label="美妝保養", text="beauty")),
                            QuickReplyButton(action=MessageAction(label="零食", text="snack")),
                            QuickReplyButton(action=MessageAction(label="保健食品", text="healthy")),
                            QuickReplyButton(action=MessageAction(label="飲品", text="drinks")),
                        ]))
                line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)