from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from database  import inquiry_list
import manager

def manager_inquiry_list(): 
    inquiry_show = []
    db_inquiry_list = inquiry_list()

    if db_inquiry_list == '找不到符合條件的資料。':
        inquiry_show = TextSendMessage(text=db_inquiry_list)
    else:
        pagemin = manager.list_page[manager.user_id+'庫存min']
        pagemax = manager.list_page[manager.user_id+'庫存max']#9
        db_inquiry = db_inquiry_list[pagemin:pagemax]     
        product = [] #庫存產品名
        productID = [] #商品ID
        productStatus = [] #庫存狀態
        productStatusColor = [] #庫存狀態顏色
        amount = [] #庫存產品數量


        #預購訂單賦值
        for db_inquiry_list in db_inquiry:
            product.append(db_inquiry_list[0])
            productID.append(db_inquiry_list[1])
            amount.append(db_inquiry_list[2])
            if db_inquiry_list[2]<10:
                productStatus.append("庫存過低")
                productStatusColor.append("#FF5151")
            else:
                productStatus.append("庫存稍微不足")
                productStatusColor.append("#FF8040")
        #列表
        for i in range(len(product)):
            inquiry_show.append({
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "庫存快速查詢",
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "商品名"
                    },
                    {
                        "type": "text",
                        "text": f"{product[i]}"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "商品ID"
                    },
                    {
                        "type": "text",
                        "text": f"{productID[i]}"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "庫存狀態"
                    },
                    {
                        "type": "text",
                        "text": f"{productStatus[i]}",
                        "color": f"{productStatusColor[i]}"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "數量"
                    },
                    {
                        "type": "text",
                        "text": f"{amount[i]}"
                    }
                    ]
                },
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "下訂",
                    "text": f"快速進貨-商品{productID[i]}"
                    }
                }
                ]
            }
        })
        if len(inquiry_show) >= 9:
              inquiry_show.append({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "flex": 1,
                            "gravity": "center",
                            "action": {
                                "type": "message",
                                "label": "''點我''下一頁",
                                "text": "【庫存警示列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                              }
                          }
                      ]
                  }
              })
        else:
              inquiry_show.append({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "flex": 1,
                            "gravity": "center",
                            "action": {
                                "type": "message",
                                "label": "已經到底囉！'點我'【查詢】庫存警示",
                                "text": "【查詢】庫存警示",
                            }
                        }
                    ]
                }
            })
    return inquiry_show