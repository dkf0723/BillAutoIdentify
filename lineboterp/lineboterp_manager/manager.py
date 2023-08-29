from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
#======這裡是呼叫的檔案內容=====
#from lirongdb import *
from database import *
from test_check import *
from relevant_information import linebotinfo,dbinfo
#======python的函數庫==========
from mysql.connector import pooling
import tempfile, os
from datetime import datetime
import time
import requests
import schedule #排程
import threading #排程執行緒
from apscheduler.schedulers.background import BackgroundScheduler#另一種排程
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
        #elif msg in ['frozen', 'dailyuse', 'dessert', 'local', 'staplefood', 'generally', 'beauty', 'snack', 'healthy', 'drinks','test']:
              #selected_category = msg
              #flex_message = testZ_categoryate(selected_category)
              #line_bot_api.reply_message(event.reply_token, flex_message)
        #elif '【依廠商】查詢'in msg:
              #flex_message = testZ_manufacturers()
              #line_bot_api.reply_message(event.reply_token, flex_message)'''
        #else:
              #line_bot_api.reply_message(event.reply_token, TextSendMessage(text='未知指令'))
        #elif  msg.startswith('選我選我'): 
              #manufacturer_id = msg[5:]  # 提取廠商編號
              #flex_message = productsZ_manufacturers(manufacturer_id)
              #line_bot_api.reply_message(event.reply_token, flex_message)
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
#####################################################################庫存管理及功能選擇按鈕##########################################################################################
        elif '庫存管理' in msg: 
            message = TextSendMessage(text='請點選以下操作功能',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="新增進貨商品", text="新增進貨商品")),
                                    QuickReplyButton(action=MessageAction(label="查詢商品庫存", text="查詢商品庫存")),
                                    QuickReplyButton(action=MessageAction(label="查看進貨紀錄", text="查看進貨紀錄")),
                            ]))
            line_bot_api.reply_message(event.reply_token, message)
            #--------------------------新增進貨商品----------------------------------
        elif '新增進貨商品' in msg:
                line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text='商品查詢選擇',
                template= ButtonsTemplate(
                    text='請選擇商品查詢方式：\n【類別】或是【廠商】',
                    actions=[
                        MessageAction(
                            label='【依類別】',
                            text='【商品查詢1】類別',
                        ),
                        MessageAction(
                            label='【依廠商】',
                            text='【商品查詢1】廠商'
                        )
                    ]
                )
            ))
            #add_goods()
            #send_product_query_menu(event, line_bot_api)
        elif '【商品查詢1】' in msg:
            if msg[7:] == '類別':
                send_category_selection(event, line_bot_api)
                line_bot_api.reply_message(event.reply_token, message)    
                #user_state[user_id] = 'adding'
                #user_state1[user_id] = 'num'
                #line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入進貨數量：'))
            elif msg[7:] == '廠商':
                flex_message = test_manufacturers()
                line_bot_api.reply_message(event.reply_token, flex_message)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='未知指令'))
        #elif msg.startswith('選擇廠商'):
                #manufacturer_id = msg[5:]  # 提取廠商編號
                #flex_message = products_manufacturers(manufacturer_id)
                #line_bot_api.reply_message(event.reply_token, flex_message)
        #elif msg in ['frozen', 'dailyuse', 'dessert', 'local', 'staplefood', 'generally', 'beauty', 'snack', 'healthy', 'drinks','test']:
                #selected_category = msg
                #flex_message = test_categoryate(selected_category)
                #line_bot_api.reply_message(event.reply_token, flex_message)
            #--------------------------查詢商品庫存----------------------------------
        elif '查詢商品庫存' in msg:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text='商品查詢選擇',
                template= ButtonsTemplate(
                    text='請選擇商品查詢方式：\n【類別】或是【廠商】',
                    actions=[
                        MessageAction(
                            label='【依類別】',
                            text='【商品查詢2】類別',
                        ),
                        MessageAction(
                            label='【依廠商】',
                            text='【商品查詢2】廠商'
                        )
                    ]
                )
            ))
        elif '【商品查詢2】' in msg:
            if msg[7:] == '類別':
                send_category_selection(event, line_bot_api)
                line_bot_api.reply_message(event.reply_token, message)
            elif msg[7:] == '廠商':
                flex_message = test_manufacturers()
                line_bot_api.reply_message(event.reply_token, flex_message)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='未知指令'))
        elif msg.startswith('庫存-選擇廠商'):
                manufacturer_id = msg[8:]  # 提取廠商編號
                flex_message = products_manufacturers(manufacturer_id)
                line_bot_api.reply_message(event.reply_token, flex_message)
        elif msg in ['frozen', 'dailyuse', 'dessert', 'local', 'staplefood', 'generally', 'beauty', 'snack', 'healthy', 'drinks','test']:
                selected_category = msg
                flex_message = test_categoryate(selected_category)
                line_bot_api.reply_message(event.reply_token, flex_message)
            #--------------------------查看進貨紀錄----------------------------------
        elif '查看進貨紀錄' in msg:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text='商品查詢選擇',
                template=ButtonsTemplate(
                    text='請選擇商品查詢方式：',
                    actions=[
                        MessageAction(
                            label='【依類別】',
                            text='【商品查詢3】類別',
                        ),
                        MessageAction(
                            label='【依廠商】',
                            text='【商品查詢3】廠商'
                        ),
                        MessageAction(
                            label='【依時間】',
                            text='【商品查詢3】時間'
                        )
                    ]
                )
            ))
        elif '【商品查詢3】' in msg:
            if msg[7:] == '類別':
                send_category_selection(event, line_bot_api)
                line_bot_api.reply_message(event.reply_token, message)
            elif msg[7:] == '廠商':
                flex_message = testAA_manufacturers()
                line_bot_api.reply_message(event.reply_token, flex_message)
            elif msg[7:] == '時間':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='4'))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='未知指令'))
        elif msg.startswith('進貨-選擇廠商'): #連不到進貨的 連到庫存
                    manufacturerA_id = msg[8:]  # 提取廠商編號
                    flex_message = productsA_manufacturers(manufacturerA_id)
                    line_bot_api.reply_message(event.reply_token, flex_message)
        elif msg in ['frozen', 'dailyuse', 'dessert', 'local', 'staplefood', 'generally', 'beauty', 'snack', 'healthy', 'drinks','test']:
                    selectedA_category = msg # 連到Lirong的
                    flex_message = testA_categoryate(selectedA_category)
                    line_bot_api.reply_message(event.reply_token, flex_message)
            #-------------------資料庫測試----------------------
        elif '資料庫' in msg:
            #databasetest_msg = databasetest()['databasetest_msg']
            databasetest_msg = f"資料庫連線1：\n{db['databasetest_msg']}\n{db['conn']}\n更新時間：\n{db['databaseup']}\n下次更新時間：\n{db['databasenext']}\n\n"
            databasetest_msg += f"資料庫連線2：\n{db['databasetest_msg1']}\n{db['conn1']}\n更新時間：\n{db['databaseup1']}\n下次更新時間：\n{db['databasenext1']}"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='【資料庫連線測試】結果：\n%s' %(databasetest_msg)))
        elif '測試' in msg:
            #datasearch = test_datasearch()
            datasearch = '暫時'
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