from linebot.models import TextSendMessage,FlexSendMessage,QuickReplyButton,MessageAction,QuickReply
import lineboterp
from database import QAsearch,QAsearchinfo,wisheslistdb#wisheslistdb未來刪除
#常見類、操作類、商品類、訂單類
def ask():
    Ask_screen = []
    operate = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/oq41k9G.jpg",
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
                    "url": "https://i.imgur.com/n17c49n.jpg",
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
                    "url": "https://i.imgur.com/BErjdwI.jpg",
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
                        "color": "#fdd45b",
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
                "url": "https://i.imgur.com/m2waPov.jpg",
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
                    "color": "#912B07",
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

        if searchtype == '操作類':
            color = '#fe587b'
        elif searchtype == '商品類':
            color = '#8FBC8F'
        elif searchtype == '訂單類':
            color = '#FF8C00'#黃澄
        elif searchtype == '常見類':
            color = '#912B07'#橘

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
                    "color": f"{color}"
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

#-------------------許願清單----------------------
def wishes_list():
    wishes_show = ''
    db_wishes_list = wisheslistdb()
    if db_wishes_list == "找不到符合條件的資料。":
        wishes_show = TextSendMessage(text=db_wishes_list)
    else:
        pagemin = lineboterp.list_page[lineboterp.user_id+'許願min']
        pagemax = lineboterp.list_page[lineboterp.user_id+'許願max']#9
        db_preorder = db_wishes_list[pagemin:pagemax] #最多九個+1more
        #商品圖片,商品名稱,會員_LINE_ID,推薦原因,願望建立時間,資料來源
        show =[]#輸出全部
        wishes_img = []#商品圖片
        wishes_name = []#商品名稱
        wishes_member = []#會員_LINE_ID
        wishes_reason = []#推薦原因
        wishes_timein = []#願望建立時間
        wishes_source = []#願望來源
        wishes_sourcecheck = []#願望來源判斷
        for db_wishes_list in db_preorder:
            if db_wishes_list[0] is None:
                break
            else:
                if (db_wishes_list[0] is None) or (db_wishes_list[0][:4] != 'http'):
                    img = 'https://i.imgur.com/rGlTAt3.jpg'
                else:
                    img = db_wishes_list[0]#商品圖片
                wishes_img.append(img)
                name = db_wishes_list[1]#商品名稱
                wishes_name.append(name)
                member = db_wishes_list[2]#會員_LINE_ID
                wishes_member.append(member)
                reason = db_wishes_list[3]#推薦原因
                wishes_reason.append(reason)
                timein = db_wishes_list[4]#願望建立時間
                wishes_timein.append(timein)
                source = db_wishes_list[5]#願望來源
                wishes_source.append(source)
                if 'http' in db_wishes_list[5]:
                    sourcecheck = '連結'#願望來源
                else:
                    sourcecheck = db_wishes_list[5]#願望來源判斷
                wishes_sourcecheck.append(sourcecheck)
        for i in range(len(wishes_img)):
            source_button = []
            if '連結' in wishes_sourcecheck[i]:
                source_button.append({
                                "type": "button",
                                "action": {
                                "type": "uri",
                                "label": "前往連結資料來源",
                                "uri": f"{wishes_source[i]}"
                                },
                                "style": "primary",
                                "color": "#5f5f5f",
                                "height": "sm"
                            })
            show.append({
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": f"{wishes_img[i]}",
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
                                "text": f"{wishes_name[i]}",
                                "weight": "bold",
                                "size": "xl",
                                "align": "center",
                                "color": "#5f5f5f",
                                "wrap": True,
                                "offsetBottom": "sm"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": f"{wishes_member[i]}",
                                    "wrap": True,
                                    "size": "sm",
                                    "align": "center",
                                    "color": "#ffffff"
                                }
                                ],
                                "backgroundColor": "#C9B0A8",
                                "cornerRadius": "xxl"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "separator",
                                    "margin": "lg"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "lg",
                                    "spacing": "sm",
                                    "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "◇推薦來源：",
                                            "color": "#3b5a5f",
                                            "size": "md",
                                            "flex": 5,
                                            "margin": "sm",
                                            "weight": "bold"
                                        }
                                        ],
                                        "maxWidth": "95px"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": f"{wishes_sourcecheck[i]}",
                                            "offsetTop": "sm",
                                            "wrap": True
                                        }
                                        ]
                                    }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "sm",
                                    "spacing": "sm",
                                    "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "◇推薦原因：",
                                            "color": "#3b5a5f",
                                            "size": "md",
                                            "flex": 5,
                                            "margin": "sm",
                                            "weight": "bold"
                                        }
                                        ],
                                        "maxWidth": "95px"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": f"{wishes_reason[i]}",
                                            "offsetTop": "sm",
                                            "wrap": True
                                        }
                                        ]
                                    }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "xxl",
                                    "spacing": "sm",
                                    "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": f"{wishes_timein[i]}",
                                            "offsetTop": "sm",
                                            "color": "#5f5f5f",
                                            "align": "end",
                                            "size": "sm"
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
                            "contents": source_button
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
                                "text": "【許願列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
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
                                "label": "已經到底囉！'點我'重新瀏覽",
                                "text": "【報表管理】許願清單"
                            }
                        }
                    ]
                }
            })
        wishes_show = FlexSendMessage(
                        alt_text='【許願清單】列表',
                        contents={
                            "type": "carousel",
                            "contents": show      
                            } 
                        )
    return wishes_show