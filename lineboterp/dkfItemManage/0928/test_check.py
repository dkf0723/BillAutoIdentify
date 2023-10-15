from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import manager
from database import *
import database,FM
from FM import products_manufacturers_FM,Now_Product_Modification_FM,Pre_Product_Modification_FM,create_now_purchase_product

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
    if 'createNowProduct' in state[id]:
        check_text= createNowProduct()
    if state[id] in 'searchingOrderByPhoneNumber':
        check_text = searchingOrderByPhoneNumber()
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
def createNowProduct():
     # 若使用者已經在等待回覆狀態，則根據回覆進行處理
    id = manager.user_id
    state = manager.user_state
    state1 = manager.user_state1
    message = manager.msg
    global_Storage = manager.global_Storage
    options = ['a','b','c','d','e','f','g','h','i']
    if state1[id] == 'first':
        global_Storage[id+'pname'] = '品名：'+ message
        check_text = ('您輸入的品名： %s' %(message))
        check_text += '\n=>請接著輸入「商品類別」'
        
        actions=[]
        for option in options:
           actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
        check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
        # check_text = TextSendMessage(text=check_text)
        state1[id] = 'one'
    elif state1[id] == 'one':
        global_Storage[id+'category'] = '商品類別:' + message
        check_text = ('%s\n %s' %(global_Storage[id+'pname'],global_Storage[id+'category']))
        check_text += '\n=>請接著選擇「商品單位」'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'two'
    elif state1[id] == 'two':
        global_Storage[id+'unit'] = '商品單位：' + message
        check_text = ('%s\n%s\n%s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit']))
        check_text += '\n=>請接著輸入「商品簡介」'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'three'
    elif state1[id] == 'three':
        global_Storage[id+'introduction'] = '商品簡介：' + message
        check_text = ('%s\n%s\n%s\n %s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction']))
        check_text += '\n=>請接著輸入「商品售出單價」'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'four'
    elif state1[id] == 'four':
        global_Storage[id+'unitPrice'] = '商品售出單價：' + message
        check_text = ('%s\n%s\n%s\n%s\n%s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction'],global_Storage[id+'unitPrice']))
        check_text += '\n=>請接著輸入「商品售出單價2」'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'five'
    elif state1[id] == 'five':
        global_Storage[id+'unitPrice2'] = '商品售出單價2：' + message
        check_text = ('%s\n%s\n%s\n%s\n%s\n %s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction'],global_Storage[id+'unitPrice'],global_Storage[id+'unitPrice2']))
        check_text += '\n=>請接著輸入「商品圖片」'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'six'
    elif state1[id] == 'six':
        global_Storage[id+'picture'] = '商品圖片：' + message
        check_text = ('%s\n%s\n%s\n%s\n%s\n%s\n%s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction'],global_Storage[id+'unitPrice'],global_Storage[id+'unitPrice2'],global_Storage[id+'picture']))
        check_text += '\n=>請接著輸入「可否退換貨」'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'seven'
    elif state1[id] == 'seven':
        global_Storage[id+'returnProduct'] = '可否退換貨：' + message
        check_text = ('%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction'],global_Storage[id+'unitPrice'],global_Storage[id+'unitPrice2'],global_Storage[id+'picture'],global_Storage[id+'returnProduct']))
        check_text = TextSendMessage(text=check_text)
        global_Storage[id+'tag'] = 'nil'
        state1[id] = 'end'
    elif state1[id] == 'end':
        # state[id] = 'normal'
        # state1[id] = 'NaN'
        # check_text = ('您的商品：%s\n已新增成功！' %(product[id]))
        if(global_Storage[id+'tag']=='品名'):
            global_Storage[id+'pname'] ='品名:'+ message
            global_Storage[id+'tag'] = 'nil'
        if(message[:2]=='品名'):
            check_text = '請輸入品名'
            global_Storage[id+'tag'] = '品名'
            check_text = TextSendMessage(text=check_text)
        if(global_Storage[id+'tag']=='商品類別'):
            global_Storage[id+'category'] ='商品類別:'+ message
            global_Storage[id+'tag'] = 'nil'
        if(message[:4]=='商品類別'):
            check_text = '請輸入商品類別'
            actions=[]
            for option in options:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
            global_Storage[id+'tag'] = '商品類別'
            # check_text = TextSendMessage(text=check_text)
        if(global_Storage[id+'tag']=='商品單位'):
            global_Storage[id+'unit'] ='商品單位:'+ message
            global_Storage[id+'tag'] = 'nil'
        if(message[:4]=='商品單位'):
            check_text = '請輸入商品單位'
            global_Storage[id+'tag'] = '商品單位'
            check_text = TextSendMessage(text=check_text)
        if(global_Storage[id+'tag']=='商品簡介'):
            global_Storage[id+'introduction'] ='商品簡介:'+ message
            global_Storage[id+'tag'] = 'nil'
        if(message[:4]=='商品簡介'):
            check_text = '請輸入商品簡介'
            global_Storage[id+'tag'] = '商品簡介'
            check_text = TextSendMessage(text=check_text)
        if(global_Storage[id+'tag']=='商品售出單價'):
            global_Storage[id+'unitPrice'] = '商品售出單價:'+message
            global_Storage[id+'tag'] = 'nil'
        if(message[:6]=='商品售出單價'):
            check_text = '請輸入商品售出單價'
            global_Storage[id+'tag'] = '商品售出單價'
            check_text = TextSendMessage(text=check_text)
        if(global_Storage[id+'tag']=='商品售出單價2'):
            global_Storage[id+'unitPrice2'] = '商品售出單價2:'+message
            global_Storage[id+'tag'] = 'nil'
        if(message[:7]=='商品售出單價2'):
            check_text = '請輸入商品售出單價2'
            global_Storage[id+'tag'] = '商品售出單價2'
            check_text = TextSendMessage(text=check_text)
        if(global_Storage[id+'tag']=='商品圖片'):
            global_Storage[id+'picture'] = '商品圖片'+message
            global_Storage[id+'tag'] = 'nil'
        if(message[:4]=='商品圖片'):
            check_text = '請輸入商品圖片'
            global_Storage[id+'tag'] = '商品圖片'
            check_text = TextSendMessage(text=check_text)
        if(global_Storage[id+'tag']=='可否退換貨'):
            global_Storage[id+'returnProduct'] = '可否退換貨:'+message
            global_Storage[id+'tag'] = 'nil'
        if(message[:5]=='可否退換貨'):
            check_text = '請輸入可否退換貨'
            global_Storage[id+'tag'] = '可否退換貨'
            check_text = TextSendMessage(text=check_text)
        if(message == '建立商品'):
            check_text = TextSendMessage(text='商品建立成功')
            global_Storage[id+'tag']=''
            state[id]= 'normal';
        if(global_Storage[id+'tag'] == 'nil'):
            check_text = FM.create_now_purchase_product(id)
        
        # check_text = TextSendMessage(text='gg')
    return check_text
def searchingOrderByPhoneNumber():
     # 若使用者已經在等待回覆狀態，則根據回覆進行處理
    id = manager.user_id
    message = manager.msg
    state = manager.user_state
    state1 = manager.user_state1
    if state1[id] =='first':
        actions = []
        options = database.getPhoneNumberByPhoneNumberLastThreeYard(message)
        if options == []:
            check_text = TextSendMessage(text='找不到符合條件的資料')
            state[id] = 'normal'
        else:            
            for option in options:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text='請選擇電話', quick_reply=QuickReply(items=actions))
            state1[id] = 'second'
    elif state1[id] == 'second':
        check_text = TemplateSendMessage(
                alt_text='取貨選擇',
                template=ConfirmTemplate(
                    text='請選擇取貨方式：\n【全部領取】或是【分開領】',
                    actions=[
                        MessageAction(
                            label='【全部領取】',
                            text='全部領取'+message,
                        ),
                        MessageAction(
                            label='【分開領】',
                            text='分開領'+message
                        )
                    ]
                )
            )
        state1[id]='third'
    elif state1[id] == 'third':
        if message[:3] == '分開領':
            actions = []
            options = database.getOrderByPhoneNumber(message[3:])
            for option in options:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text='請選擇訂單', quick_reply=QuickReply(items=actions))
            
        else:
            if message[:4]== '全部領取':
                orderdetails = database.getOrderDetailByPhoneNumber(message[4:])
                # text = '請確認訂單資料：'
                # sum =0 
                # for i in orders:
                #     if i[0] != 'pass':
                #         num = database.getTotalByOrder(i[0])
                #         sum += num
                #         # text += '\n '+i[0] + '\n  總額:' + str( num) +'元'
                #     text += '\n  '+i[1]+'*'+str(i[2]) + ' 金額:'+str(i[3]) +'元'
                # text += '\n總額 '+str(sum)    +'元'                     
            else:
                orderdetails = database.getOrderDetailByOrder(message)
                # text = '請確認訂單資料：\n ' + message + '\n   總額:' + str(database.getTotalByOrder(message)) +'元'
                # for i in orderdetails:
                #     # text +='\n  '+i[0]+'   數量:'+ str(i[1])+'件' + ' 金額:'+str(i[2]) + '元'
                #     text +='\n  '+i[0]+'*'+ str(i[1]) + ' 金額:'+str(i[2]) + '元'
                # # text += '\n  ' + '總額:' + str(database.getTotalByOrder(message))+ '元'
            check_text = FM.showOrder(orderdetails)
                
                     
            # check_text=TemplateSendMessage(
            #         alt_text='訂單資料',
            #         template=ConfirmTemplate(
            #             # data = database.getorderDetailByOrder(order)
            #             text=text,
            #             actions=[
            #                 MessageAction(
            #                     label='【是】',
            #                     text='【是】',
            #                 ),
            #                 MessageAction(
            #                     label='【否】',
            #                     text='【否】'
            #                 )
            #             ]
            #         )
            #     )
            state1[id] = 'end'
    elif state1[id] == 'end':
        if '【確認】' in message:
            check_text = TextSendMessage(text='取貨成功')
        else:
            check_text = TextSendMessage(text='取貨取消')
        state[id] = 'normal'
    return check_text