from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import manager
import database
import FM
#-------------------使用者狀態檢查----------------------
message_storage = {}
def inventory_check():
    id = manager.user_id
    state = manager.user_state
    if state[id] in 'adding': #判斷user狀態
        check_text = add_goods()
    if state[id] in 'searchingOrderByPhoneNumber':
        check_text = searchingOrderByPhoneNumber()
    # if state[id] in 'searchingOrderByOrdersNumber':
    #     check_text = searchingOrderByOrderNumber()
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

# def searchingOrderByOrderNumber():
#      # 若使用者已經在等待回覆狀態，則根據回覆進行處理
#     id = manager.user_id
#     message = manager.msg
#     state = manager.user_state
#     state1 = manager.user_state1
#     if state1[id] =='first':
#         # actions = []
#         # options = ["123", "456", "c","a", "b", "c","a", "b", "c","a", "b", "c"]
#         # for option in options:
#         #     actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
#         # check_text=TextSendMessage(text='請選擇訂單', quick_reply=QuickReply(items=actions))
#         options = ["123", "456", "c", "a", "b", "c", "a", "b", "c", "a", "b", "c"]
#         actions = []
#         for option in options:
#             actions.append(
#                 QuickReplyButton(
#                     action=PostbackAction(label=option, data=option)  # Use PostbackAction to handle button clicks
#                 )
#             )
#         # Create a message with the quick reply buttons
#         quick_reply_text = "請選擇訂單"
#         check_text = TextSendMessage(
#             text=quick_reply_text,
#             quick_reply=QuickReply(items=actions)
#         )
#         # Handle user's selections in your messaging platform's callback or event handler
#         state1 [id] = 'second'
#     elif state1[id] == 'second' :
#         check_text=TemplateSendMessage(
#                 alt_text='訂單資料',
#                 template=ConfirmTemplate(
#                     text='請選擇取貨方式：\n',
#                     actions=[
#                         MessageAction(
#                             label='【是】',
#                             text='【是】',
#                         ),
#                         MessageAction(
#                             label='【否】',
#                             text='【否】'
#                         )
#                     ]
#                 )
#             )
#         state1[id] = 'third'
#     elif state1[id] == 'third':
#         if '【是】' in message:
#             check_text = TextSendMessage(text='取貨成功')
#         else:
#             check_text = TextSendMessage(text='取貨取消')
#         state[id] = 'normal'
#     return check_text