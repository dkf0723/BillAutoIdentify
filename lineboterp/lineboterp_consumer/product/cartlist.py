from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import lineboterp
from database import cartsearch

def cart_list():
    db_cartshow = cartsearch()
    if db_cartshow=='資料庫搜尋不到':
        cart_show = TextSendMessage(text='您的購物車中尚無商品資料')
    else:
        cart_show = []
        buttons = []  #模塊中5筆資料
        num = 1
        '訂單編號, 商品ID, 商品名稱, 訂購數量, 商品單位, 商品小計'
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
                    "text": f"【修改數量】{totallist[1]}",
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
                "text": "【修改購物車清單】"
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
        cart_show = FlexSendMessage(
                alt_text='我的購物車',
                contents={
                    "type": "carousel",
                    "contents": cart_show      
                    } 
                )
    return cart_show