from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import lineboterp
from database import unitsearch

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

def Order_cart_selectionscreen():
    Order_cart_screen = []
    order = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/2sHROU2.jpg",
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
                    "text": "訂單查詢",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "※未取訂單",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "md",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "※預購訂單(等待中)",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "sm",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "※歷史訂單(已取、取消)",
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
                    "label": "我的訂單",
                    "text": "訂單查詢"
                    },
                    "color": "#668BC4",
                    "style": "primary"
                }
                ],
                "flex": 0
            }
            }
    Order_cart_screen.append(order)
    cart = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/iQ7R4iZ.jpg",
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
                    "text": "購物車",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "※購物車訂單送出建立",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "sm",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "※查看購物車商品清單",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "md",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "※修改購物車商品數量",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "sm",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "※修改購物車商品列表",
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
                    "label": "我的購物車",
                    "text": "查看購物車"
                    },
                    "color": "#FA8072",
                    "style": "primary"
                }
                ],
                "flex": 0
            }
            }
    Order_cart_screen.append(cart)
    screen =FlexSendMessage(
                            alt_text='訂單/購物車選擇',
                            contents={
                                "type": "carousel",
                                "contents": Order_cart_screen   
                                } 
                            )
    return screen

def Notpickedup_preordered_history_selectionscreen():
    Notpickedup_preordered_history_screen = []
    notpickedup = {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://i.imgur.com/hYE8pdn.jpg",
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
                            "text": "未取訂單",
                            "weight": "bold",
                            "size": "xl",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "※未取訂單查詢(最近100筆)",
                            "wrap": True,
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "margin": "md",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": "※未取訂單詳細資訊",
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
                            "label": "查詢",
                            "text": "未取訂單列表"
                            },
                            "color": "#fdd45b",
                            "style": "primary"
                        }
                        ],
                        "flex": 0
                    }
                    }
    Notpickedup_preordered_history_screen.append(notpickedup)
    preordered = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/m0FDioe.jpg",
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
                        "text": "預購訂單",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "※預購訂單查詢(最近100筆)",
                        "wrap": True,
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "margin": "sm",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "※預購訂單詳細資訊",
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
                        "label": "查詢",
                        "text": "預購訂單列表"
                        },
                        "color": "#fdb0a4",
                        "style": "primary"
                    }
                    ],
                    "flex": 0
                }
                }
    Notpickedup_preordered_history_screen.append(preordered)
    history = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/GxO4bmH.jpg",
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
                        "text": "歷史訂單",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "※歷史訂單查詢(最近100筆)",
                        "wrap": True,
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "margin": "sm",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "※歷史訂單詳細資訊",
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
                        "label": "查詢",
                        "text": "歷史訂單列表"
                        },
                        "color": "#bed0c9",
                        "style": "primary"
                    }
                    ],
                    "flex": 0
                }
                }
    Notpickedup_preordered_history_screen.append(history)
    screen =FlexSendMessage(
                            alt_text='未取/預購/歷史訂單選擇',
                            contents={
                                "type": "carousel",
                                "contents": Notpickedup_preordered_history_screen   
                                } 
                            )
    return screen

#現預購訂單(1/2)畫面
def Order_buynow_preorder_screen(product_order_preorder,product_id,product,quickreply,errormsg):
    user_id = lineboterp.user_id
    multiple = lineboterp.storage[user_id+'multiple']
    if product_order_preorder == '現購':
        distinguish = '#1a9879'#綠
        enter = f"=>1.請選擇{product_order_preorder}數量："
    elif product_order_preorder == '預購':
        distinguish = '#c42149'#紅
        enter = f"=>1.請選擇{product_order_preorder}數量({multiple}的倍數)："
    if errormsg == 'no':
        errormsg = '無'
    else:
        errormsg = str(errormsg)
    msg = {
        "type": "text",
        "text": f"◎錯誤：{errormsg}",
        "wrap": True,
        "color": "#c42149",
        "size": "sm",
        "flex": 5,
        "weight": "bold"
        }

    order_buynow_preorder_screen = {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": "高逸嚴選",
                                "color": "#A44528",
                                "size": "sm",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": f"{product_order_preorder}填寫(1/2)",
                                "weight": "bold",
                                "size": "xl",
                                "align": "center",
                                "margin": "xl"
                            },
                            {
                                "type": "separator",
                                "color": f"{distinguish}",
                                "margin": "md"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "margin": "lg",
                                "spacing": "xs",
                                "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "◇商品編號：",
                                            "wrap": True,
                                            "color": "#3b5a5f",
                                            "size": "md",
                                            "flex": 5,
                                            "margin": "sm",
                                            "weight": "bold"
                                        }
                                        ],
                                        "width": "100px"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": f"{product_id}",
                                            "wrap": True,
                                            "color": "#3b5a5f",
                                            "size": "md",
                                            "flex": 5,
                                            "margin": "sm",
                                            "weight": "bold"
                                        }
                                        ]
                                    }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "◇商品名稱：",
                                            "wrap": True,
                                            "color": "#3b5a5f",
                                            "size": "md",
                                            "flex": 5,
                                            "margin": "sm",
                                            "weight": "bold"
                                        }
                                        ],
                                        "width": "100px"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": f"{product}",
                                            "wrap": True,
                                            "color": "#3b5a5f",
                                            "size": "md",
                                            "flex": 5,
                                            "margin": "sm",
                                            "weight": "bold"
                                        }
                                        ]
                                    }
                                    ]
                                },
                                {
                                    "type": "text",
                                    "text": "<下方依序填寫～>",
                                    "wrap": True,
                                    "color": "#3b5a5f",
                                    "size": "md",
                                    "flex": 5,
                                    "margin": "xl",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": f"{enter}",
                                    "wrap": True,
                                    "color": "#3b5a5f",
                                    "size": "md",
                                    "flex": 5,
                                    "margin": "sm",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": "※提示：可以自行輸入更多的數量",
                                    "wrap": True,
                                    "color": "#f6b877",
                                    "size": "sm",
                                    "flex": 5,
                                    "weight": "bold"
                                },
                                msg
                                ]
                            }
                            ],
                            "backgroundColor": "#FCFAF1"
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "md",
                            "contents": [
                            {
                                "type": "button",
                                "style": "link",
                                "height": "sm",
                                "action": {
                                "type": "message",
                                "label": "取消",
                                "text": "取消"
                                }
                            }
                            ],
                            "flex": 0
                        }
                        }
    screen =FlexSendMessage(
                            alt_text=f"{product_order_preorder}填寫(1/2)",
                            contents={
                                "type": "carousel",
                                "contents": [order_buynow_preorder_screen]   
                                },
                            quick_reply = quickreply
                            )
    return screen

#現預購訂單(2/2)畫面
def Order_phonenum_screen(product_order_preorder,product_id,product,errormsg,phone,num):
    unit = unitsearch(product_id)#取得商品單位
    if product_order_preorder == '現購':
        distinguish = '#1a9879'#綠
    elif product_order_preorder == '預購':
        distinguish = '#c42149'#紅
    if errormsg == 'no':
        errormsg = '無'
    else:
        errormsg = str(errormsg)
        
    phone_quick_buttons = []
    if phone != 'no':
        colorchange = '#5F403B'
        quick_buttons = {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                        "type": "message",
                        "label": f"使用{phone}",
                        "text": f"{phone}"
                        },
                        "color": "#A44528"
                    }
        phone_quick_buttons.append(quick_buttons)
    else:
        colorchange = '#A44528'
    quick_buttons = {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "action": {
                    "type": "message",
                    "label": "重新填寫",
                    "text": "重新填寫"
                    },
                    "color": f"{colorchange}"
                }
    phone_quick_buttons.append(quick_buttons)
    quick_buttons = {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "message",
                    "label": "取消",
                    "text": "取消"
                    }
                }
    phone_quick_buttons.append(quick_buttons)

    msg = {
        "type": "text",
        "text": f"◎錯誤：{errormsg}",
        "wrap": True,
        "color": "#c42149",
        "size": "sm",
        "flex": 5,
        "weight": "bold"
        }
    order_phonenum_screen = {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": "高逸嚴選",
                                "color": "#A44528",
                                "size": "sm",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": f"{product_order_preorder}填寫(2/2)",
                                "weight": "bold",
                                "size": "xl",
                                "align": "center",
                                "margin": "xl"
                            },
                            {
                                "type": "separator",
                                "color": f"{distinguish}",
                                "margin": "md"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "margin": "lg",
                                "spacing": "xs",
                                "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "◇商品編號：",
                                            "wrap": True,
                                            "color": "#3b5a5f",
                                            "size": "md",
                                            "flex": 5,
                                            "margin": "sm",
                                            "weight": "bold"
                                        }
                                        ],
                                        "width": "100px"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": f"{product_id}",
                                            "wrap": True,
                                            "color": "#3b5a5f",
                                            "size": "md",
                                            "flex": 5,
                                            "margin": "sm",
                                            "weight": "bold"
                                        }
                                        ]
                                    }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "◇商品名稱：",
                                            "wrap": True,
                                            "color": "#3b5a5f",
                                            "size": "md",
                                            "flex": 5,
                                            "margin": "sm",
                                            "weight": "bold"
                                        }
                                        ],
                                        "width": "100px"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": f"{product}",
                                            "wrap": True,
                                            "color": "#3b5a5f",
                                            "size": "md",
                                            "flex": 5,
                                            "margin": "sm",
                                            "weight": "bold"
                                        }
                                        ]
                                    }
                                    ]
                                },
                                {
                                    "type": "text",
                                    "text": "<下方依序填寫～>",
                                    "wrap": True,
                                    "color": "#3b5a5f",
                                    "size": "md",
                                    "flex": 5,
                                    "margin": "xl",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": f"1.{product_order_preorder}數量：{num}{unit}",
                                    "wrap": True,
                                    "color": "#3b5a5f",
                                    "size": "md",
                                    "flex": 5,
                                    "margin": "sm",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": "=>2.請輸入您的聯絡電話：",
                                    "wrap": True,
                                    "color": "#3b5a5f",
                                    "size": "md",
                                    "flex": 5,
                                    "margin": "sm",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": "※提示：請自行輸入！ex.0952025413",
                                    "wrap": True,
                                    "color": "#f6b877",
                                    "size": "sm",
                                    "flex": 5,
                                    "weight": "bold"
                                },
                                msg
                                ]
                            }
                            ],
                            "backgroundColor": "#FCFAF1"
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "md",
                            "contents": phone_quick_buttons,
                            "flex": 0
                        }
                        }
    screen =FlexSendMessage(
                            alt_text=f"{product_order_preorder}填寫(2/2)",
                            contents={
                                "type": "carousel",
                                "contents": [order_phonenum_screen]   
                                }
                            )
    return screen

#單一訂單確認畫面
def Single_order_confirmation_screen(product_order_preorder,product_id,product,phonenum,num,unit,oderprice,oderdiscount,subtotalin):
    if product_order_preorder == '現購':
        distinguish = '#1a9879'#綠
    elif product_order_preorder == '預購':
        distinguish = '#c42149'#紅
    single_order_confirmation_screen={
                            "type": "bubble",
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "高逸嚴選",
                                    "color": "#A44528",
                                    "size": "sm",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": f"{product_order_preorder}訂單確認",
                                    "weight": "bold",
                                    "size": "xl",
                                    "align": "center",
                                    "margin": "xl"
                                },
                                {
                                    "type": "separator",
                                    "color": f"{distinguish}",
                                    "margin": "md"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "margin": "lg",
                                    "spacing": "xs",
                                    "contents": [
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": "◇商品編號：",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ],
                                            "width": "100px"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": f"{product_id}",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ]
                                        }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": "◇商品名稱：",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ],
                                            "width": "100px"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": f"{product}",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ]
                                        }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": "◇電話號碼：",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ],
                                            "width": "100px"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": f"{phonenum}",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ]
                                        }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": "◇商品單價：",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ],
                                            "width": "100px"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": f"每{unit}{oderprice}元{oderdiscount}",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ]
                                        }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": f"◇{product_order_preorder}數量：",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ],
                                            "width": "100px"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": f"{num}{unit}",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ]
                                        }
                                        ]
                                    },
                                    {
                                        "type": "separator",
                                        "margin": "xl"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"總計：NT${subtotalin}",
                                        "wrap": True,
                                        "color": "#3b5a5f",
                                        "size": "lg",
                                        "flex": 5,
                                        "margin": "sm",
                                        "weight": "bold",
                                        "align": "end"
                                    }
                                    ]
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
                                    "style": "primary",
                                    "height": "sm",
                                    "action": {
                                    "type": "message",
                                    "label": f"送出{product_order_preorder}訂單",
                                    "text": "1"
                                    },
                                    "color": "#A44528"
                                },
                                {
                                    "type": "button",
                                    "style": "link",
                                    "height": "sm",
                                    "action": {
                                    "type": "message",
                                    "label": "取消",
                                    "text": "2"
                                    }
                                }
                                ],
                                "flex": 0
                            }
                            }
    screen =FlexSendMessage(
                            alt_text=f"{product_order_preorder}訂單確認",
                            contents={
                                "type": "carousel",
                                "contents": [single_order_confirmation_screen]   
                                }
                            )
    return screen

#訂單成立訊息
def Order_establishment_message(product_order_preorder,ordernumber,product,product_id,num,unit,total,continue_browsing,oderprice,oderdiscount,phonenum):
    if product_order_preorder == '現購':
        distinguish = '#1a9879'#綠
        takemsg = '已經可以前往「店面取貨」囉～'
    elif product_order_preorder == '預購':
        distinguish = '#c42149'#紅
        takemsg = '於「商品到貨日」傳送取貨提醒～'
    order_establishment_message = {
                            "type": "bubble",
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "高逸嚴選",
                                    "color": "#A44528",
                                    "size": "sm",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": f"{product_order_preorder}訂單已成立！",
                                    "weight": "bold",
                                    "size": "xl",
                                    "align": "center",
                                    "margin": "xl"
                                },
                                {
                                    "type": "text",
                                    "text": f"訂單編號：{ordernumber}",
                                    "weight": "bold",
                                    "size": "md",
                                    "align": "center",
                                    "margin": "sm",
                                    "color": f"{distinguish}"
                                },
                                {
                                    "type": "separator",
                                    "color": f"{distinguish}",
                                    "margin": "md"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "margin": "lg",
                                    "spacing": "xs",
                                    "contents": [
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": "◇商品編號：",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ],
                                            "width": "100px"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": f"{product_id}",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ]
                                        }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": "◇商品名稱：",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ],
                                            "width": "100px"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": f"{product}",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ]
                                        }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": "◇電話號碼：",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ],
                                            "width": "100px"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": f"{phonenum}",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ]
                                        }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": "◇商品單價：",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ],
                                            "width": "100px"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": f"每{unit}{oderprice}元{oderdiscount}",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ]
                                        }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": "◇現購數量：",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ],
                                            "width": "100px"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": f"{num}{unit}",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ]
                                        }
                                        ]
                                    },
                                    {
                                        "type": "separator",
                                        "margin": "xl"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"總計：NT${total}",
                                        "wrap": True,
                                        "color": "#3b5a5f",
                                        "size": "lg",
                                        "flex": 5,
                                        "margin": "sm",
                                        "weight": "bold",
                                        "align": "end"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"\n{takemsg}",
                                        "wrap": True,
                                        "color": "#fb5840",
                                        "size": "md",
                                        "flex": 5,
                                        "margin": "sm",
                                        "weight": "bold",
                                        "align": "center"
                                    }
                                    ]
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
                                    "style": "primary",
                                    "height": "sm",
                                    "action": {
                                    "type": "message",
                                    "label": f"繼續瀏覽{product_order_preorder}商品",
                                    "text": f"{continue_browsing}"
                                    },
                                    "color": "#A44528"
                                }
                                ],
                                "flex": 0
                            }
                            }
    screen =FlexSendMessage(
                            alt_text=f"{product_order_preorder}訂單成立！",
                            contents={
                                "type": "carousel",
                                "contents": [order_establishment_message]   
                                }
                            )
    return screen

#購物車商品新增(1/1)畫面
def Cart_add_screen(product_id,product,quickreply,errormsg):
    if errormsg == 'no':
        errormsg = '無'
    else:
        errormsg = str(errormsg)
    msg = {
        "type": "text",
        "text": f"◎錯誤：{errormsg}",
        "wrap": True,
        "color": "#c42149",
        "size": "sm",
        "flex": 5,
        "weight": "bold"
        }

    cart_add_screen = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "高逸嚴選",
                            "color": "#A44528",
                            "size": "sm",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": "購物車新增(1/1)",
                            "weight": "bold",
                            "size": "xl",
                            "align": "center",
                            "margin": "xl"
                        },
                        {
                            "type": "separator",
                            "color": "#FC7000",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "xs",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "◇商品編號：",
                                        "wrap": True,
                                        "color": "#3b5a5f",
                                        "size": "md",
                                        "flex": 5,
                                        "margin": "sm",
                                        "weight": "bold"
                                    }
                                    ],
                                    "width": "100px"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": f"{product_id}",
                                        "wrap": True,
                                        "color": "#3b5a5f",
                                        "size": "md",
                                        "flex": 5,
                                        "margin": "sm",
                                        "weight": "bold"
                                    }
                                    ]
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "◇商品名稱：",
                                        "wrap": True,
                                        "color": "#3b5a5f",
                                        "size": "md",
                                        "flex": 5,
                                        "margin": "sm",
                                        "weight": "bold"
                                    }
                                    ],
                                    "width": "100px"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": f"{product}",
                                        "wrap": True,
                                        "color": "#3b5a5f",
                                        "size": "md",
                                        "flex": 5,
                                        "margin": "sm",
                                        "weight": "bold"
                                    }
                                    ]
                                }
                                ]
                            },
                            {
                                "type": "text",
                                "text": "<下方依序填寫～>",
                                "wrap": True,
                                "color": "#3b5a5f",
                                "size": "md",
                                "flex": 5,
                                "margin": "xl",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": "=>請選擇加入數量：",
                                "wrap": True,
                                "color": "#3b5a5f",
                                "size": "md",
                                "flex": 5,
                                "margin": "sm",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": "※提示：可以自行輸入更多的數量",
                                "wrap": True,
                                "color": "#f6b877",
                                "size": "sm",
                                "flex": 5,
                                "weight": "bold"
                            },
                            msg
                            ]
                        }
                        ],
                        "backgroundColor": "#FCFAF1"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "md",
                        "contents": [
                        {
                            "type": "button",
                            "style": "link",
                            "height": "sm",
                            "action": {
                            "type": "message",
                            "label": "取消",
                            "text": "取消"
                            }
                        }
                        ],
                        "flex": 0
                    }
                    }
    screen =FlexSendMessage(
                            alt_text="購物車新增(1/1)",
                            contents={
                                "type": "carousel",
                                "contents": [cart_add_screen]   
                                },
                            quick_reply = quickreply
                            )
    return screen

#購物車商品加入成功訊息
def Cart_join_success_message(product,product_id,num,unit,continue_browsing):
    cart_join_success_message = {
                            "type": "bubble",
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "高逸嚴選",
                                    "color": "#A44528",
                                    "size": "sm",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": "購物車加入成功！",
                                    "weight": "bold",
                                    "size": "xl",
                                    "align": "center",
                                    "margin": "xl"
                                },
                                {
                                    "type": "separator",
                                    "color": "#FC7000",
                                    "margin": "md"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "margin": "lg",
                                    "spacing": "xs",
                                    "contents": [
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": "◇商品編號：",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ],
                                            "width": "100px"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": f"{product_id}",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ]
                                        }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": "◇商品名稱：",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ],
                                            "width": "100px"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": f"{product}",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ]
                                        }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": "◇加入數量：",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ],
                                            "width": "100px"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": f"{num}{unit}",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "size": "md",
                                                "flex": 5,
                                                "margin": "sm",
                                                "weight": "bold"
                                            }
                                            ]
                                        }
                                        ]
                                    }
                                    ]
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
                                    "style": "primary",
                                    "height": "sm",
                                    "action": {
                                    "type": "message",
                                    "label": "繼續瀏覽現購商品",
                                    "text": f"{continue_browsing}"
                                    },
                                    "color": "#A44528"
                                },
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "height": "sm",
                                    "action": {
                                    "type": "message",
                                    "label": "查看購物車",
                                    "text": "查看購物車"
                                    },
                                    "color": "#5F403B"
                                }
                                ],
                                "flex": 0
                            }
                            }
    screen =FlexSendMessage(
                            alt_text="購物車加入成功！",
                            contents={
                                "type": "carousel",
                                "contents": [cart_join_success_message]   
                                }
                            )
    return screen

#單一現預購訂單取消、加入購物車失敗或取消(推薦)
def Cancel_fail_message(ordertype):
    user_id = lineboterp.user_id
    list_page = lineboterp.list_page
    if ordertype == '現購':
        if (user_id+'現購min') not in list_page:
            now_pagemin = list_page[user_id+'現購min'] = 0
            now_pagemax = list_page[user_id+'現購max'] = 9
        else:
            now_pagemin = list_page[user_id+'現購min']
            now_pagemax = list_page[user_id+'現購max']
    else:
        now_pagemin = list_page[user_id+'現購min'] = 0
        now_pagemax = list_page[user_id+'現購max'] = 9
        
    if ordertype == '預購':
        if (user_id+'預購min') not in list_page:
            preorder_pagemin = list_page[user_id+'預購min'] = 0
            preorder_pagemax = list_page[user_id+'預購max'] = 9
        else:
            preorder_pagemin = list_page[user_id+'預購min']
            preorder_pagemax = list_page[user_id+'預購max']
    else:
        preorder_pagemin = list_page[user_id+'預購min'] = 0
        preorder_pagemax = list_page[user_id+'預購max'] = 9
        
    now_continue_browsing = "【現購列表下一頁】"+ str(now_pagemin+1) +"～"+ str(now_pagemax)
    preorder_continue_browsing = "【預購列表下一頁】"+ str(preorder_pagemin+1) +"～"+ str(preorder_pagemax)
    cancel_fail_message = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "高逸嚴選",
                            "color": "#A44528",
                            "size": "sm",
                            "weight": "bold"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": "繼續瀏覽商品",
                                "color": "#3b5a5f",
                                "weight": "bold",
                                "style": "italic",
                                "align": "center",
                                "size": "xl"
                            }
                            ],
                            "margin": "md"
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
                            "style": "primary",
                            "height": "sm",
                            "action": {
                            "type": "message",
                            "label": "現購商品",
                            "text": f"{now_continue_browsing}"
                            },
                            "color": "#A44528"
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "height": "sm",
                            "action": {
                            "type": "message",
                            "label": "預購商品",
                            "text": f"{preorder_continue_browsing}"
                            },
                            "color": "#5F403B"
                        }
                        ],
                        "flex": 0
                    }
                    }
    screen =FlexSendMessage(
                            alt_text="動作取消/失敗後推薦",
                            contents={
                                "type": "carousel",
                                "contents": [cancel_fail_message]   
                                }
                            )
    return screen

def Cart_order_screen(phone,errormsg):
    if errormsg == 'no':
        errormsg = '無'
    else:
        errormsg = str(errormsg)
        
    phone_quick_buttons = []
    if phone != 'no':
        quick_buttons = {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                        "type": "message",
                        "label": f"使用{phone}",
                        "text": f"{phone}"
                        },
                        "color": "#A44528"
                    }
        phone_quick_buttons.append(quick_buttons)
    quick_buttons = {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "message",
                    "label": "取消",
                    "text": "取消"
                    }
                }
    phone_quick_buttons.append(quick_buttons)

    msg = {
        "type": "text",
        "text": f"◎錯誤：{errormsg}",
        "wrap": True,
        "color": "#c42149",
        "size": "sm",
        "flex": 5,
        "weight": "bold"
        }
    cart_order_screen = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "高逸嚴選",
                            "color": "#A44528",
                            "size": "sm",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": "購物車訂單填寫(1/1)",
                            "weight": "bold",
                            "size": "xl",
                            "align": "center",
                            "margin": "xl"
                        },
                        {
                            "type": "separator",
                            "color": "#77105b",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "xs",
                            "contents": [
                            {
                                "type": "text",
                                "text": "=>請輸入您的行動電話：",
                                "wrap": True,
                                "color": "#3b5a5f",
                                "size": "lg",
                                "flex": 5,
                                "margin": "sm",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": "※提示：請自行輸入！ex.0952025413",
                                "wrap": True,
                                "color": "#f6b877",
                                "size": "sm",
                                "flex": 5,
                                "weight": "bold"
                            },
                            msg
                            ]
                        }
                        ],
                        "backgroundColor": "#FCFAF1"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "md",
                        "contents": phone_quick_buttons,
                        "flex": 0
                    }
                    }
    screen =FlexSendMessage(
                            alt_text="購物車訂單填寫(1/1)",
                            contents={
                                "type": "carousel",
                                "contents": [cart_order_screen]   
                                }
                            )
    return screen