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
from FM import test_categoryate_FM
from FM import test_manufacturers_FM
from FM import products_manufacturers_FM
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
global global_Storage
global_Storage ={}

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
            user_state[user_id] = 'searchingOrderByPhoneNumber'
            user_state1[user_id] = 'first'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入手機後三碼'))
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
        elif msg in ['frozen', 'dailyuse', 'dessert', 'local', 'staplefood', 'generally', 'beauty', 'snack', 'healthy', 'drinks','test']:
            selected_category = msg
            result = test_categoryate(selected_category)
            flex_message = test_categoryate_FM(result)
            line_bot_api.reply_message(event.reply_token, flex_message)
        # elif '修改商品資訊' in msg:
        #     # extra_info = msg[8:23]  #【修改商品資訊】商品ID:{pid}
        #     line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
        #         alt_text='查詢選擇',
        #         template=ButtonsTemplate(
        #             text='目前商品狀態為：\n【現購】或【預購】',
        #             actions=[
        #                 MessageAction(
        #                     label='【現購】',
        #                     text='【現購】依類別修改'
        #                 ),
        #                 MessageAction(
        #                     label='【預購】',
        #                     text='【預購】依類別修改',
        #                 )
        #             ]
        #         )
        #     ))
        # elif '【現購】依類別修改' in msg:
        #     flex_message = Now_Product_Modification_CFM()
        #     line_bot_api.reply_message(event.reply_token, flex_message)
        #     user_state[user_id] = 'Product_Modification_Pname'
        #     product[user_id + 'Product_Modification_Product_Name'] = msg[9:] 
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text = f"商品ID：{msg[9:]}\n請輸入想修改的商品名稱："))
        # elif '【預購】依類別修改' in msg:
        #     flex_message = Pre_Product_Modification_CFM()
        #     line_bot_api.reply_message(event.reply_token, flex_message)
        elif '【依廠商】查詢'in msg:
            result = test_manufacturers()
            flex_message = test_manufacturers_FM(result)
            line_bot_api.reply_message(event.reply_token, flex_message)
        # elif msg.startswith('選我選我'):
        #     manufacturer_id = msg[5:]  # 提取廠商編號
        #     product[user_id + 'Product_Modification_manufacturer_id'] = manufacturer_id
        #     result = products_manufacturers(manufacturer_id) #套進db函數
        #     flex_message = products_manufacturers_FM(result) #套進FM
        #     line_bot_api.reply_message(event.reply_token, flex_message)
        elif msg.startswith('選我選我'):
            manufacturer_id = msg[5:]  # 提取廠商編號
            # 检查消息格式
            if not manufacturer_id:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="格式不正確，请重新输入。"))
                return

            product[user_id + 'Product_Modification_manufacturer_id'] = manufacturer_id
            
            result = products_manufacturers(manufacturer_id)  #套進db函數 
            if result:
                flex_message = products_manufacturers_FM(result)  #套進FM 
                line_bot_api.reply_message(event.reply_token, flex_message)
            else:
               line_bot_api.reply_message(event.reply_token, TextSendMessage(text="未找到相關產品資訊或發生了錯誤，請重試。"))

        # elif '【修改商品資訊】' in msg:
        #     pid = msg[13:]#【修改商品資訊】商品ID:{pid}
        #     product[str(id) + 'Product_Modification_Product_Name'] = pid
        #     result = test_Product_Modification(pid)
        #     #product[str(id) + 'Product_Modification_manufacturer_id'] = msg[13:]#【修改商品資訊】商品ID:{pid}
        #     if result:
        #        product_status = result[0]
        #        if product_status == '現購':
        #           flex_message = Now_Product_Modification_FM(result)
        #           line_bot_api.reply_message(event.reply_token, flex_message)
        #        elif product_status == '預購':
        #           flex_message = Pre_Product_Modification_FM(result)
        #           line_bot_api.reply_message(event.reply_token, flex_message)
        #        else:
        #           line_bot_api.reply_message(event.reply_token, TextSendMessage(text= '您的回覆：「'+msg+'」\n不在功能中！\n請重新輸入。')) 
        #     else:
        #           line_bot_api.reply_message(event.reply_token, TextSendMessage(text= '商品ID不存在'))  

       # 在消息处理函数中调用 test_Product_Modification
        elif '【修改商品資訊】' in msg:
            id = msg[8:]
            product[user_id + 'Product_Modification_Product_id'] = id
            user_state[user_id] = 'Product_Modification_Product'
            product_status = test_Product_Modification(id)
            product[user_id + 'Product_Modification_Product_status'] = product_status
            if product_status == '現購':
                flex_message = Now_Product_Modification_FM(id)
            elif product_status == '預購':
                flex_message = Pre_Product_Modification_FM(id)
            elif product_status == '查無':
                flex_message = TextSendMessage(text='商品有誤！')
            line_bot_api.reply_message(event.reply_token, flex_message)
        # elif '【現購】依廠商修改'in msg:
        #     user_state[user_id] = 'Product_Modification_Pname'
        #     product[user_id + 'Product_Modification_Product_Name'] = msg[9:] 
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text = f"商品ID：{msg[9:]}\n請輸入想修改的商品名稱："))
        # elif '修改商品名稱'in msg:
        #      user_state[user_id] = 'Product_Modification_Pname'
        #      product[user_id + 'Product_Modification_Product_Name'] = extra_info 
        #      line_bot_api.reply_message(event.reply_token, TextSendMessage(text = f"商品ID：{extra_info}\n請輸入想修改的商品名稱："))
        # elif '【預購】依廠商修改' in msg:
        #     flex_message = Pre_Product_Modification_FM()
        #     line_bot_api.reply_message(event.reply_token, flex_message)    
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
            result = test_manufacturers()
            flex_message = test_manufacturers_FM(result)
            line_bot_api.reply_message(event.reply_token, flex_message)
            #line_bot_api.reply_message(event.reply_token, TextSendMessage(text='列出所有廠商名稱'))
        elif '【新廠商】'in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='列出所有廠商名稱'))
        elif '新增現購商品'in msg:
            user_state[user_id] = 'createNowProduct'
            user_state1[user_id] = 'first'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入商品名稱(低於50字)'))
        elif '新增預購商品'in msg:
            user_state[user_id] = 'createPreOrder'
            user_state1[user_id] = 'first'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入商品名稱(低於50字)'))
        elif '未取名單' in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='未取名單'))
        elif '報表管理' in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='報表管理'))
        elif '廠商管理' in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='廠商管理'))
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
  
# #使用者圖片處理
# @handler.add(MessageEvent, message=ImageMessage)
# def handle_image_message(event):
#     global msgtype
#     msgtype = event.message.type
#     if user_state[user_id] == 'wishesimg':#願望圖片上傳狀態執行
#         image_name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(4))#為圖片隨機命名
#         image_content = line_bot_api.get_message_content(event.message.id)#取得訊息的ID
#         image_name = image_name.upper()+'.jpg'#轉換大寫並加入副檔名
#         path='images/'+image_name #儲存資料夾路徑
#         with open(path, 'wb') as fd: #執行檔案寫入
#             for chunk in image_content.iter_content():
#                 fd.write(chunk)
#         storage[user_id+'img'] = path #暫存圖片路徑
#         line_bot_api.reply_message(event.reply_token, wishes())
#     else:
#         if user_state[user_id] in ['wishes','wishesreason','wishessource','wishescheck']:#以下狀態皆不需要接收到圖片
#             wishesin = wishes()
#             line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='目前動作狀態無需發送照片呦～'),wishesin[1]])
#         else:
#             line_bot_api.reply_message(event.reply_token, TextSendMessage(text='目前動作狀態無需發送照片呦～'))
@handler.add(PostbackEvent)
def handle_postback(event):
    global msg
    postback_data = event.postback.data
    if 'datetime' in event.postback.params:
        # 獲取使用者選擇的日期和時間
        selected_datetime = event.postback.params['datetime']
        tdelete_datetime = selected_datetime.replace('T', ' ')
        #轉換格式2023-10-18T21:00 -> 2023-10-18 21:00:00
        if postback_data == '預購截止時間':
            date_time_obj = datetime.strptime(tdelete_datetime , '%Y-%m-%d %H:%M')
            restock_datetime = date_time_obj.strftime('%Y-%m-%d %H:%M')
            msg = str(restock_datetime)
            response = inventory_check()
        elif postback_data == '預購截止時間321':
            msg = str(restock_datetime)
            response = inventory_check()
        line_bot_api.reply_message(event.reply_token, response)