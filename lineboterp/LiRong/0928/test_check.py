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
    if state[id] in 'adding': #判斷user狀態
        check_text = add_goods()
    if 'Product_Modification' in state[id]:#商品修改
        check_text = product_modification()
    '''if state[id] in 'searching_single': #判斷user狀態
        check_text = search_inf()'''
    '''if state[id] in 'searching_all': #判斷user狀態
        check_text = search_allinf()
    if state[id] in 'end': #判斷user狀態
        check_text = end_stop()'''
    return check_text
#-------------------新增商品狀態檢查----------------------
def add_goods():
     # 若使用者已經在等待回覆狀態，則根據回覆進行處理
    id = manager.user_id
    state = manager.user_state
    state1 = manager.user_state1
    message = manager.msg
    product = manager.product
    if state1[id] == 'name':
        message_storage[id+'pname'] = '品名：'+ message
        product[id] = message
        check_text = ('您輸入的品名： %s' %(message))
        check_text += '\n=>請接著輸入「進貨數量」'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'one'
    elif state1[id] == 'one':
        message_storage[id+'num'] = '進貨數量：' + message
        check_text = ('%s\n進貨數量： %s' %(message_storage[id+'pname'],message_storage[id+'num']))
        check_text += '\n=>請接著輸入「進貨成本」'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'two'
    elif state1[id] == 'two':
        message_storage[id+'cost'] = '進貨成本：' + message
        check_text = ('%s\n%s\n進貨成本：%s' %(message_storage[id+'pname'],message_storage[id+'num'],message_storage[id+'cost']))
        check_text += '\n=>請接著輸入「廠商名」'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'three'
    elif state1[id] == 'three':
        message_storage[id+'fname'] = '廠商名：' + message
        check_text = ('%s\n%s\n%s\n進貨成本： %s' %(message_storage[id+'pname'],message_storage[id+'num'],message_storage[id+'cost'],message_storage[id+'fname']))
        check_text += '\n=>請接著輸入「商品有效期限」\nex:2023/07/24'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'four'
    elif state1[id] == 'four':
        message_storage[id+'exp'] = '商品有效期限：' + message
        check_text = ('%s\n%s\n%s\n%s\n%s\n請輸入確認' %(message_storage[id+'pname'],message_storage[id+'num'],message_storage[id+'cost'],message_storage[id+'fname'],message_storage[id+'exp']))
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'end'
    elif state1[id] == 'end':
        state[id] = 'normal'
        state1[id] = 'NaN'
        check_text = ('您的商品：%s\n已新增成功！' %(product[id]))
        check_text = TextSendMessage(text=check_text)
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


        if message == '取消':
            state[id] = 'normal'
            flex_message = TextSendMessage(text='已經取消囉！')
            
    elif state[id] in ['Product_Modification_Product_Pname', 'Product_Modification_Pintroduction', 'Product_Modification_Punit_price_sold', 'Product_Modification_Punit_price_sold2','Product_Modification_order_multiple','Product_Modification_order_deadline','Product_Modification_Photo']:
        field_to_modify = None
        if state[id] == 'Product_Modification_Product_Pname':
            field_to_modify = '商品名稱'
        elif state[id] == 'Product_Modification_Pintroduction':
            field_to_modify = '商品簡介'
        elif state[id] == 'Product_Modification_Punit_price_sold':
            field_to_modify = '售出單價'
        elif state[id] == 'Product_Modification_Punit_price_sold2':
            field_to_modify = '售出單價2'
        elif state[id] == 'Product_Modification_order_multiple':
            field_to_modify = '預購數量限制_倍數'
        elif state[id] == 'Product_Modification_order_deadline':
            field_to_modify = '預購截止時間'
        elif state[id] == 'Product_Modification_Photo':
            field_to_modify = '商品圖片'

        if message != '取消':
            result = MP_information_modify(field_to_modify, message, product_id)
            if result == 'ok':
                flex_message = TextSendMessage(text=f'{field_to_modify} 修改成功！')
                flex_message = get_product_modification_flex_message(product_status, product_id)
            else:
                flex_message = TextSendMessage(text=f'{field_to_modify} 修改失敗，请稍后再试')
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