from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from database  import order_list
import manager
#---------------預購/未取------------
def manager_order_list(queryObject):
    show = []
    db_preorder_list = order_list(queryObject)

    if db_preorder_list == '找不到符合條件的資料。':
        show = TextSendMessage(text=db_preorder_list)
    else:
        pagemin = 0
        pagemax = 8
        db_preorder = db_preorder_list[pagemin:pagemax]
        show = []
        OrderId = [] #預購的訂單編號
        LineId = [] #預購訂單的LindId
        PhoneNumber = [] #預購訂單的電話
        OrderTime = [] #預購訂單的下訂時間
        Amount = [] #預購訂單的總額
        order_deatils_ProductId = [] #商品ID
        order_deatils_amount = [] #商品個別數量
        order_deatils_total = [] #商品個別小計

        #預購訂單賦值
        for db_preorder_list in db_preorder:
                OrderId.append(db_preorder_list[0])
                LineId.append(db_preorder_list[1])
                PhoneNumber.append(db_preorder_list[2])
                OrderTime.append(db_preorder_list[3])
                Amount.append(db_preorder_list[4])
                order_deatils_ProductId.append(db_preorder_list[5])
                order_deatils_amount.append(db_preorder_list[6])
                order_deatils_total.append(db_preorder_list[7])
    
        #列表
        for i in range(len(OrderId)):
            show.append({
                    "type": "bubble",
                    "body": {
                      "type": "box",
                      "layout": "vertical",
                      "spacing": "none",
                      "contents": [
                        {
                          "type": "text",
                          "text": "高逸嚴選",
                          "wrap": True,
                          "weight": "bold",
                          "size": "sm",
                          "color": "#1DB446",
                          "align": "start"
                        },
                        {
                          "type": "text",
                          "text": f"{queryObject}資訊",
                          "margin": "xs",
                          "size": "xxl",
                          "weight": "bold"
                        },
                        {
                          "type": "box",
                          "layout": "vertical",
                          "contents": [
                            {
                              "type": "box",
                              "layout": "horizontal",
                              "contents": [
                                {
                                  "type": "text",
                                  "text":OrderId[i],
                                  "size": "lg",
                                  "margin": "none",
                                  "flex": 0
                                },
                                {
                                  "type": "text",
                                  "text": LineId[i],
                                  "margin": "none",
                                  "size": "xl",
                                  "offsetStart": "none",
                                  "offsetEnd": "none",
                                  "offsetBottom": "none",
                                  "offsetTop": "none",
                                  "style": "italic"
                                }
                              ]
                            },
                            {
                              "type": "box",
                              "layout": "horizontal",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": OrderTime[i],
                                  "size": "lg",
                                  "margin": "none",
                                  "flex": 0
                                },
                                {
                                  "type": "text",
                                  "text": "112/08/02",
                                  "size": "xl",
                                  "margin": "xs",
                                  "style": "italic"
                                }
                              ]
                            },
                            {
                              "type": "box",
                              "layout": "horizontal",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": PhoneNumber[i],
                                  "size": "lg",
                                  "flex": 0
                                },
                                {
                                  "type": "text",
                                  "text": "0978215471",
                                  "size": "xl",
                                  "margin": "xs",
                                  "style": "italic"
                                }
                              ]
                            },
                            {
                              "type": "box",
                              "layout": "horizontal",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": Amount[i],
                                  "size": "lg",
                                  "margin": "none",
                                  "flex": 0
                                },
                                {
                                  "type": "text",
                                  "text": "$1250",
                                  "size": "xl",
                                  "margin": "xs",
                                  "style": "italic"
                                }
                              ]
                            },
                            {
                              "type": "separator",
                              "margin": "xxl"
                            }
                          ],
                          "margin": "lg"
                        },
                        #訂單內容
                        {
                          "type": "box",
                          "layout": "vertical",
                          "contents": [
                            {
                              "type": "box",
                              "layout": "horizontal",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": "訂單內容",
                                  "margin": "xs",
                                  "size": "xxl",
                                  "weight": "bold",
                                  "color": "#004D99"
                                }
                              ],
                              "margin": "lg"
                            },
                            #商品數for迴圈上標
                            {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": "商品ID :"+order_deatils_ProductId+"/商品數量:"+order_deatils_amount+"/小計:"+order_deatils_total,
                                  "wrap": True,
                                  "margin": "md",
                                  "size": "md",
                                  "color": "#004D99"
                                },
                              ],
                              "margin": "none"
                            }
                            #商品數for迴圈下標
                          ]
                        }
                      ],
                      "margin": "xl"
                    }
              })
            if len(show) >= 9:
              show.append({
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
                                "text": "【未取列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                              }
                          }
                      ]
                  }
              })
            else:
              show.append({
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
                                "label": "已經到底囉！'點我'瀏覽預購/未取名單",
                                "text": "預購/未取名單",
                            }
                        }
                    ]
                }
            })
    show = FlexSendMessage(
            alt_text='【未取訂單】列表',
            contents= show
            )

    return show