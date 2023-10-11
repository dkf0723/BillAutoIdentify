from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
#======這裡是呼叫的檔案內容=====
from FM import *
from database import *
from FM import manager_products_manufacturers_list,manager_manufacturers_list,test_categoryate_FM
from test_check import *
from relevant_information import linebotinfo,dbinfo
#======python的函式庫==========
from mysql.connector import pooling
import tempfile, os
from datetime import datetime, timedelta
import schedule #排程
import threading #排程執行緒
from apscheduler.schedulers.background import BackgroundScheduler#另一種排程
import time
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
global list_page
list_page = {}

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
    global user_state
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
                    text='請選擇商品服務：\n【查詢/修改/下架】或【新增上架】',
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
                    text='請選擇商品查詢方式：\n【依類別】或【依廠商】',
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
        elif msg in ['test','frozen', 'dailyuse', 'dessert', 'local', 'staplefood', 'generally', 'beauty', 'snack', 'healthy', 'drinks']:
            selected_category = msg
            result = test_categoryate(selected_category)
            flex_message = test_categoryate_FM(result)
            line_bot_api.reply_message(event.reply_token, flex_message)
        elif '【依廠商】查詢'in msg:
            # result = db_manufacturers()
            list_page[user_id+'廠商數量min'] = 0
            list_page[user_id+'廠商數量max'] = 9
            show = manager_manufacturers_list() #這個show是變數隨便取
            line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【廠商查詢】列表',
                contents={
                    "type": "carousel",
                    "contents": show      
                    } 
                ))
        elif '【廠商列表下一頁】' in msg:
            original_string = msg
            # 找到"【廠商列表下一頁】"的位置
            start_index = original_string.find("【廠商列表下一頁】")
            if start_index != -1:
                # 從"【廠商列表下一頁】"後面開始切割字串
                substr = original_string[start_index + len("【廠商列表下一頁】"):]
                # 切割取得前後文字
                min = int(substr.split("～")[0].strip()) # 取出～前面的字並去除空白字元
                max = int(substr.split("～")[1].strip()) # 取出～後面的字並去除空白字元
            list_page[user_id+'廠商數量min'] = min-1
            list_page[user_id+'廠商數量max'] = max
            show = manager_manufacturers_list()
            if 'TextSendMessage' in show:
                line_bot_api.reply_message(event.reply_token,show)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【廠商】列表',
                contents={
                    "type": "carousel",
                    "contents": show      
                    } 
                ))
        elif msg.startswith('選我選我'):
            # manufacturer_id = msg[5:]  # 提取廠商編號
            # # 檢查格式
            # if manufacturer_id == '':
            #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text="格式不正確，请重新输入。"))
            # else:
            #     product[user_id + 'Product_Modification_manufacturer_id'] = manufacturer_id
            #     result = db_products_manufacturers(manufacturer_id)  #套進db函數 
            #     flex_message = manager_products_manufacturers_list(result)  #套進FM 
            #     line_bot_api.reply_message(event.reply_token, flex_message)
            manufacturer_id = msg[5:]  # 提取廠商編號
            # 檢查格式
            if manufacturer_id == '':
                 line_bot_api.reply_message(event.reply_token, TextSendMessage(text="格式不正確，请重新输入。"))
            else:
                product[user_id + 'Product_Modification_manufacturer_id'] = manufacturer_id
                list_page[user_id+'廠商數量min'] = 0
                list_page[user_id+'廠商數量max'] = 9
                show2 = manager_products_manufacturers_list(manufacturer_id)
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                    alt_text='【廠商查詢】列表',
                    contents={
                        "type": "carousel",
                        "contents": show2      
                        } 
                    ))
        elif '【廠商列表下一頁】' in msg:
            original_string = msg
            # 找到"【商品列表下一頁】"的位置
            start_index = original_string.find("【商品列表下一頁】")
            if start_index != -1:
                # 從"【商品列表下一頁】"後面開始切割字串
                substr = original_string[start_index + len("【商品列表下一頁】"):]
                # 切割取得前後文字
                min = int(substr.split("～")[0].strip()) # 取出～前面的字並去除空白字元
                max = int(substr.split("～")[1].strip()) # 取出～後面的字並去除空白字元
            list_page[user_id+'商品數量min'] = min-1
            list_page[user_id+'商品數量max'] = max
            show2 = manager_products_manufacturers_list()
            if 'TextSendMessage' in show2:
                line_bot_api.reply_message(event.reply_token,show)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【商品】列表',
                contents={
                    "type": "carousel",
                    "contents": show2      
                    } 
                ))


        elif '【修改商品資訊】' in msg:
            id = msg[8:]#【修改商品資訊】{pid}
            product[user_id + 'Product_Modification_Product_id'] = id
            product_status = Product_status()# Product_status()開頭是大寫不要搞錯
            product[user_id + 'Product_Modification_Product_status'] = product_status
            if product_status == '現購':
                flex_message = Now_Product_Modification_FM(id)
            elif product_status == '預購':
                flex_message = Pre_Product_Modification_FM(id)
            elif product_status == '預購進貨':
                flex_message = Pre_Product_Modification_FM(id)
            elif product_status == '預購未取':
                flex_message = Pre_Product_Modification_FM(id)
            elif product_status == '預購截止':
                flex_message = Pre_Product_Modification_FM(id)
            elif product_status == '查無':
                user_state = 'normal'
                flex_message = TextSendMessage(text='商品有誤！')
            user_state[user_id] = 'Product_Modification_Product'
            line_bot_api.reply_message(event.reply_token, flex_message)
            return   
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
        # elif '【舊廠商】'in msg:
        #     result = db_manufacturers()
        #     flex_message = test_manufacturers_FM(result)
        #     line_bot_api.reply_message(event.reply_token, flex_message)
        #     #line_bot_api.reply_message(event.reply_token, TextSendMessage(text='列出所有廠商名稱'))
        # elif '【新廠商】'in msg:
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text='列出所有廠商名稱'))

        # elif '未取名單' in msg:
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text='未取名單'))
        # elif '報表管理' in msg:
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text='報表管理'))
        # elif '廠商管理' in msg:
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text='廠商管理'))
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
#-----------------------------------------
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
