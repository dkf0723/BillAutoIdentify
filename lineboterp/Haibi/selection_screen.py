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
def report_list_selectionscreen(): # 報表管理
    report_list_screen = []
    cost = {
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
                    "text": "成本統計",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "※月統計",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "md",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "※年統計",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "md",
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
                    "label": "成本統計列表",
                    "text": "【成本統計】列表"
                    },
                    "color": "#1a9879",
                    "style": "primary"
                }
                ],
                "flex": 0
            }
            }
    report_list_screen.append(cost)
    profit = {
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
                        "text": "利潤統計",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
                    },
                {
                    "type": "text",
                    "text": "※月統計",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "md",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "※年統計",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "md",
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
                        "label": "利潤統計列表",
                        "text": "【利潤統計】列表"
                        },
                        "color": "#c42149",
                        "style": "primary"
                    }
                    ],
                    "flex": 0
                }
                }
    report_list_screen.append(profit)
    popular_products = {
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
                        "text": "熱門商品統計",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
                    },
                {
                    "type": "text",
                    "text": "※月統計",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "md",
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
                        "label": "熱門商品統計列表",
                        "text": "【熱門商品統計】列表"
                        },
                        "color": "#c42149",
                        "style": "primary"
                    }
                    ],
                    "flex": 0
                }
                }
    report_list_screen.append(popular_products)
    screen =FlexSendMessage(
                            alt_text='報表管理',
                            contents={
                                "type": "carousel",
                                "contents": report_list_screen   
                                } 
                            )
    return screen
def Report_statistics_selectionscreen(queryObject): # 報表管理各項統計
    Report_statistics_screen = []
    if queryObject == '熱門商品':
        popular_products_monthly = {
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
                        "text": "熱門商品月統計",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "※各廠商熱賣商品",
                        "wrap": True,
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "margin": "md",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "可自行選擇月份",
                        "wrap": True,
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "margin": "sm",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "十年範圍",
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
                        "label": "熱門商品月統計",
                        "text": "【熱門商品月統計】列表"
                        },
                        "color": "#1a9879",
                        "style": "primary"
                    }
                    ],
                    "flex": 0
                }
                }
        Report_statistics_screen.append(popular_products_monthly)
    else:
        monthly = {
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
                    "text": f"{queryObject}月統計",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"※該月{queryObject}統計",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "md",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "可自行選擇月份",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "sm",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "十年範圍",
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
                    "label": f"{queryObject}月統計",
                    "text": f"{queryObject}月統計"
                    },
                    "color": "#1a9879",
                    "style": "primary"
                }
                ],
                "flex": 0
            }
            }
        Report_statistics_screen.append(monthly)
        yearly = {
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
                            "text": f"{queryObject}年統計",
                            "weight": "bold",
                            "size": "xl",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": f"※該年{queryObject}統計",
                            "wrap": True,
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "margin": "md",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": "可自行選擇年份",
                            "wrap": True,
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "margin": "sm",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": "十年範圍",
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
                            "label": f"{queryObject}年統計",
                            "text": f"{queryObject}年統計"
                            },
                            "color": "#c42149",
                            "style": "primary"
                        }
                        ],
                        "flex": 0
                    }
                    }
        Report_statistics_screen.append(yearly)    
    screen =FlexSendMessage(
                            alt_text='成本/利潤報表統計',
                            contents={
                                "type": "carousel",
                                "contents": Report_statistics_screen   
                                } 
                            )
    return screen