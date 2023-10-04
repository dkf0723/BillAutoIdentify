from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import manager
from database import *
from FM import products_manufacturers_FM,Now_Product_Modification_FM,Pre_Product_Modification_FM

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

#-------------------廠商商品資訊修改-----------------------
def product_modification():
    id = manager.user_id
    state = manager.user_state
    message = manager.msg
    product = manager.product
    manufacturer_id = product[id + 'Product_Modification_manufacturer_id'] 
    product_status = product[id + 'Product_Modification_Product_status']#現預購狀態
    product_id = product[id + 'Product_Modification_Product_id']
    if state[id] == 'Product_Modification_Product':
        info = message[8:]
        if '商品名稱' == info:
            state[id] == 'Product_Modification_Product_Pname'
            flex_message = TextSendMessage(text='修改商品名稱')
        elif '商品簡介' == info:
            #state[id] == 'Product_Modification_Product_Pintroduction'
            flex_message = TextSendMessage(text='修改商品簡介')
        elif '商品售出單價' == info:
            flex_message = TextSendMessage(text='修改商品售出單價')
        elif message == '取消':
            state [id] = 'normal'
            flex_message = TextSendMessage(text=f"已經取消囉！")
        else:
            flex_message = TextSendMessage(text=f"「{message}」錯誤內容指令")
    
    elif state[id] == 'Product_Modification_Product_Pname':#修改商品名稱
        if message != '取消':
            result = MP_information(message)#接收使用者打的內容
            if result == 'ok':
                if product_status == '現購':
                    flex_message = Now_Product_Modification_FM(product_id)
                elif product_status == '預購':
                    flex_message = Pre_Product_Modification_FM(product_id)
                elif product_status == '查無':
                    flex_message = TextSendMessage(text='商品有誤！')
            else:
                flex_message = TextSendMessage(text=f"修改失敗請稍後再試")
            state[id] = 'normal'#恢復使用者狀態
        else:
            state[id] = 'normal'#恢復使用者狀態
    elif state[id] == 'Product_Modification_Pintroduction':
        flex_message = ''
    else:#取消修改動作
        state[id] = 'normal'#恢復使用者狀態
    return flex_message 

'''def search_inf():
    id = manager.user_id
    state = manager.user_state
    state2 = manager.user_state1
    message = manager.msg
    product = manager.product[id+'product']
    if state[id] == 'searching_oneinf':
            if state2[id] == 'name':
                message_storage[id+'pname'] = '品名：'+ message
                check_text = ('您輸入的品名： %s' %(message))
                check_text += '\n=>請接著輸入「進貨數量」'
                check_text = TextSendMessage(text=check_text)
                state1[id] = 'checking_one'

    return check_text
     
def search_allinf():
     return check_text

def end_stop():
     return check_text'''