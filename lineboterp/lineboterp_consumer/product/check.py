from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from product.buy_now import *
from product.product_preorder import *
import lineboterp
from ask_wishes.ask import *
from ask_wishes.wishes import *
from database import *

#-------------------使用者狀態檢查----------------------
def product_check():
    id = lineboterp.user_id
    state = lineboterp.user_state
    if state[id] in ['ordering','preorder','phonenum','end']: #判斷user狀態
        check_text = orderandpreorder_check()
    elif state[id] == 'ask':
        check_text = ask()
    elif state[id] == 'wishes':
        check_text = wishes()
    return check_text

#-------------------訂單檢查----------------------
def orderandpreorder_check():
     # 若使用者已經在等待回覆狀態，則根據回覆進行處理
    id = lineboterp.user_id
    state = lineboterp.user_state
    message = lineboterp.msg
    product_id = lineboterp.product[id+'product_id']
    product = lineboterp.product[id+'product']
    product_order_preorder = lineboterp.product_order_preorder
    duplicate_save = lineboterp.duplicate_save
    message_storage = lineboterp.storage
    orderall = lineboterp.orderall
    if message.isdigit():
            # 處理完問題後，結束等待回覆狀態
        if state[id] == 'ordering':
            message_storage[id+'num'] = message
            message_storage[id+'ordertype'] = '訂購'
            check_text = ('商品名稱：%s\n您輸入的訂購數量： %s' %(product,message))
            check_text += '\n=>請接著，打字輸入「電話號碼」\nex.0952000000'
            duplicate_save[id] = check_text
            check_text = TextSendMessage(text=check_text)
            duplicate_save[id] = check_text
            state[id] = 'phonenum' #從user_state轉換輸入電話狀態
        elif state[id] == 'preorder':
            message_storage[id+'num'] = message
            message_storage[id+'ordertype'] = '預購'
            check_text = ('商品名稱：%s\n您輸入的預購數量： %s' %(product,message))
            check_text += '\n=>請接著，打字輸入「電話號碼」\n ex.0952000000'
            check_text = TextSendMessage(text=check_text)
            duplicate_save[id] = check_text
            state[id] = 'phonenum' #從user_state轉換輸入電話狀態
        elif state[id] == 'phonenum':
            if message.isdigit():
                if(len(message) < 10):
                    check_text = TextSendMessage(text='輸入電話格式錯誤！(10碼)\n請重新打字輸入正確的電話號碼：'),TextSendMessage(text='取消訂/預購流程請輸入\n" 取消 "')
                else:
                    if(message[:2] != '09'):
                        check_text = TextSendMessage(text='輸入電話格式錯誤！(09碼)\n請重新打字輸入正確的電話號碼：'),TextSendMessage(text='取消訂/預購流程請輸入\n" 取消 "')
                    else:
                        message_storage[id+'phonenum'] = message
                        state[id] = 'end'#從user_state轉換確認狀態
                        check_text =TemplateSendMessage(
                            alt_text='訂單確認',
                            template=ConfirmTemplate(
                                text=('==訂單資料確認==\n商品ID：%s\n商品名稱：%s\n%s數量：%s\n電話號碼：%s' % (product_id,product,message_storage[id+'ordertype'],message_storage[id+'num'],message_storage[id+'phonenum'])),
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
                numtype = message_storage[id+'ordertype']
                orderall[id] = [product_id,message_storage[id+'num']]#商品紀錄以便存入資料庫
                orderinfo, establishment_message = order_create()#資料庫訂單建立
                orderinfo = orderinfo[0]
                if establishment_message == 'ok':
                    if numtype == '訂購':
                        check_text = f"您的{orderinfo[2]}訂單已成立！\n訂單編號：{str(orderinfo[0])}商品名稱：{orderinfo[1]}\n數量：{str(orderinfo[3])}\n總額：{str(orderinfo[4])}元\n已經可以前往「店面取貨」囉～"
                        check_text = TextSendMessage(text=check_text),Company_location()
                    elif numtype == '預購':
                        check_text = f"您的{orderinfo[2]}訂單已成立！\n訂單編號：{str(orderinfo[0])}商品名稱：{orderinfo[1]}\n數量：{str(orderinfo[3])}\n總額：{str(orderinfo[4])}元\n注意：將於「預購結單日」傳送您是否預購成功呦～"
                        check_text = TextSendMessage(text=check_text)
                    state[id] = 'normal' #從user_state轉換普通狀態
                    #下方重置
                    message_storage[id+'num'] = 'NaN'
                    message_storage[id+'phonenum'] = 'NaN'
                    product_id = 'NaN'
                    product = 'NaN'
                    product_order_preorder[id] = 'NaN'
                    message_storage[id+'ordertype'] = 'NaN'
                else:
                    check_text = TextSendMessage(text=establishment_message)
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
            product_id = 'NaN'
            product = 'NaN'
            product_order_preorder[id] = 'NaN'
            message_storage[id+'ordertype'] = 'NaN'
        elif state[id] in ['ordering','preorder']:
            if state[id] == 'ordering':
                check_text = Order_buynow()
            elif state[id] == 'preorder':
                check_text = Order_preorder()
        elif state[id] =='phonenum':
            check_text = TextSendMessage(text='訂/預購流程中，如想取消請打字輸入" 取消 "'),duplicate_save[id]
        elif state[id] =='end':
            check_text = TemplateSendMessage(
                            alt_text='訂單確認',
                            template=ConfirmTemplate(
                                text=('==訂單資料確認==\n商品名稱：%s\n訂購數量：%s\n%s' % (product,message_storage[id+'num'],message_storage[id+'phonenum'])),
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
        else:
            #非數字
            check_text = '您還在訂/預購中喔！\n輸入的 "' + message + '" 不是此流程的填寫！\n請重新輸入，謝謝～'
            check_text = TextSendMessage(text=check_text),TextSendMessage(text='訂/預購流程中，如想取消請打字輸入" 取消 "')    
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

