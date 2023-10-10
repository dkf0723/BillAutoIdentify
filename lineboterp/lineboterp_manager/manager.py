from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from linebot.models import TextSendMessage
#======這裡是呼叫的檔案內容=====
from flexmsg import *
from database import *
#from repurinf import *
from relevant_information import linebotinfo,dbinfo
from nepurinf import *
#from pdf_utils import create_pdf
#======python的函式庫==========
from mysql.connector import pooling
import tempfile, os
from datetime import datetime, timedelta
import schedule #排程
import threading #排程執行緒
from apscheduler.schedulers.background import BackgroundScheduler#另一種排程
import time
import logging
import requests
import string #字符串處理相關的工具
import random #隨機產生
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
global db
db = {}

#資料庫pool設定數量4個
dbdata = dbinfo()
db_pool = pooling.MySQLConnectionPool(
            pool_name="db_pool",
            pool_size=4,
            host= dbdata['host'],
            user=dbdata['user'],
            password=dbdata['password'],
            database=dbdata['database']
        )

#首次資料庫連線，最底下有排程設定
databasetest(db_pool,1) #主要1
databasetest(db_pool,2) #備用1
#-----------------------------------------

# 處理訊息
user_state = {}

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
        check_text = purchase_check()
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
        #--------商品管理----------------#           
        elif '商品管理' in msg:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text='查詢選擇',
                template=ButtonsTemplate(
                    text='請選擇商品服務：\n【查詢/修改/下架】或是【新增上架】',
                    actions=[
                        MessageAction(
                            label='【查詢/修改/下架】',
                            text='【查詢/修改/下架】',
                        ),
                        MessageAction(
                            label='【新增上架】',
                            text='【新增上架】'
                        )
                    ]
                )
            ))
        elif '【查詢/修改/下架】' in msg:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text='查詢選擇',
                template=ButtonsTemplate(
                    text='請選擇商品查詢方式：\n【依類別】或是【依廠商】',
                    actions=[
                        MessageAction(
                            label='【依類別】',
                            text='【依類別】查詢',
                        ),
                        MessageAction(
                            label='【依廠商】',
                            text='【依廠商】查詢',
                        )
                    ]
                )
            ))
        elif '【依類別】查詢' in msg:
                send_category_selection(event, line_bot_api)
                line_bot_api.reply_message(event.reply_token, message)    
        elif '【新增上架】' in msg:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text='查詢選擇',
                template=ButtonsTemplate(
                    text='請先選擇廠商：\n【舊廠商】或是【新廠商】',
                    actions=[
                        MessageAction(
                            label='【舊廠商】',
                            text='【舊廠商】',
                        ),
                        MessageAction(
                            label='【新廠商】',
                            text='【新廠商】',
                        )
                    ]
                )
            ))
        elif '【舊廠商】'in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='列出所有廠商名稱'))
        elif '【新廠商】'in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='列出所有廠商名稱'))   
        elif '未取名單' in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='未取名單'))
        elif '報表管理' in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='報表管理'))
        elif '廠商管理' in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='廠商管理'))
######################################庫存管理及功能選擇按鈕########################################################
        elif '庫存管理' in msg: 
            message = TextSendMessage(text='請點選以下操作功能',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="新增及快速進貨商品", text="新增及快速進貨商品")),
                                    QuickReplyButton(action=MessageAction(label="查詢商品庫存", text="查詢商品庫存")),
                                    QuickReplyButton(action=MessageAction(label="進貨商品狀態查詢", text="進貨商品狀態查詢")),
                            ]))
            line_bot_api.reply_message(event.reply_token, message)
            #--------------------------新增及修改進貨商品----------------------------------
        elif '新增及快速進貨商品' in msg:
                line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text='商品新增及快速進貨選擇',
                template= ButtonsTemplate(
                    text='請選擇新增或快速進貨商品：',
                    actions=[
                        MessageAction(
                            label='【新增】',
                            text='【進貨商品】新增',
                        ),
                        MessageAction(
                            label='【快速進貨】',
                            text='【進貨商品】快速進貨'
                        )
                    ]
                )
            ))
        elif '【進貨商品】' in msg:
            if msg[6:] == '新增':
                result = nopur_inf()
                flex_message = nopur_inf_flex_msg(result)
                line_bot_api.reply_message(event.reply_token, flex_message)
            elif msg[6:] == '快速進貨':
                line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                                alt_text='商品查詢選擇',
                                template=ButtonsTemplate(
                                    text='請選擇商品查詢方式：',
                                    actions=[
                                        MessageAction(
                                            label='【依類別】',
                                            text='【快速進貨】類別',
                                        ),
                                        MessageAction(
                                            label='【依廠商】',
                                            text='【快速進貨】廠商'
                                        )
                                    ]
                                )
                            ))
        elif msg.startswith('商品ID:'):
            pid = msg[5:-1]
            unit = msg[-1:]
            user_state[user_id] = 'purchase_ck'
            message_storage[user_id + 'purchase_pid'] = pid
            message_storage[user_id + 'purchase_unit'] = unit
            message_storage[user_id+'purchase_all'] = f"商品ID： {pid}\n商品單位：{unit}"
            check_text = f"{message_storage[user_id+'purchase_all']}\n=>請接著輸入「進貨數量」"
            user_state1[user_id] = 'num'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=check_text))
        elif msg.startswith('您已成功新增進貨商品'):
            suc_np_pid = msg[11:]
            np_statechange(suc_np_pid)
        elif '【快速進貨】' in msg:
            if msg[6:] == '類別':
                message = TextSendMessage(text='請點選查詢類別',
                        quick_reply=QuickReply(items=[
                            QuickReplyButton(action=MessageAction(label="測試", text="test1")),
                            QuickReplyButton(action=MessageAction(label="冷凍食品", text="frozen1")),
                            QuickReplyButton(action=MessageAction(label="日常用品", text="dailyuse1")),
                            QuickReplyButton(action=MessageAction(label="甜點", text="dessert1")),
                            QuickReplyButton(action=MessageAction(label="地方特產", text="local1")),
                            QuickReplyButton(action=MessageAction(label="主食", text="staplefood1")),
                            QuickReplyButton(action=MessageAction(label="常溫食品", text="generally1")),
                            QuickReplyButton(action=MessageAction(label="美妝保養", text="beauty1")),
                            QuickReplyButton(action=MessageAction(label="零食", text="snack1")),
                            QuickReplyButton(action=MessageAction(label="保健食品", text="healthy1")),
                            QuickReplyButton(action=MessageAction(label="飲品", text="drinks1")),
                        ]))
                line_bot_api.reply_message(event.reply_token, message)
            elif msg[6:] == '廠商':
                result = allr_manufacturers_name()
                flex_messages = allr_manufacturers_name_flex_msg(result)
                reply_messages = []
                for flex_message in flex_messages:
                    reply_messages.append(flex_message)
                line_bot_api.reply_message(event.reply_token, reply_messages)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='未知指令'))
        ##1010進貨時間要換行換不了
        elif msg.startswith('快速進貨-選擇廠商'):
            manufacturerR_id = msg[9:] 
            result = revm_pur_info(manufacturerR_id)
            flex_message = rev_pur_info_flex_msg(result)
            line_bot_api.reply_message(event.reply_token, flex_message)
        ##1011狀態已成功可以做快速進貨且資料庫可修改
        elif msg.startswith('快速進貨-商品'):
            ppid = msg[7:]
            user_state[user_id] = 'repurchase_ck'
            message_storage[user_id + 'purchase_pid'] = ppid
            message_storage[user_id+'purchase_all'] = f"商品ID： {ppid}"
            check_text = f"{message_storage[user_id+'purchase_all']}\n=>請接著修改「進貨數量」"
            user_state1[user_id] = 'num'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=check_text))
            #line_bot_api.reply_message(event.reply_token, TextSendMessage(text='快速進貨-商品'))
        elif msg in ['frozen1', 'dailyuse1', 'dessert1', 'local1', 'staplefood1', 'generally1', 'beauty1', 'snack1', 'healthy1', 'drinks1', 'test1']:
            selectedr_category = msg.rstrip("1")
            result = revc_pur_info(selectedr_category)
            flex_message = revc_pur_info_flex_msg(result)
            line_bot_api.reply_message(event.reply_token, flex_message)
            #--------------------------查詢商品庫存----------------------------------
        elif '查詢商品庫存' in msg:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text='商品庫存查詢選擇',
                template= ButtonsTemplate(
                    text='請選擇商品庫存查詢方式：\n【庫存警示】或是【所有庫存】',
                    actions=[
                        MessageAction(
                            label='【庫存警示】',
                            text='【查詢】庫存警示',
                        ),
                        MessageAction(
                            label='【所有庫存】',
                            text='【查詢】所有庫存'
                        )
                    ]
                )
            ))
        elif '【查詢】所有庫存' in msg:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text='商品所有庫存查詢選擇',
                template= ButtonsTemplate(
                    text='請選擇商品庫存查詢方式：\n【廠商】或是【類別】',
                    actions=[
                        MessageAction(
                            label='【庫存查詢廠商】',
                            text='【庫存查詢】廠商',
                        ),
                        MessageAction(
                            label='【庫存查詢類別】',
                            text='【庫存查詢】類別'
                        )
                    ]
                )
            )) 

        elif '【庫存查詢】' in msg:
            if msg[6:] == '廠商':
                result = alls_manufacturers_name()
                flex_messages = alls_manufacturers_name_flex_msg(result)
                reply_messages = []
                for flex_message in flex_messages:
                    reply_messages.append(flex_message)
                line_bot_api.reply_message(event.reply_token, reply_messages)
            elif msg[6:] == '類別':
                message = TextSendMessage(text='請點選查詢類別',
                        quick_reply=QuickReply(items=[
                            QuickReplyButton(action=MessageAction(label="測試", text="test2")),
                            QuickReplyButton(action=MessageAction(label="冷凍食品", text="frozen2")),
                            QuickReplyButton(action=MessageAction(label="日常用品", text="dailyuse2")),
                            QuickReplyButton(action=MessageAction(label="甜點", text="dessert2")),
                            QuickReplyButton(action=MessageAction(label="地方特產", text="local2")),
                            QuickReplyButton(action=MessageAction(label="主食", text="staplefood2")),
                            QuickReplyButton(action=MessageAction(label="常溫食品", text="generally2")),
                            QuickReplyButton(action=MessageAction(label="美妝保養", text="beauty2")),
                            QuickReplyButton(action=MessageAction(label="零食", text="snack2")),
                            QuickReplyButton(action=MessageAction(label="保健食品", text="healthy2")),
                            QuickReplyButton(action=MessageAction(label="飲品", text="drinks2")),
                        ]))
                line_bot_api.reply_message(event.reply_token, message)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='未知指令'))
        elif '【查詢】庫存警示' in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='庫存警示'))
        elif msg.startswith('庫存-選擇廠商'):
            manufacturer_id = msg[8:] 
            result = stock_manufacturers(manufacturer_id)
            flex_message = stock_manufacturers_flex_msg(result)
            line_bot_api.reply_message(event.reply_token, flex_message)
        elif msg in ['frozen2', 'dailyuse2', 'dessert2', 'local2', 'staplefood2', 'generally2', 'beauty2', 'snack2', 'healthy2', 'drinks2', 'test2']:
            selectedD_category = msg.rstrip("2")
            result = stock_categoryate(selectedD_category)
            flex_message = stock_categoryate_flex_msg(result)
            line_bot_api.reply_message(event.reply_token, flex_message)
            #--------------------------查看進貨紀錄----------------------------------
        elif '進貨商品狀態查詢' in msg:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text='進貨商品狀態',
                template=ButtonsTemplate(
                    text='請選擇進貨商品狀態查詢方式：',
                    actions=[
                        MessageAction(
                            label='【進貨中】',
                            text='【進貨狀態】進貨中',
                        ),
                        MessageAction(
                            label='【已到貨】',
                            text='【進貨狀態】已到貨'
                        )
                    ]
                )
            ))
        elif '【進貨狀態】' in msg:
            if msg[6:] == '進貨中':
                result = puring_pro()
                flex_messages = puring_pro_flex_msg(result)
                reply_messages = []
                for flex_message in flex_messages:
                    reply_messages.append(flex_message)
                line_bot_api.reply_message(event.reply_token, reply_messages)
            elif msg[6:] == '已到貨':
                result = pured_pro()
                flex_messages = pured_pro_flex_msg(result)
                reply_messages = []
                for flex_message in flex_messages:
                    reply_messages.append(flex_message)
                line_bot_api.reply_message(event.reply_token, reply_messages)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='未知指令'))
        elif msg.startswith('商品已到貨'):
            manufacturerV_id = msg[5:] 
            result = puring_trastate(manufacturerV_id)
            line_bot_api.reply_message(event.reply_token, result)
            #-------------------資料庫測試----------------------
        elif '資料庫' in msg:
            databasetest_msg = f"資料庫連線1：\n{db['databasetest_msg']}\n{db['conn']}\n更新時間：\n{db['databaseup']}\n下次更新時間：\n{db['databasenext']}\n\n"
            databasetest_msg += f"資料庫連線2：\n{db['databasetest_msg1']}\n{db['conn1']}\n更新時間：\n{db['databaseup1']}\n下次更新時間：\n{db['databasenext1']}"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='【資料庫連線測試】結果：\n%s' %(databasetest_msg)))
        elif '測試' in msg:
            datasearch = '暫時'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='【資料庫測試】提取資料測試：\n%s' %(datasearch)))

def send_category_selection(event, line_bot_api):
    message = TextSendMessage(text='請點選查詢類別',
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="測試", text="test")),
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

#-------------------排程設定----------------------
scheduler = BackgroundScheduler()
#資料庫連線1
def dbconnect_job():
    databasetest(db_pool,3)#主要1的重新連線(3分鐘)

#資料庫連線2
def dbconnect1_job():
    databasetest(db_pool,4)#備用1的重新連線(5分鐘)

#檢測資料庫連線
def checkdb():
    timeget = gettime()
    formatted_millisecond = timeget['formatted_datetime']
    formatted_datetime_obj = datetime.strptime(formatted_millisecond, '%Y-%m-%d %H:%M:%S')
    modified_minutes = formatted_datetime_obj.minute
    minutes = int(modified_minutes)
    if minutes not in [0,15,30,45]:
        if minutes % 3 == 0:
            dbconnect_job()
        if minutes % 5 == 0:
            dbconnect1_job()
    else:
        dbconnect_job()
        dbconnect1_job()

# 建立新的執行緒來運行排程函式
def run_schedule():
    while True:
        checkdb()
        schedule.run_pending()
        time.sleep(60)  # 秒
# 啟動排程
schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)