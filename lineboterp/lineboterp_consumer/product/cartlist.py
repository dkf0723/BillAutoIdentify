from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import lineboterp
from database import cartsearch,unitsearch,stock,removecart,revise,cartsubtotal

#-------------------購物車資料查詢----------------------
def cart_list():
    user_id = lineboterp.user_id
    db_cartshow = cartsearch()
    if db_cartshow=='資料庫搜尋不到':
        cart_show = TextSendMessage(text='您的購物車中尚無商品資料')
    else:
        cart_show = []
        buttons = []  #模塊中5筆資料
        num = 1
        changelist = '==購物車自檢結果==\n'
        #訂單編號, 商品ID, 商品名稱, 訂購數量, 商品單位, 商品小計
        for totallist in db_cartshow:
            dbstock,dbrnum = stock(totallist[1],totallist[3])
            if dbstock == 'ok':
                if totallist[3] == dbrnum:
                    changenum = str(totallist[3])
                    subtotal = totallist[5]
                else:
                    changenum = str(dbrnum)
                    changelist += f"修改購物車商品：{str(totallist[2])}，已幫您修改至目前庫存剩餘最大數量{dbrnum}{totallist[4]}！\n"
                    text = revise(user_id,totallist[1],int(dbrnum))
                    subtotal = cartsubtotal(totallist[1])
                text ={
                    "type": "text",
                    "text": f"商品{str(num)}",
                    "weight": "bold",
                    "offsetTop": "none",
                    "size": "xl",
                    "margin": "md"
                    }
                text1 ={
                    "type": "text",
                    "text": f"{str(totallist[2])}x{changenum}{totallist[4]}",
                    "size": "md",
                    "wrap": True
                    }
                text2 ={
                    "type": "text",
                    "text": f"小計NT${str('{:,}'.format(subtotal))}",
                    "weight": "bold",
                    "size": "md",
                    "wrap": True,
                    "margin": "md",
                    "align": "end"
                    }
                button ={
                    "type": "button",
                    "action": {
                        "type": "message",
                        "text": f"【修改數量】{totallist[1]}_{str(totallist[2])}",
                        "label": f"修改商品{str(num)}數量"
                    },
                    "margin": "xs",
                    "height": "sm",
                    "style": "secondary"
                    }
                separator ={
                        "type": "separator",
                        "margin": "xl"
                    }
                for i in [text,text1,text2,button,separator]:
                    buttons.append(i)
                num += 1
            elif dbstock == 'no':
                changelist += f"移除購物車清單：{str(totallist[2])}，已無庫存！\n"
                move = removecart(user_id, totallist[1])
        cart_show.append({
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "高逸嚴選",
                "weight": "bold",
                "color": "#1DB446",
                "size": "sm"
            },
            {
                "type": "text",
                "text": "我的購物車",
                "weight": "bold",
                "size": "xxl",
                "margin": "md"
            },
            {
                "type": "separator",
                "margin": "xxl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "md",
                "contents": buttons[:-1]
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "送出購物車訂單",
                "text": "【送出購物車訂單】"
                }
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "修改購物車清單",
                "text": "修改購物車清單"
                }
            }
            ],
            "spacing": "none",
            "paddingAll": "sm"
        },
        "styles": {
            "footer": {
            "separator": True
            }
        }
        })
        if buttons == []:
            cart_show = TextSendMessage(text='您的購物車中尚無商品資料')
        else:
            if len(changelist) != 12:
                change = TextSendMessage(text=changelist)
            else:
                change = TextSendMessage(text='購物車自檢無誤！')
            cart_show = change,FlexSendMessage(
                    alt_text='我的購物車',
                    contents={
                        "type": "carousel",
                        "contents": cart_show      
                        } 
                    )
    return cart_show

#-------------------購物車商品新增----------------------
def addcart():
    user_id = lineboterp.user_id
    user_state = lineboterp.user_state
    product_id = lineboterp.product[user_id+'cartproduct_id']
    product = lineboterp.product[user_id+'cartproduct']

    #購物車清單數量確認最大5筆
    db_cartcheck = cartsearch()
    #訂單編號, 商品ID, 商品名稱, 訂購數量, 商品單位, 商品小計
    cartproductid = []#存放購物車中已有的商品ID
    if db_cartcheck!='資料庫搜尋不到':
        for productcartid in db_cartcheck:
            cartproductid.append(productcartid[1])
    if isinstance(db_cartcheck, str) or len(db_cartcheck) < 5:#等於字串或小於5
        #檢查現在想加入的商品有沒有在購物車中
        if product_id in cartproductid:
            cart = TextSendMessage(text='您的購物車清單中已存在此商品囉～')
        else:
            #Quick Reply 按鈕數量範圍
            quantity_option = []
            unit = unitsearch(product_id)
            for i in range(10):
                if unit == '無':
                    quantity_option.append(QuickReplyButton(action=MessageAction(label=str(i+1), text=str(i+1))))
                else:
                    quantity_option.append(QuickReplyButton(action=MessageAction(label=str(i+1)+unit, text=str(i+1))))
            #------------------------
            user_state[user_id] = 'cartnum'#從user_state轉換輸入購物車數量狀態
            # 建立 Quick Reply 按鈕
            quick_reply_message = TextSendMessage(
                text='商品ID：%s\n商品名稱：%s\n=>請點選此商品加入購物車的數量：' %(product_id,product),
                quick_reply=QuickReply(items=quantity_option)
            )
            cart = TextSendMessage(text='加入購物車流程中，如想取消請打字輸入" 取消 "'),quick_reply_message
                # 傳送回應訊息給使用者
    else:
        cart = TextSendMessage(text='您的購物車清單筆數已達5個商品上限！無法再新增商品至購物車！')
    return cart

#-------------------修改購物車單項商品數量----------------------
def cartrevise():
    user_id = lineboterp.user_id
    user_state = lineboterp.user_state
    product_id = lineboterp.product[user_id+'cartreviseproduct_id']
    product= lineboterp.product[user_id+'cartreviseproduct_name']
    #Quick Reply 按鈕數量範圍
    quantity_option = []
    unit = unitsearch(product_id)
    for i in range(10):
        if unit == '無':
            quantity_option.append(QuickReplyButton(action=MessageAction(label=str(i+1), text=str(i+1))))
        else:
            quantity_option.append(QuickReplyButton(action=MessageAction(label=str(i+1)+unit, text=str(i+1))))
    #------------------------
    user_state[user_id] = 'cartrevise'#從user_state轉換輸入購物車數量狀態
    # 建立 Quick Reply 按鈕
    quick_reply_message = TextSendMessage(
        text='商品ID：%s\n商品名稱：%s\n=>請點選此下方小按鈕修改此商品在購物車中的數量：' %(product_id,product),
        quick_reply=QuickReply(items=quantity_option)
    )
    rcart = TextSendMessage(text='購物車商品數量修改流程中，如想取消請打字輸入" 取消 "'),quick_reply_message
        # 傳送回應訊息給使用者
    return rcart

#-------------------修改購物車清單----------------------
def editcart():
    db_cartshow = cartsearch()
    if db_cartshow=='資料庫搜尋不到':
        edcart_show = TextSendMessage(text='您的購物車中尚無商品資料')
    else:
        edcart_show = []
        buttons = []  #模塊中5筆資料
        num = 1
        #訂單編號, 商品ID, 商品名稱, 訂購數量, 商品單位, 商品小計
        for totallist in db_cartshow:
            text ={
                "type": "text",
                "text": f"商品{str(num)}",
                "weight": "bold",
                "offsetTop": "none",
                "size": "xl",
                "margin": "md"
                }
            text1 ={
                "type": "text",
                "text": f"{str(totallist[2])}x{str(totallist[3])}{totallist[4]}",
                "size": "md",
                "wrap": True
                }
            text2 ={
                "type": "text",
                "text": f"小計NT${str('{:,}'.format(totallist[5]))}",
                "weight": "bold",
                "size": "md",
                "wrap": True,
                "margin": "md",
                "align": "end"
                }
            button ={
                "type": "button",
                "action": {
                    "type": "message",
                    "text": f"【清單移除商品】{totallist[1]}_{str(totallist[2])}",
                    "label": f"從清單移除商品{str(num)}"
                },
                "margin": "xs",
                "height": "sm",
                "style": "secondary"
                }
            separator ={
                    "type": "separator",
                    "margin": "xl"
                }
            for i in [text,text1,text2,button,separator]:
                buttons.append(i)
            num += 1
        edcart_show.append({
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "高逸嚴選",
                "weight": "bold",
                "color": "#1DB446",
                "size": "sm"
            },
            {
                "type": "text",
                "text": "我的購物車",
                "weight": "bold",
                "size": "xxl",
                "margin": "md"
            },
            {
                "type": "separator",
                "margin": "xxl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "md",
                "contents": buttons[:-1]
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "取消修改清單",
                "text": "取消修改清單"
                }
            }
            ],
            "spacing": "none",
            "paddingAll": "sm"
        },
        "styles": {
            "footer": {
            "separator": True
            }
        }
        })
        edcart_show = FlexSendMessage(
                alt_text='我的購物車',
                contents={
                    "type": "carousel",
                    "contents": edcart_show      
                    } 
                )
    return edcart_show