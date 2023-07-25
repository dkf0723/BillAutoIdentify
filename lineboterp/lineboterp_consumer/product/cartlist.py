from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import lineboterp

def cart_list():
    cart_show = []
    cart_list = []
    for i in range(1, 6):
        button = {
            "type": "button",
            "action": {
                "type": "message",
                "label": str(i),
                "text": str(i)
            }
        }
        cart_list.append(button)

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
                "contents": cart_list
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
    return cart_show