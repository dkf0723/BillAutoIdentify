from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import lineboterp

#新增廠商填寫及確認畫面
def Manufacturer_fillin_and_check_screen(errormsg):
    id = lineboterp.user_id
    message_storage = lineboterp.storage
    edit_step = message_storage[id+'Manufacturer_edit_step']#編寫到第幾步驟
    if edit_step <= 4:
        title = f"廠商資料填寫({str(edit_step+1)}/5)"
    elif edit_step in [5,6]:
        if edit_step == 5:
            num = '1'
        else:
            num = '2'
        title = f"廠商付款資料填寫({num}/2)"
    else: #8
        title = "廠商資料確認"
    manufacturer_fillin_and_check_screen = []
    hint = ['2.請打字輸入負責人或對接人名稱：\n(10字內)',
            '3.請打字輸入公司市話(0+2~3碼)+7碼：\nex.039981234、0379981234、08269981234、略過',
            '4.請打字輸入行動電話：\nex.0952025413、略過',
            '5.請打字輸入付款方式：\nex.現金、匯款',
            '6.請打字輸入行庫代號(數字3碼)或行庫名稱(30字內)，則一即可',
            '8.請打字輸入行庫帳號：\n(數字14碼內)']#編寫提示訊息
    Completed = ['廠商名稱','負責/對接人','公司市話','行動電話','付款方式','行庫代號','行庫名稱','匯款帳號']#填寫後的欄位顯示
    field_value = ['manufacturer_name','manufacturer_principal','manufacturer_localcalls','manufacturer_phonenum',
                   'manufacturer_Payment','manufacturer_bankid','manufacturer_bankname','manufacturer_bankaccount']
    fillin = []#填寫訊息合併暫存
    if edit_step == 0:
        fill = {
                "type": "text",
                "text": "=>1.請打字輸入廠商名稱：\n(20字內)",
                "wrap": True,
                "color": "#3b5a5f",
                "weight": "bold"
            }
        fillin.append(fill)
    else:#1~8
        if edit_step == 8:
            if message_storage[id+'manufacturer_Payment'] == '現金':
                showstep = 5
            elif message_storage[id+'manufacturer_Payment'] == '匯款':
                showstep = 8
        else:
            showstep = edit_step
        for step in range(showstep): #0~5,7
            #負責人長度不同判斷
            if step == 4:
                hintshow = hint[4]
            elif step <= 5:
                hintshow = hint[step]
            else:
                hintshow = hint[5]

            if step != 1:#除了負責人
                max = '100'
            else:
                max = '120'

            show = {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": f"◇{Completed[step]}：",
                            "wrap": True,
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "margin": "sm",
                            "weight": "bold"
                        }
                        ],
                        "width": f"{max}px"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": f"{message_storage[id+field_value[step]]}",
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
            fillin.append(show)
            if (step == 5) and (edit_step != 8) :#確認前的填寫步驟
                show = {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": f"◇{Completed[6]}：",
                            "wrap": True,
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "margin": "sm",
                            "weight": "bold"
                        }
                        ],
                        "width": f"{max}px"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": f"{message_storage[id+field_value[6]]}",
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
                fillin.append(show)
        if edit_step != 8:    
            fill_3 = {
                    "type": "text",
                    "text": f"=>{hintshow}",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "weight": "bold"
                }
            fillin.append(fill_3)
    if errormsg != '':
        fill_4 = {
                    "type": "text",
                    "text": f"★錯誤：{errormsg}",
                    "wrap": True,
                    "color": "#c42149",
                    "margin": "md"
                }
        fillin.append(fill_4)

    #按鈕
    buttonshow = []
    color = '#696969'

    if edit_step in [2,3,4]:
        if edit_step in [2,3]:
            changelabel = '略過'
            changetext = '略過'
        else:
            changelabel = '現金'
            changetext = '現金'
        color = '#bcb5bf'
        button = {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": f"{changelabel}",
                    "text": f"{changetext}"
                    },
                    "height": "sm",
                    "style": "primary",
                    "color": "#696969"
                }
        buttonshow.append(button)

    labelshow = '重新填寫'
    txtshow = '重新填寫'
    msgshow = '取消'
    if edit_step == 8:
        txtshow = '1'
        msgshow = '2'
        labelshow = '送出'
    if edit_step == 4:
        txtshow = '匯款'
        labelshow = '匯款'
    if edit_step != 0:
        button1 = {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": f"{labelshow}",
                    "text": f"{txtshow}"
                    },
                    "height": "sm",
                    "style": "primary",
                    "margin": "md",
                    "color": f"{color}"
                }
        buttonshow.append(button1)
    
    button2 = {
                "type": "button",
                "action": {
                "type": "message",
                "label": "取消",
                "text": f"{msgshow}"
                },
                "margin": "md"
            }
    buttonshow.append(button2)
                        
    fillin_screen = {
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
                            "text": f"{title}",
                            "weight": "bold",
                            "size": "xl",
                            "align": "center",
                            "margin": "xl"
                        },
                        {
                            "type": "separator",
                            "color": "#564006",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "xs",
                            "contents": fillin,
                            "backgroundColor": "#F5F5F5"
                        }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": buttonshow
                    }
                    }

    manufacturer_fillin_and_check_screen.append(fillin_screen)
    screen =FlexSendMessage(
                            alt_text='現/預購商品選擇',
                            contents={
                                "type": "carousel",
                                "contents": manufacturer_fillin_and_check_screen   
                                } 
                            )
    return screen

#新增廠商建立成功畫面
def Manufacturer_establishment_screen(num,name,principal,localcalls,phone,payment,bankid,bankname,bankaccount):
    #廠商編號, 廠商名, 負責或對接人, 市話, 電話, 付款方式, 行庫名, 行庫代號, 匯款帳號
    manufacturer_establishment_screen = []

    payinfo = []
    show0 = {
            "type": "separator",
            "margin": "md"
        }
    payinfo.append(show0)
    if payment == '匯款':
        show1 = {
                "type": "text",
                "text": "▼匯款資訊",
                "wrap": True,
                "color": "#3b5a5f",
                "size": "md",
                "flex": 5,
                "margin": "sm",
                "weight": "bold",
                "offsetTop": "xs"
            }
        payinfo.append(show1)
        show2 = {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "行庫代號：",
                        "offsetStart": "xl",
                        "color": "#3b5a5f"
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
                        "wrap": True,
                        "text": f"{bankid}",
                        "color": "#3b5a5f"
                    }
                    ]
                }
                ]
            }
        payinfo.append(show2)
        show3 = {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "行庫名稱：",
                        "offsetStart": "xl",
                        "color": "#3b5a5f"
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
                        "text": f"{bankname}",
                        "wrap": True,
                        "color": "#3b5a5f"
                    }
                    ]
                }
                ]
            }
        payinfo.append(show3)
        show4 = {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "匯款帳號：",
                        "offsetStart": "xl",
                        "color": "#3b5a5f"
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
                        "text": f"{bankaccount}",
                        "wrap": True,
                        "color": "#3b5a5f"
                    }
                    ]
                }
                ]
            }
        payinfo.append(show4)
    
    if localcalls != '略過':
        localcall = f"({localcalls[:-7]}){localcalls[-7:]}"
    else:
        localcall = localcalls
    showall = {
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
                    "text": "廠商成功建立！",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "margin": "xl"
                },
                {
                    "type": "text",
                    "text": f"廠商編號：{num}",
                    "weight": "bold",
                    "size": "md",
                    "align": "center",
                    "margin": "sm",
                    "color": "#564006"
                },
                {
                    "type": "separator",
                    "color": "#564006",
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
                                "text": "◇廠商名稱：",
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
                                "text": f"{name}",
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
                                "text": "◇負責/對接人：",
                                "wrap": True,
                                "color": "#3b5a5f",
                                "size": "md",
                                "flex": 5,
                                "margin": "sm",
                                "weight": "bold"
                            }
                            ],
                            "width": "120px"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": f"{principal}",
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
                                "text": "◇公司市話：",
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
                                "text": f"{localcall}",
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
                                "text": "◇行動電話：",
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
                                "text": f"{phone}",
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
                                "text": "◇付款方式：",
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
                                "text": f"{payment}",
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
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": payinfo
                }
                ]
            }
            }
    manufacturer_establishment_screen.append(showall)
    screen =FlexSendMessage(
                            alt_text='現/預購商品選擇',
                            contents={
                                "type": "carousel",
                                "contents": manufacturer_establishment_screen   
                                } 
                            )
    return screen

#廠商列表畫面
'''def Manufacturer_list_screen():
    manufacturer_list_screen = []
    mlist = {}
    mlist.append()
    manufacturer_list_screen.append()
    screen =FlexSendMessage(
                            alt_text='現/預購商品選擇',
                            contents={
                                "type": "carousel",
                                "contents": manufacturer_list_screen   
                                } 
                            )
    return screen'''