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
    product = lineboterp.product[id+'product']
    if message.isdigit():
                # 處理完問題後，結束等待回覆狀態
        if state[id] == 'ordering':
            message_storage[id+'num'] = '訂購數量：'+ message
            check_text = ('商品名稱：%s\n您輸入的訂購數量： %s' %(product,message))
            check_text += '\n=>請接著輸入「電話號碼」\nex.0952000000'
            check_text = TextSendMessage(text=check_text)
            state[id] = 'phonenum' #從user_state轉換輸入電話狀態
        elif state[id] == 'preorder':
            message_storage[id+'num'] = '預購數量：'+message
            check_text = ('商品名稱：%s\n您輸入的預購數量： %s' %(product,message))
            check_text += '\n=>請接著，輸入「電話號碼」\n ex.0952000000'
            check_text = TextSendMessage(text=check_text)
            state[id] = 'phonenum' #從user_state轉換輸入電話狀態
        elif state[id] == 'phonenum':
            if message.isdigit():
                if(len(message) < 10):
                    check_text = TextSendMessage(text='輸入電話格式錯誤！(10碼)\n請繼續輸入正確的電話號碼：'),TextSendMessage(text='取消訂/預購流程請輸入\n" 取消 "')
                else:
                    if(message[:2] != '09'):
                        check_text = TextSendMessage(text='輸入電話格式錯誤！(09碼)\n請繼續輸入正確的電話號碼：'),TextSendMessage(text='取消訂/預購流程請輸入\n" 取消 "')
                    else:
                        message_storage[id+'phonenum'] = '電話號碼：' + message
                        state[id] = 'end'#從user_state轉換確認狀態
                        check_text =TemplateSendMessage(
                            alt_text='ConfirmTemplate',
                            template=ConfirmTemplate(
                                text=('==訂單資料確認==\n商品名稱：%s\n%s\n%s' % (product,message_storage[id+'num'],message_storage[id+'phonenum'])),
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
                numtype = message_storage[id+'num']
                if numtype[:2] == '訂購':
                    check_text = ('您的商品：%s\n已完成訂購囉！\n可以前往「店面取貨」囉～' %(product))
                    check_text = TextSendMessage(text=check_text),Company_location()
                elif numtype[:2] == '預購':
                    check_text = ('您的商品：%s\n已完成預購囉！\n注意：將於「預購結單日」傳送您是否預購成功呦～' %(product))
                    check_text = TextSendMessage(text=check_text)
            elif message == '2':
                check_text = '您的商品訂/預購流程\n已經取消囉～'
                check_text = TextSendMessage(text=check_text)
            state[id] = 'normal' #從user_state轉換普通狀態
    else:
        if(message == "取消"):
            check_text = '您的商品訂/預購流程\n已經取消囉～'
            check_text = TextSendMessage(text=check_text)
            state[id] = 'normal' #從user_state轉換普通狀態
            #下方重置
            message_storage[id+'num'] = 'NaN'
            message_storage[id+'phonenum'] = 'NaN'
            product = 'NaN'
        else:
            check_text = '您輸入的 "' + message + '" 不是數字！\n請重新輸入，謝謝～'
            check_text = TextSendMessage(text=check_text)    
    return check_text

#-------------------商家地址----------------------
def Company_location():
    location = LocationSendMessage(
    title='高逸嚴選百貨團購',
    address='235新北市中和區員山路325-4號',
    latitude='25.000965554762445',#緯度
    longitude='121.48115945271607'#經度
    )
    return location

#-------------------商家資訊----------------------
def business_information():
    business_detail= TextSendMessage(text='歡迎來到「高逸嚴選百貨團購」\n'\
    '\n我們的營業時間：\n一至五9:00-20:00\n(六日會發公告是否有營業)\n'\
    '\n簡介：\n高逸團購注重天然、高品質、高CP值商品，讓您們安心選購～若有任何許願商品也歡迎告知！感謝支持與陪伴，很開心能為您們服務！\n'\
    '\n地址：\n新北市中和區員山路325之4號2樓'
    ),Company_location()
    return business_detail