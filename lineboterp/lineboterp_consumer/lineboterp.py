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
from database import *
from ask_wishes.ask import *
from ask_wishes.wishes import *
from relevant_information import linebotinfo
from product.cartlist import *
from product.orderlist import *
from selection_screen import *
#======python的函式庫==========
import tempfile, os
import datetime
import schedule #排程
import threading #排程執行緒
import time
import requests
import string #字符串處理相關的工具
import random #隨機產生
#安裝schedule套件=> pip install schedule
#=========================
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


#-------------------儲存各種狀態----------------------
global user_state
user_state = {}
global member
member = {}
global product
product = {}
global list_page
list_page = {}
global product_order_preorder
product_order_preorder = {}
global duplicate_save
duplicate_save = {}
global storage
storage = {}
global orderall
orderall = {}
global db
db = {}
global msgtype

#首次資料庫連線，最底下有排程設定
databasetest()

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global user_id
    global msg
    global msgtype
    msgtype = event.message.type
    msg = event.message.text
    user_id = event.source.user_id
    #-------------------檢查是否有在會員名單並且有自己的購物車----------------------
    if user_id not in member:
        member_profile(user_id)#執行會員資料確認
    #-------------------確認及給予初始使用者狀態----------------------
    if user_id not in user_state:
        user_state[user_id] = 'normal'
    if (user_id+'img') not in storage:
        storage[user_id+'img'] = 'NaN'
    #-------------------確認使用者狀態進行處理----------------------
    #使用者狀態不屬於normal，不允許進行其他動作
    if user_state[user_id] != 'normal':
        #執行使用者狀態處理
        check_text = product_check()
        line_bot_api.reply_message(event.reply_token, check_text)
    else:
        if '營業資訊' in msg:
            business_detail = business_information()
            line_bot_api.reply_message(event.reply_token, business_detail)
        #-------------------團購商品及2種商品列表----------------------
        elif '團購商品' in msg:
            line_bot_api.reply_message(event.reply_token, Order_preorder_selectionscreen())
        elif '【預購商品】列表' in msg:
            list_page[user_id+'預購min'] = 0
            list_page[user_id+'預購max'] = 9
            product_show = product_preorder_list()
            line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【預購商品】列表',
                contents={
                    "type": "carousel",
                    "contents": product_show      
                    } 
                ))
        elif '【現購商品】列表' in msg:
            list_page[user_id+'現購min'] = 0
            list_page[user_id+'現購max'] = 9
            product_show = product_buynow_list()
            line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【現購商品】列表',
                contents={
                    "type": "carousel",
                    "contents": product_show      
                    } 
                ))
        #-------------------查詢、訂單、購物車----------------------
        elif '訂單/購物車查詢' in msg:
            line_bot_api.reply_message(event.reply_token, Order_cart_selectionscreen())
        elif '訂單查詢' in msg:
            line_bot_api.reply_message(event.reply_token, Notpickedup_preordered_history_selectionscreen())
        elif '未取訂單列表' in msg:
            ordernottaken = ordernottaken_list()
            line_bot_api.reply_message(event.reply_token, ordernottaken)
        elif '預購訂單列表' in msg:
            line_bot_api.reply_message(event.reply_token, orderpreorder_list())
        elif '歷史訂單列表' in msg:
            history = orderhastaken_list()
            line_bot_api.reply_message(event.reply_token, history)
        elif '【訂單詳細】' in msg:
            msg = str(msg)
            orderall[user_id+'dt'] = msg[-18:]
            searchresult = orderdtsearch()
            line_bot_api.reply_message(event.reply_token, searchresult)
        elif '【加入購物車】' in msg:
            original_string = msg
            # 找到"【加入購物車】"的位置
            start_index = original_string.find("【加入購物車】")
            if start_index != -1:
                # 從"【加入購物車】"後面開始切割字串
                substr = original_string[start_index + len("【加入購物車】"):]
                # 切割取得前後文字
                product_id = substr.split("_")[0].strip() # 取出～前面的字並去除空白字元
                product_name = substr.split("_")[1].strip() # 取出～後面的字並去除空白字元
            product[user_id+'cartproduct_id'] = product_id
            product[user_id+'cartproduct'] = product_name
            cartadd = addcart()
            line_bot_api.reply_message(event.reply_token, cartadd)
        elif '查看購物車' in msg:
            cart = cart_list()
            line_bot_api.reply_message(event.reply_token, cart)
        elif '【修改數量】' in msg:
            original_string = msg
            # 找到"【修改數量】"的位置
            start_index = original_string.find("【修改數量】")
            if start_index != -1:
                # 從"【修改數量】"後面開始切割字串
                substr = original_string[start_index + len("【修改數量】"):]
                # 切割取得前後文字
                product_id = substr.split("_")[0].strip() # 取出_前面的字並去除空白字元
                product_name = substr.split("_")[1].strip() # 取出_後面的字並去除空白字元
            product[user_id+'cartreviseproduct_id'] = product_id
            product[user_id+'cartreviseproduct_name'] = product_name
            cartr = cartrevise()
            line_bot_api.reply_message(event.reply_token, cartr)
        elif '修改購物車清單' in msg:
            carted = editcart()
            line_bot_api.reply_message(event.reply_token, carted)
        elif '【清單移除商品】' in msg:
            original_string = msg
            # 找到"【清單移除商品】"的位置
            start_index = original_string.find("【清單移除商品】")
            if start_index != -1:
                # 從"【清單移除商品】"後面開始切割字串
                substr = original_string[start_index + len("【清單移除商品】"):]
                # 切割取得前後文字
                product_id = substr.split("_")[0].strip() # 取出_前面的字並去除空白字元
                product_name = substr.split("_")[1].strip() # 取出_後面的字並去除空白字元
            movecart = removecart(user_id, product_id)
            if movecart == 'ok':
                msgtxt = ('==購物車商品成功移除==\n移除商品名稱：%s' %(product_name))
            else:
                msgtxt = ('購物車商品移除失敗！請稍後再試。')
            line_bot_api.reply_message(event.reply_token, (TextSendMessage(text=msgtxt),editcart()))
        elif '取消修改清單' in msg:
            line_bot_api.reply_message(event.reply_token, cart_list())
        elif '【送出購物車訂單】' in msg:
            user_state[user_id] = 'cartorderphonenum'
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='購物車訂單流程中，如想取消請打字輸入" 取消 "'),TextSendMessage(text='購物車訂單填寫\n=>請打字輸入手機號碼：\nex.0952000000')])
        #-------------------提問及許願----------------------
        elif '問題提問' in msg:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='問題提問'))  
        elif '許願商品' in msg:
            user_state[user_id] = 'wishes'
            storage[user_id+'wishesstep'] = 1
            storage[user_id+'userfilter'] = 'NaN'
            line_bot_api.reply_message(event.reply_token, initial_fill_screen())
        #-------------------執行購買或預購----------------------
        elif '【立即購買】' in msg:
            original_string = msg
            # 找到"【立即購買】"的位置
            start_index = original_string.find("【立即購買】")
            if start_index != -1:
                # 從"【立即購買】"後面開始切割字串
                substr = original_string[start_index + len("【立即購買】"):]
                # 切割取得前後文字
                product_id = substr.split("_")[0].strip() # 取出～前面的字並去除空白字元
                product_name = substr.split("_")[1].strip() # 取出～後面的字並去除空白字元
            product[user_id+'product_id'] = product_id
            product[user_id+'product'] = product_name
            Order_buynow_text = Order_buynow()
            line_bot_api.reply_message(event.reply_token, Order_buynow_text)
        elif '【手刀預購】' in msg:
            original_string = msg
            # 找到"【手刀預購】"的位置
            start_index = original_string.find("【手刀預購】")
            if start_index != -1:
                # 從"【手刀預購】"後面開始切割字串
                substr = original_string[start_index + len("【手刀預購】"):]
                # 切割取得前後文字
                product_id = substr.split("_")[0].strip() # 取出～前面的字並去除空白字元
                product_name = substr.split("_")[1].strip() # 取出～後面的字並去除空白字元
            product[user_id+'product_id'] = product_id
            product[user_id+'product'] = product_name
            Order_preorder_text = Order_preorder()
            line_bot_api.reply_message(event.reply_token, Order_preorder_text)
        #-------------------現/預購、訂單下一頁----------------------
        elif '【現購列表下一頁】' in msg:
            original_string = msg
            # 找到"【現購列表下一頁】"的位置
            start_index = original_string.find("【現購列表下一頁】")
            if start_index != -1:
                # 從"【現購列表下一頁】"後面開始切割字串
                substr = original_string[start_index + len("【現購列表下一頁】"):]
                # 切割取得前後文字
                min = int(substr.split("～")[0].strip()) # 取出～前面的字並去除空白字元
                max = int(substr.split("～")[1].strip()) # 取出～後面的字並去除空白字元
            list_page[user_id+'現購min'] = min-1
            list_page[user_id+'現購max'] = max
            buynowpage = product_buynow_list()
            if 'TextSendMessage' in buynowpage:
                line_bot_api.reply_message(event.reply_token,buynowpage)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【現購商品】列表',
                contents={
                    "type": "carousel",
                    "contents": buynowpage      
                    } 
                ))
        elif '【預購列表下一頁】' in msg:
            original_string = msg
            # 找到"【預購列表下一頁】"的位置
            start_index = original_string.find("【預購列表下一頁】")
            if start_index != -1:
                # 從"【預購列表下一頁】"後面開始切割字串
                substr = original_string[start_index + len("【預購列表下一頁】"):]
                # 切割取得前後文字
                min = int(substr.split("～")[0].strip()) # 取出～前面的字並去除空白字元
                max = int(substr.split("～")[1].strip()) # 取出～後面的字並去除空白字元
            list_page[user_id+'預購min'] = min-1
            list_page[user_id+'預購max'] = max
            preorderpage = product_preorder_list()
            if 'TextSendMessage' in preorderpage:
                line_bot_api.reply_message(event.reply_token,buynowpage)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【現購商品】列表',
                contents={
                    "type": "carousel",
                    "contents": preorderpage      
                    } 
                ))
        #-------------------資料庫連線測試----------------------
        elif '資料庫' in msg:
            databasetest_msg = databasetest()['databasetest_msg']
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='【資料庫連線測試】\n結果：%s' %(databasetest_msg)))
        elif '測試' in msg:
            datasearch = test_datasearch()
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='【資料庫測試】提取資料測試：\n%s' %(datasearch)))
        #資料庫圖片測試
        elif '圖片' in msg:
            imgsend = imagesent()
            line_bot_api.reply_message(event.reply_token, imgsend)
        #-------------------非上方功能的所有回覆----------------------
        else:
            if '【商品簡介】' not in msg:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text= '您的問題：\n「'+msg+'」\n無法立即回覆！\n已將問題發送至客服人員，請稍後！'))
        #return user_id,user_state

#使用者圖片處理
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    global msgtype
    msgtype = event.message.type
    if user_state[user_id] == 'wishesimg':#願望圖片上傳狀態執行
        image_name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(4))#為圖片隨機命名
        image_content = line_bot_api.get_message_content(event.message.id)#取得訊息的ID
        image_name = image_name.upper()+'.jpg'#轉換大寫並加入副檔名
        path='images/'+image_name #儲存資料夾路徑
        with open(path, 'wb') as fd: #執行檔案寫入
            for chunk in image_content.iter_content():
                fd.write(chunk)
        storage[user_id+'img'] = path #暫存圖片路徑
        line_bot_api.reply_message(event.reply_token, wishes())
    else:
        if user_state[user_id] in ['wishes','wishesreason','wishessource','wishescheck']:#以下狀態皆不需要接收到圖片
            wishesin = wishes()
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='目前動作狀態無需發送照片呦～'),wishesin[1]])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='目前動作狀態無需發送照片呦～'))

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    profile = line_bot_api.get_group_member_profile(uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
    member_profile(uid)#執行會員資料確認
        
#-------------------排程設定----------------------
#資料庫重新連線
def dbconnect_job():
    db['conn'].close()
    db['cursor'].close()
    databasetest()

# 建立新的執行緒來運行排程函式
def run_schedule():
    while True:
        dbconnect_job()
        schedule.run_pending()
        time.sleep(180)  # 秒

# 啟動排程執行緒
schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()
#-----------------------------------------
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

