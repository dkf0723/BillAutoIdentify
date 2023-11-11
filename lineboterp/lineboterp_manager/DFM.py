from linebot.models import FlexSendMessage
#-------------顧客取貨一開始的畫面-------
def Customer_pickup():
    customer_pickup = []
    info1 =  {
            "type": "bubble",
            "hero": {
                "type": "image",
                "aspectRatio": "20:13",
                "url": "https://i.imgur.com/UXBDb1Y.jpg",
                "align": "center",
                "margin": "none",
                "animated": True,
                "aspectMode": "fit",
                "size": "full",
                "offsetTop": "xxl"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "手機後三碼",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "※",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "※",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
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
                    "action": {
                    "type": "message",
                    "text": "【取貨】手機後三碼",
                    "label": "後三碼"
                    },
                    "height": "sm",
                    "color": "#FCA310"
                }
                ],
                "flex": 0,
                "margin": "sm"
            }
            }
    customer_pickup.append(info1)
    screen =FlexSendMessage(
                            alt_text='商品管理服務選擇',
                            contents={
                                "type": "carousel",
                                "contents": customer_pickup  
                                } 
                            )
    return screen
def Report_management():
    Report_management = []
    info1 = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "aspectRatio": "20:13",
                "url": "https://i.imgur.com/V8091Bp.jpg",
                "align": "center",
                "margin": "none",
                "animated": True,
                "aspectMode": "fit",
                "size": "full",
                "offsetTop": "md"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "報表管理",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "※多種報表檢視經營成果",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "※可選擇時間範圍：單一年或單一月",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
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
                    "action": {
                    "type": "message",
                    "text": "【報表管理】報表管理",
                    "label": "報表管理"
                    },
                    "height": "sm",
                    "color": "#5bb09b",
                    "offsetTop": "none"
                }
                ],
                "flex": 0,
                "margin": "sm"
            }
            }
    Report_management.append(info1)
    info2 =  {
            "type": "bubble",
            "hero": {
                "type": "image",
                "aspectRatio": "20:13",
                "url": "https://i.imgur.com/rZ6Wic2.jpg",
                "align": "center",
                "margin": "none",
                "animated": True,
                "aspectMode": "cover",
                "size": "full",
                "offsetTop": "none"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "許願清單",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "※列出客戶的許願商品",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
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
                    "action": {
                    "type": "message",
                    "text": "【報表管理】許願清單",
                    "label": "許願清單"
                    },
                    "height": "sm",
                    "color": "#5bb09b",
                    "offsetTop": "none"
                }
                ],
                "flex": 0,
                "margin": "sm"
            }
            }
    Report_management.append(info2)
    screen =FlexSendMessage(
                            alt_text='商品管理服務選擇',
                            contents={
                                "type": "carousel",
                                "contents": Report_management  
                                } 
                            )
    return screen
