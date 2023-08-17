from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import lineboterp
def Order_preorder_selectionscreen():
    Order_preorder_screen = []
    Order = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/vLCC99Q.jpg",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "現購商品",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "※商品已在店面。",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "md",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "※隨買快速領取。",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "sm",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "※方便又便宜。",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "sm",
                    "weight": "bold"
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                {
                    "type": "button",
                    "height": "sm",
                    "action": {
                    "type": "message",
                    "label": "現購商列表",
                    "text": "【現購商品】列表"
                    },
                    "color": "#1a9879",
                    "style": "primary"
                }
                ],
                "flex": 0
            }
            }
    Order_preorder_screen.append(Order)
    preorder = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/5ksWY7Y.jpg",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "預購商品",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "※預購訂單截止才進貨。",
                        "wrap": True,
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "margin": "md",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "※預購時間限制(不用搶)。",
                        "wrap": True,
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "margin": "sm",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "※預購數量倍數限制、優惠價格。",
                        "wrap": True,
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "margin": "sm",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "※商品到貨發送取貨通知訊息。",
                        "wrap": True,
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "margin": "sm",
                        "weight": "bold"
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "button",
                        "height": "sm",
                        "action": {
                        "type": "message",
                        "label": "預購商列表",
                        "text": "【預購商品】列表"
                        },
                        "color": "#c42149",
                        "style": "primary"
                    }
                    ],
                    "flex": 0
                }
                }
    Order_preorder_screen.append(preorder)
    screen =FlexSendMessage(
                            alt_text='現/預購商品選擇',
                            contents={
                                "type": "carousel",
                                "contents": Order_preorder_screen   
                                } 
                            )
    return screen