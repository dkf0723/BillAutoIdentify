from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import lineboterp
#-------------------使用者狀態檢查----------------------

message_storage = {}
def product_check():
    id = lineboterp.user_id
    state = lineboterp.user_state
    if state[id] in ['ordering','preorder','phonenum','end']: #判斷user狀態
        check_text = orderandpreorder_check()
    return check_text

#-------------------訂單檢查----------------------
def orderandpreorder_check():
     # 若使用者已經在等待回覆狀態，則根據回覆進行處理
    id = lineboterp.user_id
    state = lineboterp.user_state
    message = lineboterp.msg
    product = lineboterp.product['product']
    if message.isdigit():
                # 處理完問題後，結束等待回覆狀態
        if state[id] == 'ordering':
            message_storage['num'] = '訂購數量：'+ message
            check_text = ('商品名稱：%s\n您輸入的訂購數量： %s' %(product,message))
            check_text += '\n=>請接著輸入「電話號碼」\nex.0952000000'
            check_text = TextSendMessage(text=check_text)
            state[id] = 'phonenum' #從user_state轉換輸入電話狀態
        elif state[id] == 'preorder':
            message_storage['num'] = '預購數量：'+message
            check_text = ('商品名稱：%s\n您輸入的預購數量： %s' %(product,message))
            check_text += '\n=>請接著，輸入「電話號碼」\n ex.0952000000'
            check_text = TextSendMessage(text=check_text)
            state[id] = 'phonenum' #從user_state轉換輸入電話狀態
        elif state[id] == 'phonenum':
            message_storage['phonenum'] = '電話號碼：' + message
            state[id] = 'end'#從user_state轉換確認狀態
            check_text =TemplateSendMessage(
                alt_text='ConfirmTemplate',
                template=ConfirmTemplate(
                    text=('==訂單資料確認==\n商品名稱：%s\n%s\n%s' % (product,message_storage['num'],message_storage['phonenum'])),
                        actions=[
                            MessageAction(
                                label='【1.確認】',
                                text='1'
                            ),
                            MessageAction(
                                label='【2.取消】',
                                text='2'
                            )
                        ]
                    )
                )   
        elif state[id] =='end':
            if message == '1':
                numtype = message_storage['num']
                if numtype[:2] == '訂購':
                    check_text = ('您的商品：%s\n已完成訂購囉！\n可以前往「店面取貨」囉～' %(product))
                    check_text = TextSendMessage(text=check_text)
                elif numtype[:2] == '預購':
                    check_text = ('您的商品：%s\n已完成預購囉！\n注意：將於「預購結單日」傳送您是否預購成功呦～' %(product))
                    check_text = TextSendMessage(text=check_text)
            elif message == '2':
                check_text = '您的商品訂/預購流程\n已經取消囉～'
                check_text = TextSendMessage(text=check_text)
            state[id] = 'normal' #從user_state轉換普通狀態
    else:
        check_text = '您輸入的 "' + message + '" 不是數字！\n請重新輸入，謝謝～'
        check_text = TextSendMessage(text=check_text)    
    return check_text