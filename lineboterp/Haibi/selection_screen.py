from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import manager

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
                    "text": "預購名單",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "※最近100筆訂單",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "md",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "BLANK",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "sm",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "BLANK",
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
                    "label": "預購名單列表",
                    "text": "【預購名單】列表"
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
                        "text": "未取名單",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "※最近100筆訂單",
                        "wrap": True,
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "margin": "md",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "※BLANK",
                        "wrap": True,
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "margin": "sm",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "※BLANK",
                        "wrap": True,
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "margin": "sm",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "※BLANK",
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
                        "label": "未取名單列表",
                        "text": "【未取名單】列表"
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
                            alt_text='預購/未取名單列表',
                            contents={
                                "type": "carousel",
                                "contents": Order_preorder_screen   
                                } 
                            )
    return screen