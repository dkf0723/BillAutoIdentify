from linebot.models import TextSendMessage,FlexSendMessage,QuickReplyButton,MessageAction,QuickReply
import lineboterp
from database import QAsearch,QAsearchinfo
#常見類、操作類、商品類、訂單類
def ask():
    Ask_screen = []
    operate = {
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
                        "text": "操作類QA",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
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
                        "label": "操作類",
                        "text": "【QA列表】操作類"
                        },
                        "color": "#fdb0a4",
                        "style": "primary"
                    }
                    ],
                    "flex": 0
                }
                }
    Ask_screen.append(operate)
    commodity = {
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
                        "text": "商品類QA",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
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
                        "label": "商品類",
                        "text": "【QA列表】商品類"
                        },
                        "color": "#bed0c9",
                        "style": "primary"
                    }
                    ],
                    "flex": 0
                }
                }
    Ask_screen.append(commodity)
    order = {
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
                        "text": "訂單類QA",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
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
                        "label": "訂單類",
                        "text": "【QA列表】訂單類"
                        },
                        "color": "#bed0c9",
                        "style": "primary"
                    }
                    ],
                    "flex": 0
                }
                }
    Ask_screen.append(order)
    common_problem = {
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
                    "text": "常見類QA",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
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
                    "label": "常見類",
                    "text": "【QA列表】常見類"
                    },
                    "color": "#fdd45b",
                    "style": "primary"
                }
                ],
                "flex": 0
            }
            }
    Ask_screen.append(common_problem)
    screen =FlexSendMessage(
                            alt_text='QA四類別選擇',
                            contents={
                                "type": "carousel",
                                "contents": Ask_screen   
                                } 
                            )
    return screen
#-------------------列表----------------------
def qasearch_list(searchtype):#類別
    db_qasearch = QAsearch(searchtype)
    if db_qasearch=='找不到符合條件的資料。':
        qasearch_show = TextSendMessage(text='尚未有此類別QA資料')
    else:
        qasearch_show = []#發送全部
        orderqasearch_handlelist = []#處理切割db_qasearch資料10筆一組

        # 迴圈每次取出10個元素，並將這兩個元素作為一個子陣列存入結果陣列中，直到取完為止
        while len(db_qasearch) > 0:
            two_elements = db_qasearch[:10]  # 取得10個元素
            orderqasearch_handlelist.append(two_elements)  # 將10個元素作為一個子陣列加入結果陣列
            db_qasearch = db_qasearch[10:]  # 移除已取得的元素

        for totallist in orderqasearch_handlelist:
            #UID,問題
            buttons = []  # #模塊中10筆資料
            for i in range(len(totallist)):
                button = {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": f"{totallist[i][1]}",
                        "text": f"【QA詳細】{totallist[i][0]}"
                    },
                    "color": "#FF8C00"
                }
                buttons.append(button)

            qasearch_show.append({
                    "type": "bubble",
                    "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": "高逸嚴選",
                        "weight": "bold",
                        "color": "#A44528",
                        "size": "sm"
                        },
                        {
                        "type": "text",
                        "text": f"{searchtype}QA查詢",
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
                        "contents": buttons
                        }
                    ]
                    },
                    "styles": {
                    "footer": {
                        "separator": True
                    }
                    }
                })
        
        qasearch_show = FlexSendMessage(
            alt_text=f"{searchtype}QA查詢",
            contents={
                "type": "carousel",
                "contents": qasearch_show      
                } 
            )
    return qasearch_show

#-------------------詳細----------------------
def QAsearchinfoscreen(UID):
    db_qainfo = QAsearchinfo(UID)
    if db_qainfo =='找不到符合條件的資料。':
        qasearch_info = TextSendMessage(text='此QA目前查無資料')
    else:
        #類別,問題,回答
        showout = []
        show = {
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
                        "text": f"{db_qainfo[0][0]}\nQA查詢結果",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "margin": "xl",
                        "color": "#010203",
                        "wrap": True
                    },
                    {
                        "type": "separator",
                        "color": "#010203",
                        "margin": "md"
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
                                "text": "◇問題：",
                                "color": "#3b5a5f",
                                "weight": "bold"
                            }
                            ],
                            "maxWidth": "70px"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": f"{db_qainfo[0][1]}",
                                "wrap": True,
                                "color": "#3b5a5f"
                            }
                            ],
                        }
                        ],
                        "margin": "md"
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
                                "text": "◇回答：",
                                "color": "#3b5a5f",
                                "weight": "bold"
                            }
                            ],
                            "maxWidth": "70px"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": f"{db_qainfo[0][2]}",
                                "wrap": True,
                                "color": "#3b5a5f"
                            }
                            ],
                        }
                        ],
                        "margin": "lg"
                    },
                    {
                        "type": "separator",
                        "color": "#010203",
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
                        "label": "繼續瀏覽QA",
                        "text": "問題提問"
                        },
                        "color": "#A44528"
                    }
                    ],
                    "flex": 0
                }
                }
        showout.append(show)
        qasearch_info = FlexSendMessage(
            alt_text=f"{db_qainfo[0][0]}QA查詢結果",
            contents={
                "type": "carousel",
                "contents": showout     
                } 
            )
    return qasearch_info