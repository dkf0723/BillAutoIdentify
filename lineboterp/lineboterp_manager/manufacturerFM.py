from linebot.models import FlexSendMessage,TextSendMessage
import manager
from database import wisheslistdb
#廠商管理列表與新增選擇畫面
def Manufacturer_list_and_new_chosen_screen():
    manufacturer_list_and_new_chosen_screen = []
    info1 = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/VpkoVwC.jpg",
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
                    "text": "查詢廠商",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "※廠商資料列表",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "md",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "※廠商資料修改",
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
                    "label": "廠商列表",
                    "text": "【管理廠商】廠商列表"
                    },
                    "color": "#5f5f5f",
                    "style": "primary"
                }
                ],
                "flex": 0
            }
            }
    manufacturer_list_and_new_chosen_screen.append(info1)
    info2 = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/CePlNvY.jpg",
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
                    "text": "新增廠商",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "※建立新廠商資料",
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
                    "label": "新增廠商",
                    "text": "【管理廠商】建立廠商"
                    },
                    "color": "#C9B0A8",
                    "style": "primary"
                }
                ],
                "flex": 0
            }
            }
    manufacturer_list_and_new_chosen_screen.append(info2)
    screen =FlexSendMessage(
                            alt_text='廠商列表或新增選擇',
                            contents={
                                "type": "carousel",
                                "contents": manufacturer_list_and_new_chosen_screen  
                                } 
                            )
    return screen
#新增廠商填寫及確認畫面
def Manufacturer_fillin_and_check_screen(errormsg):
    id = manager.user_id
    message_storage = manager.storage
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
            '3.請打字輸入公司市話(區碼)+市話5~8碼：\n區碼名單：02,03,037,04,049,05,06,07,08,089,082,0826,0836。\nex.0224820346、039981564、037748231',
            '4.請打字輸入行動電話：\nex.0952025413',
            '5.請打字輸入付款方式：\nex.現金、匯款',
            '6.請打字輸入行庫代號(數字3碼)或行庫名稱(30字內)，擇一即可',
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
            elif step < 4:
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
                            alt_text='新增廠商填寫或確認',
                            contents={
                                "type": "carousel",
                                "contents": manufacturer_fillin_and_check_screen   
                                } 
                            )
    return screen

#新增廠商建立成功畫面
def Manufacturer_establishment_screen(num,name,principal,localcalls,phone,payment,bankname,bankid,bankaccount):
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
                                "text": f"{localcalls}",
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
                            alt_text='廠商建立成功！',
                            contents={
                                "type": "carousel",
                                "contents": manufacturer_establishment_screen   
                                } 
                            )
    return screen

#廠商資訊修改畫面
def Manufacturer_edit_screen(edittype,errormsg,before):
    manufacturer_edit_screen = []
    id = manager.user_id
    message_storage = manager.storage
    #editfield=廠商名, 負責或對接人, 市話, 電話, 付款方式, 行庫名, 行庫代號, 匯款帳號
    heading = ['廠商名稱','廠商負責或對接人','廠商市話','廠商電話','付款方式','匯款行庫資料','匯款帳號資料']
    contentshow = ['廠商名稱','負責/對接人','廠商市話','廠商電話','付款方式','行庫資料','匯款帳號']
    title = f"修改{heading[edittype-1]}"

    hint = ['1.請打字輸入廠商名稱：\n(20字內)',
            '2.請打字輸入負責人或對接人名稱：\n(10字內)',
            '3.請打字輸入公司市話(區碼)+市話5~8碼：\n區碼名單：02,03,037,04,049,05,06,07,08,089,082,0826,0836。\nex.0224820346、039981564、037748231',
            '4.請打字輸入行動電話：\nex.0952025413',
            '5.請打字輸入付款方式：\nex.現金、匯款',
            '6.請打字輸入行庫代號(數字3碼)或行庫名稱(30字內)，擇一即可',
            '7.請打字輸入行庫帳號：\n(數字14碼內)']#編寫提示訊息
    fillin = []#填寫訊息合併暫存
    if edittype == 6:
        if before[0] == '略過':
                beforeinfo = '(尚無填寫行庫相關內容)'
        else:
            beforeinfo = f"{before[0]}\n{before[1]}"
    else:
        if edittype == 7:
            if before == '略過':
                beforeinfo = '(尚無填寫帳號內容)'
            else:
                beforeinfo = before
        else:
            beforeinfo = before
    fill = {
            "type": "text",
            "text": f"〈修改前內容〉",
            "wrap": True,
            "color": "#3b5a5f",
            "weight": "bold",
            "size": "md"
        }
    fillin.append(fill)
    fill_0 = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": f"{contentshow[edittype-1]}：",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "sm"
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
                    "text": f"{beforeinfo}",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "sm"
                }
                ]
            }
            ]
        }
    fillin.append(fill_0)
    fill_1 = {
                "type": "separator",
                "color": "#564006",
                "margin": "lg"
            }
    fillin.append(fill_1)
    fill_2 = {
            "type": "text",
            "text": f"=>{hint[edittype-1]}",
            "wrap": True,
            "color": "#3b5a5f",
            "weight": "bold"
        }
    fillin.append(fill_2)
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
    if edittype in [3,4]:
        button = {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "略過",
                    "text": "略過"
                    },
                    "height": "sm",
                    "style": "primary",
                    "color": "#696969"
                }
        buttonshow.append(button)

    if edittype == 5:
        button = {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "現金",
                    "text": "現金"
                    },
                    "height": "sm",
                    "style": "primary",
                    "color": "#696969"
                }
        buttonshow.append(button)
        button1 = {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "匯款",
                    "text": "匯款"
                    },
                    "height": "sm",
                    "style": "primary",
                    "margin": "md",
                    "color": "#bcb5bf"
                }
        buttonshow.append(button1)
    
    button2 = {
                "type": "button",
                "action": {
                "type": "message",
                "label": "取消",
                "text": "取消"
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
    manufacturer_edit_screen.append(fillin_screen)
    screen =FlexSendMessage(
                            alt_text='廠商資訊修改',
                            contents={
                                "type": "carousel",
                                "contents": manufacturer_edit_screen   
                                } 
                            )
    return screen

#-------------------許願清單----------------------
def wishes_list():
    wishes_show = ''
    db_wishes_list = wisheslistdb()
    if db_wishes_list == "找不到符合條件的資料。":
        wishes_show = TextSendMessage(text=db_wishes_list)
    else:
        pagemin = manager.list_page[manager.user_id+'許願min']
        pagemax = manager.list_page[manager.user_id+'許願max']#9
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