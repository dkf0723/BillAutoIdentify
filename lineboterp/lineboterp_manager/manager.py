from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from linebot.models import TextSendMessage
#======這裡是呼叫的檔案內容-蓉=====
# from FM import * #因為蓉的程式碼很多所以多建一個FM
# from test_check import * #蓉所需
from FM import (manager_products_manufacturers_list,manager_manufacturers_list,manager_categoryate_list,Product_management,
                Now_Product_Modification_FM, Pre_Product_Modification_FM)
selected_category = None
#======這裡是呼叫的檔案內容=====
from flexmsg import (quick_purchase_manufacturers_list,quickmanu_pro_list,nopur_inf_flex_msg,product_ing_flex_msg,
                     quick_catepro_list,stock_manufacturers_name_list,stock_manuinf_list,stock_categoryinf_list,
                     pured_pro_list,puring_pro_list,Order_preorder_selectionscreen,Inventory_management)
from database import databasetest,Product_status,stop_time,nopur_inf,product_ing,puring_trastate,bankpay
from relevant_information import linebotinfo,dbinfo
from nepurinf import purchase_check,gettime
from manufacturerFM import Manufacturer_fillin_and_check_screen,Manufacturer_list_and_new_chosen_screen,wishes_list
from vendor_management import Manufacturer_list,Manufacturer_edit 
from DidnotPickedup import *
from Preorder import *
from Inventoryinquiry import *
#======python的函式庫==========
from mysql.connector import pooling
import os
from datetime import datetime
import schedule #排程
import threading #排程執行緒
from apscheduler.schedulers.background import BackgroundScheduler#另一種排程
import time
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
global storage
storage = {}
global orderall
orderall = {}

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
    global user_state #蓉
    global duplicate_save#蓉
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
        #--------商品管理【查詢/修改/下架】或【停售及截止商品列表 】或【新增上架】蓉----------------#           
        elif '商品管理' in msg:
            line_bot_api.reply_message(event.reply_token, Product_management())
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
         #-------------【依類別】查詢-蓉------------------
        elif '【依類別】查詢' in msg:
            send_category_selection(event, line_bot_api)
        elif msg in ['test','frozen', 'dailyuse', 'dessert', 'local', 'staplefood', 'generally', 'beauty', 'snack', 'healthy', 'drinks']:
            duplicate_save[user_id+"selected_category"] = msg
            list_page[user_id+'類別商品數量min'] = 0
            list_page[user_id+'類別商品數量max'] = 9
            show3 = manager_categoryate_list(duplicate_save[user_id+"selected_category"])
            line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                    alt_text='【商品查詢】列表',
                    contents={
                        "type": "carousel",
                        "contents": show3      
                        } 
                    ))
        elif'【商品列表下一頁】' in msg:
            original_string = msg
            # 找到"【商品列表下一頁】"的位置
            start_index = original_string.find("【商品列表下一頁】")
            if start_index != -1:
                # 從"【商品列表下一頁】"後面開始切割字串
                substr = original_string[start_index + len("【商品列表下一頁】"):]
                # 切割取得前後文字
                min = int(substr.split("～")[0].strip()) # 取出～前面的字並去除空白字元
                max = int(substr.split("～")[1].strip()) # 取出～後面的字並去除空白字元
            list_page[user_id+'類別商品數量min'] = min-1
            list_page[user_id+'類別商品數量max'] = max
            show3 = manager_categoryate_list(duplicate_save[user_id+"selected_category"])
            if 'TextSendMessage' in show3:
                line_bot_api.reply_message(event.reply_token,show3)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【類別商品】列表',
                contents={
                    "type": "carousel",
                    "contents": show3 
                    } 
                ))
        #-------------【依廠商】查詢-蓉------------------
        elif '【依廠商】查詢'in msg:
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
        elif '【廠商列表下一頁1】' in msg:#莉蓉的
            original_string = msg
            # 找到"【廠商列表下一頁】"的位置
            start_index = original_string.find("【廠商列表下一頁1】")
            if start_index != -1:
                # 從"【廠商列表下一頁】"後面開始切割字串
                substr = original_string[start_index + len("【廠商列表下一頁1】"):]
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
            duplicate_save[user_id+"manufacturer_id"] = msg[5:]  # 提取廠商編號
            # 檢查格式
            if duplicate_save[user_id+"manufacturer_id"] == '':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="查無此廠商，请重新输入。"))
            else:
                product[user_id + 'Product_Modification_manufacturer_id'] = duplicate_save[user_id+"manufacturer_id"]
                list_page[user_id+'數量min'] = 0
                list_page[user_id+'數量max'] = 9
                show2 = manager_products_manufacturers_list(duplicate_save[user_id+"manufacturer_id"],'no')
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                    alt_text='【商品查詢】列表',
                    contents={
                    "type": "carousel",
                    "contents": show2      
                    } 
                    ))
        elif '【此廠商商品列表下一頁】' in msg:
            original_string = msg
            # 找到"【商品列表下一頁】"的位置
            start_index = original_string.find("【此廠商商品列表下一頁】")
            if start_index != -1:
                # 從"【商品列表下一頁】"後面開始切割字串
                substr = original_string[start_index + len("【此廠商商品列表下一頁】"):]
                # 切割取得前後文字
                min = int(substr.split("～")[0].strip()) # 取出～前面的字並去除空白字元
                max = int(substr.split("～")[1].strip()) # 取出～後面的字並去除空白字元
            list_page[user_id+'廠商數量min'] = min-1
            list_page[user_id+'廠商數量max'] = max
            show2 = manager_products_manufacturers_list(duplicate_save[user_id+"manufacturer_id"],'no')
            if 'TextSendMessage' in show2:
                line_bot_api.reply_message(event.reply_token,show2)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【商品】列表',
                contents={
                    "type": "carousel",
                    "contents": show2      
                    } 
                ))
            #-------------【停售及截止商品列表】-蓉--------------------
        elif msg.startswith('【停售及截止商品列表 】'):
            duplicate_save[user_id+"manufacturer_id"] = msg[5:]  # 提取廠商編號
            # 檢查格式
            if duplicate_save[user_id+"manufacturer_id"] == '':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="查無此廠商，请重新输入。"))
            else:
                product[user_id + 'Product_Modification_manufacturer_id'] = duplicate_save[user_id+"manufacturer_id"]
                list_page[user_id+'stop數量min'] = 0
                list_page[user_id+'stop數量max'] = 9
                show2 = manager_products_manufacturers_list('','stop')
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                    alt_text='【stop商品】列表',
                    contents={
                    "type": "carousel",
                    "contents": show2      
                    } 
                    ))
        elif '【stop商品列表下一頁】' in msg:
            original_string = msg
            # 找到"【商品列表下一頁】"的位置
            start_index = original_string.find("【stop商品列表下一頁】")
            if start_index != -1:
                # 從"【商品列表下一頁】"後面開始切割字串
                substr = original_string[start_index + len("【stop商品列表下一頁】"):]
                # 切割取得前後文字
                min = int(substr.split("～")[0].strip()) # 取出～前面的字並去除空白字元
                max = int(substr.split("～")[1].strip()) # 取出～後面的字並去除空白字元
            list_page[user_id+'stop數量min'] = min-1
            list_page[user_id+'stop數量max'] = max
            show2 = manager_products_manufacturers_list('','stop')
            if 'TextSendMessage' in show2:
                line_bot_api.reply_message(event.reply_token,show2)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【stop商品】列表',
                contents={
                    "type": "carousel",
                    "contents": show2      
                    } 
                ))
        #-------------【修改商品資訊】-蓉------------------------
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
           #-------------【停售】-蓉-------------
        elif '【停售】' in msg:
            a = stop_time(msg[4:])#【停售】{pid}
            if a == 'ok':
                message = '此商品已停售'
            else:
                message = '停售指令失敗'
            # message = f"+{id}+\n+{product_status}+"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = message))   
######################################庫存管理及功能選擇按鈕########################################################
        elif '庫存管理' in msg: 
            line_bot_api.reply_message(event.reply_token, Inventory_management())
            # message = TextSendMessage(text='請點選以下操作功能',
            #                     quick_reply=QuickReply(items=[
            #                         QuickReplyButton(action=MessageAction(label="新增及快速進貨商品", text="新增及快速進貨商品")),
            #                         QuickReplyButton(action=MessageAction(label="查詢商品庫存", text="查詢商品庫存")),
            #                         QuickReplyButton(action=MessageAction(label="進貨商品狀態查詢", text="進貨商品狀態查詢")),
            #                 ]))
            # line_bot_api.reply_message(event.reply_token, message)
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
                line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text='預購及現購選擇',
                template= ButtonsTemplate(
                    text='請選擇預購或現購商品：',
                    actions=[
                        MessageAction(
                            label='【新增預購】',
                            text='【新增】預購',
                        ),
                        MessageAction(
                            label='【新增現購】',
                            text='【新增】現購'
                        )
                    ]
                )
            ))
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
        elif msg.startswith('【新增】預購'):
            result = nopur_inf()
            if result is None:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='無可顯示的預購商品'))
            else:
                flex_message = nopur_inf_flex_msg(result)
                line_bot_api.reply_message(event.reply_token, flex_message)
        elif msg.startswith('【新增】現購'):
            result = product_ing()
            if result is None:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='無可顯示的現購商品'))
            else:
                flex_message = product_ing_flex_msg(result)
                line_bot_api.reply_message(event.reply_token, flex_message)
        elif msg.startswith('預購商品ID:'):
            parts = msg.split("~")
            pid = parts[0].split(":")[1]
            unit = parts[1].split("!")[0]
            manuname = parts[1].split("!")[1].split("/")[0]
            payment = parts[1].split("!")[1].split("/")[1]
            user_state[user_id] = 'pre_purchase_ck'
            storage[user_id + 'purchase_pid'] = pid
            storage[user_id + 'purchase_unit'] = unit
            storage[user_id + 'manu_manuname'] = manuname
            storage[user_id + 'manu_payment'] = payment
            storage[user_id+'purchase_all'] = f"商品ID： {pid}\n商品單位：{unit}\n廠商名：{manuname}\n付款方式：{payment}"
            check_text = f"{storage[user_id+'purchase_all']}\n=>請接著輸入「進貨數量」"
            user_state1[user_id] = 'num'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=check_text))
        elif msg.startswith('現購商品ID:'):
            pid = msg[7:-1]
            unit = msg[-1:]
            user_state[user_id] = 'purchasing_ck'
            storage[user_id + 'purchase_pid'] = pid
            storage[user_id + 'purchase_unit'] = unit
            storage[user_id+'purchase_all'] = f"商品ID： {pid}\n商品單位：{unit}"
            check_text = f"{storage[user_id+'purchase_all']}\n=>請接著輸入「進貨數量」"
            user_state1[user_id] = 'num'
            #getmanuinf()#取得現預購類別及廠商付款方式
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=check_text))
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
                list_page[user_id+'廠商數量min'] = 0
                list_page[user_id+'廠商數量max'] = 9
                showa =  quick_purchase_manufacturers_list()
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                    alt_text='【廠商查詢】列表',
                    contents={
                        "type": "carousel",
                        "contents": showa      
                        } 
                    ))
        elif '【廠商查詢列表下一頁】' in msg:
            original_string = msg
            start_index = original_string.find("【廠商查詢列表下一頁】")
            if start_index != -1:
                substr = original_string[start_index + len("【廠商查詢列表下一頁】"):]
                min = int(substr.split("～")[0].strip()) 
                max = int(substr.split("～")[1].strip()) 
            list_page[user_id+'廠商數量min'] = min-1
            list_page[user_id+'廠商數量max'] = max
            showa = quick_purchase_manufacturers_list()
            if 'TextSendMessage' in showa:
                line_bot_api.reply_message(event.reply_token, showa)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【廠商】列表',
                contents={
                    "type": "carousel",
                    "contents": showa      
                    } 
                ))
        elif msg.startswith('快速進貨-選擇廠商'):
            duplicate_save[user_id+"manufacturerR_id"] = msg[9:]
            if duplicate_save[user_id+"manufacturerR_id"] == '':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="查無此廠商，请重新输入。"))
            else:
                list_page[user_id+'廠商數量min'] = 0
                list_page[user_id+'廠商數量max'] = 9
                showb = quickmanu_pro_list(duplicate_save[user_id+"manufacturerR_id"])
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                    alt_text='【商品查詢】列表',
                    contents={
                    "type": "carousel",
                    "contents": showb      
                    } 
                    ))
        elif '【快速進貨商品列表下一頁】' in msg:
            original_string = msg
            start_index = original_string.find("【快速進貨商品列表下一頁】")
            if start_index != -1:
                substr = original_string[start_index + len("【快速進貨商品列表下一頁】"):]
                min = int(substr.split("～")[0].strip()) 
                max = int(substr.split("～")[1].strip()) 
            list_page[user_id+'廠商數量min'] = min-1
            list_page[user_id+'廠商數量max'] = max
            showb = quickmanu_pro_list(duplicate_save[user_id+"manufacturerR_id"])
            if 'TextSendMessage' in showb:
                line_bot_api.reply_message(event.reply_token,showb)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【商品查詢】列表',
                contents={
                    "type": "carousel",
                    "contents": showb      
                    } 
                ))
        elif msg in ['frozen1', 'dailyuse1', 'dessert1', 'local1', 'staplefood1', 'generally1', 'beauty1', 'snack1', 'healthy1', 'drinks1', 'test1']:
            selectedr_category = msg.rstrip("1")
            duplicate_save[user_id+" selectedr_category"] = selectedr_category
            if selectedr_category == '':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="查無此類別，请重新输入。"))
            else:
                list_page[user_id+'廠商數量min'] = 0
                list_page[user_id+'廠商數量max'] = 9
                showi = quick_catepro_list(selectedr_category)
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                    alt_text='【快速進貨商品查詢】列表',
                    contents={
                    "type": "carousel",
                    "contents":  showi      
                    } 
                    ))
        elif '【類別快速進貨商品列表下一頁】' in msg:
            original_string = msg
            start_index = original_string.find("【類別快速進貨商品列表下一頁】")
            if start_index != -1:
                substr = original_string[start_index + len("【類別快速進貨商品列表下一頁】"):]
                min = int(substr.split("～")[0].strip()) 
                max = int(substr.split("～")[1].strip()) 
            list_page[user_id+'廠商數量min'] = min-1
            list_page[user_id+'廠商數量max'] = max
            showi = quick_catepro_list(duplicate_save[user_id+" selectedr_category"])
            if 'TextSendMessage' in  showi:
                line_bot_api.reply_message(event.reply_token, showi)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【快速進貨商品查詢】列表',
                contents={
                    "type": "carousel",
                    "contents":  showi      
                    } 
                ))
        elif msg.startswith('快速進貨-'): 
            parts = msg.split('~')
            if len(parts) >= 2:
                sta_pro = parts[0].split('-')[1][:2]
                pid = parts[1].split('!')[0]
                unit = parts[1].split('!')[1].split('@')[0]
                payment = parts[1].split('!')[1].split('@')[1]
                storage[user_id + 'purchase_pid'] = pid
                storage[user_id + 'purchase_unit'] = unit
                storage[user_id + 'manu_payment'] = payment
                if sta_pro[:2] == '預購':
                    user_state[user_id] = 'repurchase_ck'
                else:
                    user_state[user_id] = 'rerepurchase_ck'
                storage[user_id+'purchase_all'] = f"商品ID： {pid}\n商品單位：{unit}\n付款方式：{payment}"
                check_text = f"{storage[user_id+'purchase_all']}\n=>請接著輸入「進貨數量」"
                user_state1[user_id] = 'num'
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=check_text))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='錯誤'))
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
                            label='【依類別】',
                            text='【庫存查詢】類別',
                        ),
                        MessageAction(
                            label='【依廠商】',
                            text='【庫存查詢】廠商'
                        )
                    ]
                )
            )) 
        elif '【庫存查詢】' in msg:
            if msg[6:] == '廠商':
                list_page[user_id+'廠商數量min'] = 0
                list_page[user_id+'廠商數量max'] = 9
                showc =  stock_manufacturers_name_list() 
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                    alt_text='【廠商查詢】列表',
                    contents={
                        "type": "carousel",
                        "contents": showc      
                        } 
                    ))
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

        elif '【庫存廠商查詢列表下一頁】' in msg:
            original_string = msg
            start_index = original_string.find("【庫存廠商查詢列表下一頁】")
            if start_index != -1:
                substr = original_string[start_index + len("【庫存廠商查詢列表下一頁】"):]
                min = int(substr.split("～")[0].strip()) 
                max = int(substr.split("～")[1].strip()) 
            list_page[user_id+'廠商數量min'] = min-1
            list_page[user_id+'廠商數量max'] = max
            showc = stock_manufacturers_name_list()
            if 'TextSendMessage' in showc:
                line_bot_api.reply_message(event.reply_token, showc)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【廠商查詢】列表',
                contents={
                    "type": "carousel",
                    "contents": showc      
                    } 
                ))        
        elif msg.startswith('庫存-選擇廠商'):
            duplicate_save[user_id+" manufacturerZ_id"] = msg[7:]
            if duplicate_save[user_id+" manufacturerZ_id"] == '':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="查無此廠商，请重新输入。"))
            else:
                list_page[user_id+'廠商數量min'] = 0
                list_page[user_id+'廠商數量max'] = 9
                showd = stock_manuinf_list(duplicate_save[user_id+" manufacturerZ_id"])
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                    alt_text='【商品查詢】列表',
                    contents={
                    "type": "carousel",
                    "contents":  showd      
                    } 
                    ))
        elif '【庫存商品列表下一頁】' in msg:
            original_string = msg
            start_index = original_string.find("【庫存商品列表下一頁】")
            if start_index != -1:
                substr = original_string[start_index + len("【庫存商品列表下一頁】"):]
                min = int(substr.split("～")[0].strip()) 
                max = int(substr.split("～")[1].strip()) 
            list_page[user_id+'廠商數量min'] = min-1
            list_page[user_id+'廠商數量max'] = max
            showd = stock_manuinf_list(duplicate_save[user_id+"manufacturerZ_id"])
            if 'TextSendMessage' in  showd:
                line_bot_api.reply_message(event.reply_token, showd)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【商品查詢】列表',
                contents={
                    "type": "carousel",
                    "contents":  showd      
                    } 
                ))
        elif msg in ['frozen2', 'dailyuse2', 'dessert2', 'local2', 'staplefood2', 'generally2', 'beauty2', 'snack2', 'healthy2', 'drinks2', 'test2']:
            selectedD_category = msg.rstrip("2")
            duplicate_save[user_id+" selectedD_category"] = selectedD_category
            if selectedD_category == '':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="查無此類別，请重新输入。"))
            else:
                list_page[user_id+'廠商數量min'] = 0
                list_page[user_id+'廠商數量max'] = 9
                showe = stock_categoryinf_list(selectedD_category)
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                    alt_text='【商品查詢】列表',
                    contents={
                    "type": "carousel",
                    "contents":  showe      
                    } 
                    ))
        elif '【類別庫存商品列表下一頁】' in msg:
            original_string = msg
            start_index = original_string.find("【類別庫存商品列表下一頁】")
            if start_index != -1:
                substr = original_string[start_index + len("【類別庫存商品列表下一頁】"):]
                min = int(substr.split("～")[0].strip()) 
                max = int(substr.split("～")[1].strip()) 
            list_page[user_id+'廠商數量min'] = min-1
            list_page[user_id+'廠商數量max'] = max
            showe = stock_categoryinf_list(duplicate_save[user_id+" selectedD_category"])
            if 'TextSendMessage' in  showe:
                line_bot_api.reply_message(event.reply_token, showe)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【商品查詢】列表',
                contents={
                    "type": "carousel",
                    "contents":  showe      
                    } 
                ))
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
                list_page[user_id+'廠商數量min'] = 0
                list_page[user_id+'廠商數量max'] = 9
                showf = puring_pro_list() 
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                    alt_text='【進貨中】商品列表',
                    contents={
                        "type": "carousel",
                        "contents": showf      
                        } 
                    ))
            elif msg[6:] == '已到貨':#!!
                list_page[user_id+'廠商數量min'] = 0
                list_page[user_id+'廠商數量max'] = 9
                showg = pured_pro_list() 
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                    alt_text='【廠商查詢】列表',
                    contents={
                        "type": "carousel",
                        "contents": showg      
                        } 
                    ))
        elif '【已到貨商品查詢列表下一頁】' in msg:
            original_string = msg
            start_index = original_string.find("【已到貨商品查詢列表下一頁】")
            if start_index != -1:
                substr = original_string[start_index + len("【已到貨商品查詢列表下一頁】"):]
                min = int(substr.split("～")[0].strip()) 
                max = int(substr.split("～")[1].strip()) 
            list_page[user_id+'廠商數量min'] = min-1
            list_page[user_id+'廠商數量max'] = max
            showg = pured_pro_list()
            if 'TextSendMessage' in showg:
                line_bot_api.reply_message(event.reply_token, showg)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【已到貨】商品列表',
                contents={
                    "type": "carousel",
                    "contents": showg      
                    } 
                ))        
        elif '【進貨中商品查詢列表下一頁】' in msg:
            original_string = msg
            start_index = original_string.find("【進貨中商品查詢列表下一頁】")
            if start_index != -1:
                substr = original_string[start_index + len("【進貨中商品查詢列表下一頁】"):]
                min = int(substr.split("～")[0].strip()) 
                max = int(substr.split("～")[1].strip()) 
            list_page[user_id+'廠商數量min'] = min-1
            list_page[user_id+'廠商數量max'] = max
            showf = puring_pro_list()
            if 'TextSendMessage' in showf:
                line_bot_api.reply_message(event.reply_token, showf)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【進貨中】商品列表',
                contents={
                    "type": "carousel",
                    "contents": showf      
                    } 
                ))        
        elif msg.startswith('商品已到貨'): #商品已到貨~test00001~現金~預購進貨
            parts = msg.split('~')
            if len(parts) >= 3:
                manufacturerV_id = parts[1]
                payment = parts[2]
                stapro = parts[3][:1]
                if payment == '現金':
                    result = bankpay(manufacturerV_id)#增加當下時間
                    if result == 'ok':
                        result1 = puring_trastate(manufacturerV_id,stapro)
                        if result1 == 'ok':
                            checkchange = '完成1'
                        else:
                            checkchange = f"第一類錯誤1-{result1}"#錯誤訊息(包含資料庫回來的)
                    else:
                        checkchange = f"第一類錯誤2-{result}"#錯誤訊息(包含資料庫回來的)
                else:
                    result = puring_trastate(manufacturerV_id,stapro)
                    if result == 'ok':
                        checkchange = '完成2'
                    else:
                        checkchange = f"第二類錯誤-{result}"#錯誤訊息(包含資料庫回來的)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"商品已到貨流程\n{checkchange}"))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='消息格式不正确'))
        #-------------------廠商管理-新增廠商----------------------
        elif '廠商管理' in msg:
            line_bot_api.reply_message(event.reply_token, Manufacturer_list_and_new_chosen_screen())
        elif '【管理廠商】廠商列表' in msg:
            #上方加入 global list_page = {}
            list_page[user_id+'廠商列表min'] = 0
            list_page[user_id+'廠商列表max'] = 9
            Manufacturerlistpage = Manufacturer_list()
            if 'TextSendMessage' in Manufacturerlistpage:
                line_bot_api.reply_message(event.reply_token,Manufacturerlistpage)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【管理廠商】廠商列表',
                contents={
                    "type": "carousel",
                    "contents": Manufacturerlistpage      
                    } 
                ))
        elif '【廠商列表下一頁2】' in msg:
            original_string = msg
            # 找到"【廠商列表下一頁2】"的位置
            start_index = original_string.find("【廠商列表下一頁2】")
            if start_index != -1:
                # 從"【廠商列表下一頁2】"後面開始切割字串
                substr = original_string[start_index + len("【廠商列表下一頁2】"):]
                # 切割取得前後文字
                min = int(substr.split("～")[0].strip()) # 取出～前面的字並去除空白字元
                max = int(substr.split("～")[1].strip()) # 取出～後面的字並去除空白字元
            if (min - 1) < 0:
                min = 0
            else:
                min = min - 1
            list_page[user_id+'廠商列表min'] = min
            list_page[user_id+'廠商列表max'] = max
            Manufacturerlistpage = Manufacturer_list()
            if 'TextSendMessage' in Manufacturerlistpage:
                line_bot_api.reply_message(event.reply_token,Manufacturerlistpage)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【管理廠商】廠商列表',
                contents={
                    "type": "carousel",
                    "contents": Manufacturerlistpage      
                    } 
                ))
        elif '【管理廠商】建立廠商' in msg:
            user_state[user_id] = 'manufacturer_name'
            storage[user_id+'Manufacturer_edit_step'] = 0
            show = Manufacturer_fillin_and_check_screen('')
            line_bot_api.reply_message(event.reply_token,show)
        elif '【廠商修改資料】' in msg:
            original_string = msg
            # 找到"【廠商修改資料】"的位置
            start_index = original_string.find("【廠商修改資料】")
            if start_index != -1:
                # 從"【廠商修改資料】"後面開始切割字串
                substr = original_string[start_index + len("【廠商修改資料】"):]
                # 切割取得前後文字
                id = substr.split("_")[0].strip() # 取出_前面的廠商id
                substrpage = substr.split("_")[1].strip() # 取出_後面的頁號
                min = int(substrpage.split("～")[0].strip()) # 取出～前面的字並去除空白字元
                max = int(substrpage.split("～")[1].strip()) # 取出～後面的字並去除空白字元
            storage[user_id+'manufacturer_list_id'] = id
            list_page[user_id+'廠商列表min'] = min
            list_page[user_id+'廠商列表max'] = max
            user_state[user_id] = 'manufacturereditall'
            show = Manufacturer_edit()
            line_bot_api.reply_message(event.reply_token,show)
        elif '未取/預購名單' in msg:
            line_bot_api.reply_message(event.reply_token, Order_preorder_selectionscreen())
        elif '【預購名單】列表' in msg:
            show = manager_preorder_list()
            line_bot_api.reply_message(event.reply_token, show)
        elif '【未取名單】列表' in msg:
            show = manager_order_list()
            line_bot_api.reply_message(event.reply_token, show)
        elif '【訂單詳細】' in msg:
            msg = str(msg)
            orderall[user_id+'dt'] = msg[-18:]
            searchresult = orderdtsearch()
            line_bot_api.reply_message(event.reply_token, searchresult)
            #-------------------庫存查詢----------------------
        elif '【查詢】庫存警示' in msg:
            list_page[user_id+'庫存min'] = 0
            list_page[user_id+'庫存max'] = 9
            show = manager_inquiry_list()
            line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【查詢】庫存警示',
                contents={
                    "type": "carousel",
                    "contents": show      
                    } 
                ))
        elif '【庫存警示列表下一頁】' in msg:
            original_string = msg
            # 找到"【庫存警示列表下一頁】"的位置
            start_index = original_string.find("【庫存警示列表下一頁】")
            if start_index != -1:
                # 從"【庫存警示列表下一頁】"後面開始切割字串
                substr = original_string[start_index + len("【庫存警示列表下一頁】"):]
                # 切割取得前後文字
                min = int(substr.split("～")[0].strip()) # 取出～前面的字並去除空白字元
                max = int(substr.split("～")[1].strip()) # 取出～後面的字並去除空白字元
            list_page[user_id+'庫存min'] = min-1
            list_page[user_id+'庫存max'] = max
            show = manager_inquiry_list()
            if 'TextSendMessage' in show:
                line_bot_api.reply_message(event.reply_token,show)
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                alt_text='【庫存警示】列表',
                contents={
                    "type": "carousel",
                    "contents": show      
                    } 
                ))
        elif msg.startswith('報表管理'):
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text='報表管理及許願清單選擇',
                template=ButtonsTemplate(
                    text='請選擇報表管理或許願清單：',
                    actions=[
                        MessageAction(
                            label='報表管理',
                            text='【報表管理】報表管理',
                        ),
                        MessageAction(
                            label='許願清單',
                            text='【報表管理】許願清單'
                        )
                    ]
                )
            ))
        #海碧
        elif '【報表管理】報表管理' in msg:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='報表管理'))
        #-------------------許願清單----------------------
        elif '【報表管理】許願清單' in msg:
            list_page[user_id+'許願min'] = 0
            list_page[user_id+'許願max'] = 9
            line_bot_api.reply_message(event.reply_token,wishes_list())
        #-------------------許願清單下一頁----------------------
        elif '【許願列表下一頁】' in msg:
            original_string = msg
            # 找到"【許願列表下一頁】"的位置
            start_index = original_string.find("【許願列表下一頁】")
            if start_index != -1:
                # 從"【預購列表下一頁】"後面開始切割字串
                substr = original_string[start_index + len("【許願列表下一頁】"):]
                # 切割取得前後文字
                min = int(substr.split("～")[0].strip()) # 取出～前面的字並去除空白字元
                max = int(substr.split("～")[1].strip()) # 取出～後面的字並去除空白字元
            list_page[user_id+'許願min'] = min-1
            list_page[user_id+'許願max'] = max
            line_bot_api.reply_message(event.reply_token,wishes_list())
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

#日期時間選擇器
@handler.add(PostbackEvent)
def handle_postback(event):
    global msg
    storage = manager.storage
    postback_data = event.postback.data
    if 'datetime' in event.postback.params:
        # 獲取使用者選擇的日期和時間
        selected_datetime = event.postback.params['datetime']
        tdelete_datetime = selected_datetime.replace('T', ' ')
        #轉換格式2023-10-18T21:00 -> 2023-10-18 21:00:00
        date_time_obj = datetime.strptime(tdelete_datetime , '%Y-%m-%d %H:%M')
        restock_datetime = date_time_obj.strftime('%Y-%m-%d %H:%M')
        if postback_data in ['新增進貨預購商品匯款時間','快速進貨商品匯款時間']:
            storage[user_id + 'money_time'] = str(restock_datetime)
            storage[user_id+'purchase_all'] += f'\n您輸入的匯款時間： {str(restock_datetime)}'
           
        elif postback_data == '修改商品資訊-預購截止時間':
            msg = str(restock_datetime)
        response = purchase_check()
        line_bot_api.reply_message(event.reply_token, response)
        

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
    if minutes not in [0,15,30,45,60]:
        if minutes % 3 == 0:
            dbconnect_job()
        if minutes % 5 == 0:
            dbconnect1_job()
    else:
        dbconnect_job()

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


    