from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import lineboterp

def order_list():
    order_show = []#發送全部
    order_list = []#11筆資料
    for i in range(1, 12):
        button = {
            "type": "button",
            "action": {
                "type": "message",
                "label": str(i),
                "text": str(i)
            }
        }
        order_list.append(button)

    order_show.append({
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
                "text": "訂單查詢",
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
                "contents": order_list
                }
            ]
            },
            "styles": {
            "footer": {
                "separator": True
            }
            }
        })
    return order_show