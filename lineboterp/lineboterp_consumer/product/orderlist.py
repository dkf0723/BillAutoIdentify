from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import lineboterp

#-------------------未取列表----------------------
def ordernottaken_list():
    ordernottaken_show = []#發送全部
    ordernottaken_list = []#10筆資料
    for i in range(1, 11):
        button = {
            "type": "button",
            "action": {
                "type": "message",
                "label": str(i),
                "text": str(i)
            }
        }
        ordernottaken_list.append(button)

    ordernottaken_show.append({
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
                "text": "未取訂單查詢",
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
                "contents": ordernottaken_list
                }
            ]
            },
            "styles": {
            "footer": {
                "separator": True
            }
            }
        })
    return ordernottaken_show

#-------------------已取列表----------------------
def orderhastaken_list():
    orderhastaken_show = []#發送全部
    orderhastaken_list = []#10筆資料
    for i in range(1, 11):
        button = {
            "type": "button",
            "action": {
                "type": "message",
                "label": str(i),
                "text": str(i)
            }
        }
        orderhastaken_list.append(button)

    orderhastaken_show.append({
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
                "text": "歷史(已取)訂單查詢",
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
                "contents": orderhastaken_list
                }
            ]
            },
            "styles": {
            "footer": {
                "separator": True
            }
            }
        })
    return orderhastaken_show