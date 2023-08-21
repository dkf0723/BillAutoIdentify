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
from product.cartlist import cart_list,addcart,cartrevise,checkcart

#-------------------使用者狀態檢查----------------------
def product_check():
    id = lineboterp.user_id
    state = lineboterp.user_state
     #判斷user狀態
    if state[id] in ['ordering','preorder','phonenum','end']: #單筆訂預購
        check_text = orderandpreorder_check()
    elif state[id] == 'cartnum':#新增購物車
        check_text = cartnum()
    elif state[id] == 'cartrevise':#修改購物車單項商品數量
        check_text = cartrpnum()
    elif state[id] in ['cartorderphonenum','cartorderrun']:#購物車訂單
        check_text = cartorder()
    elif state[id] == 'ask':#QA
        check_text = ask()
    elif state[id] in ['wishes','wishesreason','wishessource','wishesimg','wishescheck']:#願望清單
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
    storage_multiple = lineboterp.storage[id+'multiple']
    if message.isdigit():
            # 處理完問題後，結束等待回覆狀態
        if state[id] == 'ordering':
            message_storage[id+'num'] = message
            message_storage[id+'ordertype'] = '現購'
            check_text = ('商品名稱：%s\n您輸入的現購數量： %s' %(product,message))
            check_text += '\n=>請接著，打字輸入「電話號碼」\nex.0952000000'
            duplicate_save[id] = check_text
            check_text = TextSendMessage(text=check_text)
            duplicate_save[id] = check_text
            state[id] = 'phonenum' #從user_state轉換輸入電話狀態
        elif state[id] == 'preorder':
            if int(message) % storage_multiple == 0:
                message_storage[id+'num'] = message
                message_storage[id+'ordertype'] = '預購'
                check_text = ('商品名稱：%s\n您輸入的預購數量： %s' %(product,message))
                check_text += '\n=>請接著，打字輸入「電話號碼」\n ex.0952000000'
                check_text = TextSendMessage(text=check_text)
                duplicate_save[id] = check_text
                state[id] = 'phonenum' #從user_state轉換輸入電話狀態
            else:
                check_text = [TextSendMessage(text=f"您輸入的「{message}」預購數量倍數不是{str(storage_multiple)}喔！\n請重新輸入預購數量。"),Order_preorder()[0],Order_preorder()[1]]
        elif state[id] == 'phonenum':
            if message.isdigit():
                if(len(message) < 10):
                    check_text = TextSendMessage(text='輸入電話格式錯誤！(10碼)\n請重新打字輸入正確的電話號碼：'),TextSendMessage(text='取消訂/預購流程請輸入\n" 取消 "')
                elif (len(message) > 10):
                    check_text = TextSendMessage(text='輸入電話格式錯誤！(10碼)\n請重新打字輸入正確的電話號碼：'),TextSendMessage(text='取消訂/預購流程請輸入\n" 取消 "')
                elif(message[:2] != '09'):           
                    check_text = TextSendMessage(text='輸入電話格式錯誤！(09碼)\n請重新打字輸入正確的電話號碼：'),TextSendMessage(text='取消訂/預購流程請輸入\n" 取消 "')
                else:
                    message_storage[id+'phonenum'] = message
                    state[id] = 'end'#從user_state轉換確認狀態
                    localsubtotal,dbunitin = quickcalculation(product_id,int(message_storage[id+'num']))#快速計算小計
                    if str(localsubtotal).isdigit():
                        subtotal = str('{:,}'.format(localsubtotal))
                        message_storage[id+'subtotalin'] = subtotal
                        message_storage[id+'unitin'] = dbunitin
                        check_text =TemplateSendMessage(
                        alt_text='訂單確認',
                        template=ConfirmTemplate(
                            text=(f"==訂單資料確認==\n商品ID：{product_id}\n商品名稱：{product}\n電話號碼：{message_storage[id+'phonenum']}\n{message_storage[id+'ordertype']}數量：{message_storage[id+'num']+message_storage[id+'unitin']}\n總計：NT${message_storage[id+'subtotalin']}"),
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
                        check_text = TextSendMessage(text=localsubtotal)
                       
        elif state[id] =='end':
            if message == '1':
                numtype = message_storage[id+'ordertype']
                orderall[id] = [product_id,message_storage[id+'num']]#商品紀錄以便存入資料庫
                orderinfo, establishment_message = order_create()#資料庫訂單建立
                orderinfo = orderinfo[0]
                if establishment_message == 'ok':
                    if numtype == '現購':
                        check_text = f"您的{orderinfo[2]}訂單已成立！\n訂單編號：{str(orderinfo[0])}商品名稱：{orderinfo[1]}\n數量：{str(orderinfo[3])}{str(orderinfo[5])}\n總額：NT${str('{:,}'.format(orderinfo[4]))}\n已經可以前往「店面取貨」囉～"
                        check_text = TextSendMessage(text=check_text),Company_location()
                    elif numtype == '預購':
                        check_text = f"您的{orderinfo[2]}訂單已成立！\n訂單編號：{str(orderinfo[0])}商品名稱：{orderinfo[1]}\n數量：{str(orderinfo[3])}{str(orderinfo[5])}\n總額：NT${str('{:,}'.format(orderinfo[4]))}\n注意：將於「預購結單日」傳送您是否預購成功呦～"
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
                check_text = TemplateSendMessage(
                            alt_text='訂單確認',
                            template=ConfirmTemplate(
                                text=(f"==訂單資料確認==\n商品ID：{product_id}\n商品名稱：{product}\n電話號碼：{message_storage[id+'phonenum']}\n{message_storage[id+'ordertype']}數量：{message_storage[id+'num']+message_storage[id+'unitin']}\n總計：NT${message_storage[id+'subtotalin']}"),
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
        if(message == "取消"):
            check_text = '您的商品現/預購流程\n已經取消囉～'
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
                                text=(f"==訂單資料確認==\n商品ID：{product_id}\n商品名稱：{product}\n電話號碼：{message_storage[id+'phonenum']}\n{message_storage[id+'ordertype']}數量：{message_storage[id+'num']+message_storage[id+'unitin']}\n總計：NT${message_storage[id+'subtotalin']}"),
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
            check_text = '您還在訂/預購中喔！\n輸入的 "' + message + '" 不是此流程的填寫！\n請重新輸入，謝謝～'
            check_text = TextSendMessage(text=check_text),TextSendMessage(text='訂/預購流程中，如想取消請打字輸入" 取消 "')    
    return check_text

#購物車商品新增
def cartnum():
    id = lineboterp.user_id
    state = lineboterp.user_state
    message = lineboterp.msg
    product_id = lineboterp.product[id+'cartproduct_id']
    product = lineboterp.product[id+'cartproduct']
    if message.isdigit():#是數字
        text = cartadd(id,product_id,int(message))
        if text == 'ok':
            unit = unitsearch(product_id)
            check_text = ('==商品成功加入購物車==\n商品名稱：%s\n加入數量： %s %s' %(product,message,unit))
            check_text = TextSendMessage(text=check_text)
            state[id] = 'normal' #結束流程將user_state轉換預設狀態
        else:
            check_text = TextSendMessage(text='購物車加入失敗！請稍後再試。')
            state[id] = 'normal' #結束流程將user_state轉換預設狀態
    else:
        if(message == "取消"):
            check_text = '您的商品加入購物車流程\n已經取消囉～'
            check_text = TextSendMessage(text=check_text)
            state[id] = 'normal' #結束流程將user_state轉換預設狀態
        else:
            check_text = addcart()
    return check_text

def cartrpnum():
    id = lineboterp.user_id
    state = lineboterp.user_state
    message = lineboterp.msg
    product_id = lineboterp.product[id+'cartreviseproduct_id']
    product = lineboterp.product[id+'cartreviseproduct_name']
    if message.isdigit():#是數字
        text = revise(id,product_id,int(message))
        if text == 'ok':
            unit = unitsearch(product_id)
            check_text = ('==購物車商品成功修改數量==\n商品名稱：%s\n修改後數量： %s %s' %(product,message,unit))
            cart1 = cart_list()[0]
            cart2 = cart_list()[1]
            check_text = [TextSendMessage(text=check_text),cart1,cart2]
            state[id] = 'normal' #結束流程將user_state轉換預設狀態
        else:
            check_text = TextSendMessage(text='購物車商品數量修改失敗！請稍後再試。')
            state[id] = 'normal' #結束流程將user_state轉換預設狀態
    else:
        if(message == "取消"):
            check_text = '您的購物車商品數量修改流程\n已經取消囉～'
            cart1 = cart_list()[0]
            cart2 = cart_list()[1]
            check_text = [TextSendMessage(text=check_text),cart1,cart2]
            state[id] = 'normal' #結束流程將user_state轉換預設狀態
        else:
            check_text = cartrevise()
    return check_text

#購物車訂單
def cartorder():
    id = lineboterp.user_id
    state = lineboterp.user_state
    message = lineboterp.msg
    message_storage = lineboterp.storage
    check_text = ''
    if message.isdigit():
        if state[id] == 'cartorderphonenum':
            if message.isdigit():
                if(len(message) < 10):
                    check_text = TextSendMessage(text='輸入電話格式錯誤！(10碼)\n請重新打字輸入正確的電話號碼：'),TextSendMessage(text='取消訂/預購流程請輸入\n" 取消 "')
                elif (len(message) > 10):
                    check_text = TextSendMessage(text='輸入電話格式錯誤！(10碼)\n請重新打字輸入正確的電話號碼：'),TextSendMessage(text='取消訂/預購流程請輸入\n" 取消 "')
                elif(message[:2] != '09'):           
                    check_text = TextSendMessage(text='輸入電話格式錯誤！(09碼)\n請重新打字輸入正確的電話號碼：'),TextSendMessage(text='取消訂/預購流程請輸入\n" 取消 "')
                else:
                    state[id] = 'cartorderrun'#從user_state轉換確認狀態
                    db_cartshow = cartsearch()
                    showp = f"電話號碼：{message}\n\n"
                    num = 1
                    tnum = 0#總額
                    #訂單編號, 商品ID, 商品名稱, 訂購數量, 商品單位, 商品小計
                    for totallist in db_cartshow:
                        showp += f"<<商品{num}>>\n商品ID：{totallist[1]}\n商品名稱：{totallist[2]}\n數量：{totallist[3]}{totallist[4]}\n小計：{str('{:,}'.format(totallist[5]))}\n---\n"
                        num += 1
                        tnum += totallist[5]
                    message_storage[id+'showp'] = showp[:-4] #訂單資訊
                    message_storage[id+'shownum'] = tnum #總額
                    message_storage[id+'phonenum'] = message
                    ##購物車列表
                    check_text = checkcart(message_storage[id+'showp'],message_storage[id+'shownum'])
        elif state[id] == 'cartorderrun':
            if message == '1':
                orderinfo, establishment_message = cartordergo(message_storage[id+'phonenum'])#執行購物車訂單建立
                number = 1
                total = 0
                if establishment_message == 'ok':
                    check_text = f"您的購物車訂單已成立！\n訂單編號：{str(orderinfo[0][0])}"
                    for orderlistinfo in orderinfo:
                        check_text += f"商品{number}名稱：{orderlistinfo[1]}\n數量：{str(orderlistinfo[3])}{str(orderlistinfo[5])}\n小計：{str('{:,}'.format(orderlistinfo[4]))}\n---\n"
                        number += 1
                        total += orderlistinfo[4]
                    check_text += f"總額：{str('{:,}'.format(total))}元\n已經可以前往「店面取貨」囉～"
                    check_text = TextSendMessage(text=check_text),Company_location()
                    state[id] = 'normal' #從user_state轉換普通狀態
                else:
                    cart1 = cart_list()[0]
                    cart2 = cart_list()[1]
                    check_text = [TextSendMessage(text=establishment_message),cart1,cart2]
            elif message == '2':
                check_text = '您的購物車訂單流程\n已經取消囉～'
                check_text = TextSendMessage(text=check_text)
                state[id] = 'normal' #從user_state轉換普通狀態
            else:
                check_text = TextSendMessage(text='購物車訂單流程中，如想取消請打字輸入" 取消 "'),checkcart(message_storage[id+'showp'],message_storage[id+'shownum'])
    else:
        if(message == "取消"):
            check_text = '您的購物車訂單流程\n已經取消囉～'
            check_text = TextSendMessage(text=check_text)
            state[id] = 'normal' #結束流程將user_state轉換預設狀態
        elif state[id] == 'cartorderphonenum':
            check_text = TextSendMessage(text='購物車訂單流程中，如想取消請打字輸入" 取消 "'),TextSendMessage(text='您還在購物車訂單流程\n=>請輸入手機號號碼：')
        elif state[id] == 'cartorderrun':
            check_text = TextSendMessage(text='購物車訂單流程中，如想取消請打字輸入" 取消 "'),checkcart(message_storage[id+'showp'],message_storage[id+'shownum'])
        else:
            check_text = '您還在購物車訂單中喔！\n輸入的 "' + message + '" 不是此流程的填寫！\n請重新輸入，謝謝～'
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
    '''business_detail= TextSendMessage(text='歡迎來到「高逸嚴選百貨團購」\n'\
    '\n我們的營業時間：\n一至五9:00-20:00\n(六日會發公告是否有營業)\n'\
    '\n簡介：\n高逸團購注重天然、高品質、高CP值商品，讓您們安心選購～若有任何許願商品也歡迎告知！感謝支持與陪伴，很開心能為您們服務！\n'\
    '\n地址：\n新北市中和區員山路325之4號2樓'
    ),Company_location()'''
    business_info = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "image",
                            "url": "https://i.imgur.com/hQ0qG9c.jpg",
                            "size": "5xl",
                            "aspectMode": "cover",
                            "aspectRatio": "150:196",
                            "gravity": "center",
                            "flex": 1
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "image",
                                "url": "https://i.imgur.com/XsyIMd0.jpg",
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "150:98",
                                "gravity": "center"
                            },
                            {
                                "type": "image",
                                "url": "https://i.imgur.com/4Nh5x9j.jpg",
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "150:98",
                                "gravity": "center"
                            }
                            ],
                            "flex": 1
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "image",
                                "url": "https://i.imgur.com/rGlTAt3.jpg",
                                "aspectMode": "cover",
                                "size": "full"
                            }
                            ],
                            "cornerRadius": "100px",
                            "width": "80px",
                            "height": "80px"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "contents": [
                                {
                                    "type": "span",
                                    "text": "高逸嚴選百貨團購",
                                    "weight": "bold",
                                    "color": "#000000",
                                    "size": "lg"
                                }
                                ],
                                "size": "sm",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": "營業時間：\n週一至五9:00-20:00\n(六、日會發公告) ",
                                "wrap": True
                            }
                            ]
                        }
                        ],
                        "spacing": "xl",
                        "paddingAll": "20px"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "separator"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "簡介",
                                    "wrap": True,
                                    "size": "xl",
                                    "offsetTop": "xxl",
                                    "weight": "bold"
                                }
                                ],
                                "cornerRadius": "100px",
                                "width": "30px",
                                "height": "100px"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "高逸團購注重天然、高品質、高CP值商品，讓您們安心選購～若有任何許願商品也歡迎告知！感謝支持與陪伴，很開心能為您們服務！",
                                    "wrap": True
                                }
                                ]
                            }
                            ],
                            "spacing": "xl",
                            "paddingAll": "20px"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "uri",
                            "label": "FB粉絲專頁",
                            "uri": "https://www.facebook.com/profile.php?id=100063943548653&mibextid=LQQJ4d"
                            },
                            "style": "primary",
                            "color": "#a8c1c9",
                            "margin": "sm"
                        },
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "地址",
                                    "wrap": True,
                                    "size": "xl",
                                    "weight": "bold"
                                }
                                ],
                                "cornerRadius": "100px",
                                "width": "25px",
                                "height": "72px"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "新北市中和區員山路325之4號2樓(全家-中和員山店旁)",
                                    "wrap": True,
                                    "offsetTop": "lg"
                                }
                                ]
                            }
                            ],
                            "spacing": "xl",
                            "paddingAll": "20px"
                        }
                        ]
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "uri",
                        "label": "地圖導航",
                        "uri": "https://goo.gl/maps/N1Rq3nX3XEpdtxLm9"
                        },
                        "style": "primary",
                        "color": "#C9B0A8"
                    }
                    ],
                    "paddingAll": "0px"
                }
                }

    business_detail =FlexSendMessage(
                            alt_text='營業資訊',
                            contents={
                                "type": "carousel",
                                "contents": [business_info]   
                                } 
                            )
    return business_detail

