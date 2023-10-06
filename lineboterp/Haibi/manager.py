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
from DidnotPickedUp import *
from selection_screen import *
from test import *
#======python的函數庫==========
import tempfile, os
import datetime
import time
import requests

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
global db
db = {}
global list_page
list_page = {}
global queryObject
queryObject = ' '
global orderall
orderall = {}
databasetest()

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
        #-------------------顧客取貨及2種取貨方式列表----------------------
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
            #-------------------商品管理及2種商品狀態列表----------------------
        elif '商品管理' in msg:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text='商品選擇',
            template=ConfirmTemplate(
                    text='請選擇商品狀態：\n【已到貨】或是【未到貨】',
                    actions=[
                        MessageAction(
                            label='【已到貨】',
                            text='【商品】已到貨',
                        ),
                        MessageAction(
                            label='【未到貨】',
                            text='【商品】未到貨'
                        )
                    ]
                )
            ))
        elif '【商品】' in msg:
            if msg[4:] == '已到貨':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='顯示已到貨商品選單'))
            elif msg[4:] == '未到貨':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='顯示未到貨商品選單'))
            #-------------------報表管理----------------------
        elif '報表管理' in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='報表管理'))
            #-------------------顧客QA及2種回覆狀態列表----------------------
        elif '顧客QA' in msg:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text='QA選擇',
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
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='列出未回覆者問題'))
            elif msg[4:] == '未回覆':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='列出歷史問答記錄'))
            #-------------------庫存管理及功能選擇按鈕----------------------
        elif '庫存管理' in msg: 
            message = TextSendMessage(text='請點選以下操作功能',
                                quick_reply=QuickReply(items=[
                                QuickReplyButton(action=MessageAction(label="新增商品", text="新增商品")),
                                QuickReplyButton(action=MessageAction(label="查詢個別商品資訊", text="查詢個別商品資訊")),
                                QuickReplyButton(action=MessageAction(label="查詢所有商品資訊", text="查詢所有商品資訊"))
                        ]))
            line_bot_api.reply_message(event.reply_token, message)
        elif '新增商品' in msg:
            user_state[user_id] = 'adding'
            user_state1[user_id] = 'name'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入品名：'))
        elif '查詢個別商品資訊' in msg:
            #user_state[user_id] = 'searching_oneinf'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入要查詢庫存之品名：'))
        elif '查詢所有商品資訊' in msg:
            #message = select_all_goods()
            message = TextSendMessage(text='查詢所有商品資訊')
            line_bot_api.reply_message(event.reply_token, message)
            #-------------------資料庫測試----------------------
        elif '資料庫' in msg:
            databasetest_msg = databasetest()['databasetest_msg']
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='【資料庫連線測試】\n結果：%s' %(databasetest_msg)))
        elif '測試' in msg:
            datasearch = test_datasearch()
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='【資料庫測試】提取資料測試：\n%s' %(datasearch)))
            

        elif '預購/未取名單' in msg:
            line_bot_api.reply_message(event.reply_token, Order_preorder_selectionscreen())
        elif '【預購名單】列表' in msg:
                queryObject = '預購'
                # querylist = '預購名單'
                show = manager_order_list(queryObject)
                line_bot_api.reply_message(event.reply_token, show)
        elif '【未取名單】列表' in msg:
                queryObject = '未取'
                # querylist = '未取名單'
                show = manager_order_list(queryObject)
                line_bot_api.reply_message(event.reply_token, show)
        elif '【訂單詳細】' in msg:
            msg = str(msg)
            orderall[user_id+'dt'] = msg[-18:]
            searchresult = orderdtsearch()
            line_bot_api.reply_message(event.reply_token, searchresult)
            #-------------------庫存查詢----------------------
        elif '庫存查詢' in msg:
            list_page[user_id+'庫存min'] = 0
            list_page[user_id+'庫存max'] = 9
            show = manager_inquiry_list()
            line_bot_api.reply_message(event.reply_token, show)
            #-------------------報表查詢----------------------
        elif '報表查詢' in msg:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text='報表選擇',
            template=ConfirmTemplate(
                    text='請選擇報表',
                    actions=[
                            MessageAction(
                                label='【累積銷售】',
                                text='【累積銷售】報表'
                            )
                    ]
                )
            ))
        elif '累積銷售' in msg:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text='範圍選擇',
            template=ConfirmTemplate(
                    text='請選擇範圍',
                    actions=[
                            MessageAction(
                                label='【當月】',
                                text='【月】報表'
                            ),
                            MessageAction(
                                label='【當季】',
                                text='【季】報表'
                            )
                    ]
                )
            ))
        elif '【月】報表' in msg:
                queryObject = '月' #取當月
                # show = manager_order_list(queryObject)
                # line_bot_api.reply_message(event.reply_token, show)
        elif '【季】報表' in msg:
                queryObject = '季' #取當季
                # show = manager_order_list(queryObject)
                # line_bot_api.reply_message(event.reply_token, show) 
        elif '【年】報表' in msg:
                queryObject = '年' #取當年
                # show = manager_order_list(queryObject)
                # line_bot_api.reply_message(event.reply_token, show)  
        #      
        elif 'id搜尋' in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='結果：%s' %(user_id)))
        elif '發送' in msg:
            show = testshow()
            line_bot_api.reply_message(event.reply_token, show)
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
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
