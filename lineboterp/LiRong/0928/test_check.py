from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import manager
from database import *
from FM import Now_Product_Modification_FM,Pre_Product_Modification_FM
from datetime import datetime
#-------------------使用者狀態檢查----------------------
message_storage = {}
def inventory_check():
    id = manager.user_id
    state = manager.user_state
    if 'Product_Modification' in state[id]:#商品修改
        check_text = product_modification()
    '''if state[id] in 'searching_single': #判斷user狀態
        check_text = search_inf()'''
    '''if state[id] in 'searching_all': #判斷user狀態
        check_text = search_allinf()
    if state[id] in 'end': #判斷user狀態
        check_text = end_stop()'''
    return check_text
#-----------修改商品資訊-----------------
def product_modification():
    id = manager.user_id
    state = manager.user_state
    message = manager.msg
    product = manager.product
    product_status = product[id + 'Product_Modification_Product_status']#現預購狀態
    product_id = product.get(id + 'Product_Modification_Product_id')
    flex_message = None
    storage= manager.storage
    before_all = db_infotmation(product_id)
    
    if state[id] == 'Product_Modification_Product':#這邊是按鈕按下去後的流程
        info = message[8:]
        if '商品名稱' == info:
            state[id] = 'Product_Modification_Product_Pname'
            flex_message = TextSendMessage(text='(◍•ᴗ•◍)請輸入想修改的商品名稱:')
        elif '商品簡介' == info:
            state[id] = 'Product_Modification_Pintroduction'
            flex_message = TextSendMessage(text='(◍•ᴗ•◍)請輸入想修改的商品簡介:')
        elif '商品售出單價' == info:
            state[id] = 'Product_Modification_Punit_price_sold'
            flex_message = TextSendMessage(text='(◍•ᴗ•◍)請輸入想修改的商品售出單價:')
        elif '商品售出單價2'== info:
            state[id] = 'Product_Modification_Punit_price_sold2'
            flex_message = TextSendMessage(text='(◍•ᴗ•◍)請輸入想修改的商品售出單價2:')
        elif '預購倍數' == info:
            state[id] = 'Product_Modification_order_multiple'
            flex_message = TextSendMessage(text='(◍•ᴗ•◍)請輸入想修改的預購倍數:')
        elif '預購截止時間' == info:
            timeget = gettime()
            datetime = timeget['formatted_datetime2']#2023-10-18T21:00 用於LINE的格式
            state[id] = 'Product_Modification_order_deadline'
            template_message = FlexSendMessage(
                            alt_text='預購截止時間選擇',
                            contents={
                                "type": "carousel",
                                "contents": [{
                                "type": "bubble",
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "選擇日期時間",
                                        "weight": "bold",
                                        "size": "xl"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"(◍•ᴗ•◍)請輸入想修改的預購截止時間:",
                                        "wrap": True,
                                    }
                                    ]
                                },
                                "footer": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                    {
                                        "type": "button",
                                        "style": "link",
                                        "height": "sm",
                                        "action": {
                                        "type": "datetimepicker",
                                        "label": "點擊選擇日期與時間",
                                        "data": "預購截止時間",
                                        "mode": "datetime",
                                        "min": f"{datetime}"
                                        }
                                    }
                                    ],
                                    "flex": 0
                                }
                                }]   
                                } 
                            )
            flex_message = template_message
        elif '更換商品圖片' == info:
            state[id] = 'Product_Modification_Photo'
            flex_message = TextSendMessage(text='(◍•ᴗ•◍)請輸入新的商品圖片連結:')
        elif message == '取消':
            state[id] = 'normal'
            flex_message = TextSendMessage(text='已經取消囉！')
        else:
            flex_message = TextSendMessage(text=f'「{message}」錯誤內容指令')


        if message == '退出修改':
            state[id] = 'normal'
            flex_message = TextSendMessage(text='已經取消囉！')
        
    elif state[id] in ['Product_Modification_Product_Pname', 'Product_Modification_Pintroduction', 'Product_Modification_Punit_price_sold', 
                       'Product_Modification_Punit_price_sold2','Product_Modification_order_multiple','Product_Modification_order_deadline',
                       'Product_Modification_Photo']:
        #商品名稱,商品簡介,售出單價,售出單價2,預購數量限制_倍數,預購截止時間,商品圖片
        field_to_modify = None
        if state[id] == 'Product_Modification_Product_Pname':
            if before_all[0][0] == message:
                checkbefore = 'no'#不做資料庫
            else:
                field_to_modify = '商品名稱'
                checkbefore = 'ok'
        elif state[id] == 'Product_Modification_Pintroduction':
            if before_all[0][1] == message:
                checkbefore = 'no'#不做資料庫
            else:
                field_to_modify = '商品簡介'
                checkbefore = 'ok'
        elif state[id] == 'Product_Modification_Punit_price_sold':
            if before_all[0][2] == message:
                checkbefore = 'no'#不做資料庫
            else:
                field_to_modify = '售出單價'
                checkbefore = 'ok'
        elif state[id] == 'Product_Modification_Punit_price_sold2':
            if before_all[0][3] == message:
                checkbefore = 'no'#不做資料庫
            else:
                field_to_modify = '售出單價2'
                checkbefore = 'ok'
        elif state[id] == 'Product_Modification_order_multiple':
            if before_all[0][4] == message:
                checkbefore = 'no'#不做資料庫
            else:
                field_to_modify = '預購數量限制_倍數'
                checkbefore = 'ok'
        elif state[id] == 'Product_Modification_order_deadline':
            if before_all[0][5] == message:
                checkbefore = 'no'#不做資料庫
            else:
                field_to_modify = '預購截止時間'
                checkbefore = 'ok'
        elif state[id] == 'Product_Modification_Photo':
            if before_all[0][6] == message:
                checkbefore = 'no'#不做資料庫
            else:
                field_to_modify = '商品圖片'
                checkbefore = 'ok'

        if message != '取消':
            if checkbefore == 'ok':
                result = MP_information_modify(field_to_modify, message, product_id)
                if result == 'ok':
                    # flex_message = TextSendMessage(text=f'{field_to_modify} 修改成功！')
                    flex_message = get_product_modification_flex_message(product_status, product_id)
                else:
                    flex_message = TextSendMessage(text=f'{field_to_modify} 修改失敗，请稍后再试')
        else:
            flex_message = get_product_modification_flex_message(product_status, product_id)
        state[id] = 'Product_Modification_Product'
    return flex_message

def get_product_modification_flex_message(product_status, product_id):
    if product_status == '現購':
        return Now_Product_Modification_FM(product_id)
    elif product_status == '預購':
        return Pre_Product_Modification_FM(product_id)
    elif product_status == '預購進貨':
        return Pre_Product_Modification_FM(product_id)
    elif product_status == '預購未取':
        return Pre_Product_Modification_FM(product_id)
    elif product_status == '預購截止':
        return Pre_Product_Modification_FM(product_id)
    elif product_status == '查無':
        return TextSendMessage(text='商品有誤！')