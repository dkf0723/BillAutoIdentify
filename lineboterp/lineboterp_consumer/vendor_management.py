from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import lineboterp
from database import Manufacturer,Manufacturer_single

#廠商列表
def Manufacturer_list():
    Manufacturer_list_db = Manufacturer()
    #廠商編號, 廠商名, 負責或對接人, 市話, 電話, 付款方式, 行庫名, 行庫代號, 匯款帳號
    #num,name,principal,localcalls,phone,payment,bankname,bankid,bankaccount
    if Manufacturer_list_db != 'no':
        pagemin = lineboterp.list_page[lineboterp.user_id+'廠商列表min']
        pagemax = lineboterp.list_page[lineboterp.user_id+'廠商列表max']#9
        db_manufacturer = Manufacturer_list_db[pagemin:pagemax] #最多九個+1more

        manufacturer_show =[]#輸出全部
        manufacturer_num = []#廠商編號
        manufacturer_name = []#廠商名
        manufacturer_principal = []#負責或對接人
        manufacturer_localcalls = []#市話
        manufacturer_phone = []#電話
        manufacturer_payment = []#付款方式
        manufacturer_bankname = []#行庫名
        manufacturer_bankid = []#行庫代號
        manufacturer_bankaccount = []#匯款帳號
        for db_manufacturer_list in db_manufacturer:
            if db_manufacturer_list[0] is None:
                break
            else:
                num = db_manufacturer_list[0]
                manufacturer_num.append(num)#廠商編號
                name = db_manufacturer_list[1]
                manufacturer_name.append(name)#廠商名
                principal = db_manufacturer_list[2]
                manufacturer_principal.append(principal)#負責或對接人
                localcalls = db_manufacturer_list[3]
                manufacturer_localcalls.append(localcalls)#市話
                phone = db_manufacturer_list[4]
                manufacturer_phone.append(phone)#電話
                payment = db_manufacturer_list[5]
                manufacturer_payment.append(payment)#付款方式
                bankname = db_manufacturer_list[6]
                manufacturer_bankname.append(bankname)#行庫名
                bankid = db_manufacturer_list[7]
                manufacturer_bankid.append(bankid)#行庫代號
                bankaccount = db_manufacturer_list[8]
                manufacturer_bankaccount.append(bankaccount)#匯款帳號
        
        for i in range(len(manufacturer_num)):
            payinfo = []
            show0 = {
                    "type": "separator",
                    "margin": "md"
                }
            payinfo.append(show0)
            if manufacturer_payment[i] == '匯款':
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
                                "text": f"{manufacturer_bankid[i]}",
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
                                "text": f"{manufacturer_bankname[i]}",
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
                                "text": f"{manufacturer_bankaccount[i]}",
                                "wrap": True,
                                "color": "#3b5a5f"
                            }
                            ]
                        }
                        ]
                    }
                payinfo.append(show4)
            
            if manufacturer_localcalls[i] is None:
                localcall = manufacturer_localcalls[i]
            elif manufacturer_localcalls[i] != '略過':
                localcall = f"({manufacturer_localcalls[i][:-7]}){manufacturer_localcalls[i][-7:]}"
            else:
                localcall = manufacturer_localcalls[i]
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
                                "text": f"{manufacturer_name[i]}",
                                "weight": "bold",
                                "size": "xl",
                                "align": "center",
                                "margin": "xl"
                            },
                            {
                                "type": "text",
                                "text": f"廠商編號：{manufacturer_num[i]}",
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
                                            "text": f"{manufacturer_principal[i]}",
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
                                            "text": f"{manufacturer_phone[i]}",
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
                                            "text": f"{manufacturer_payment[i]}",
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
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "button",
                                "action": {
                                "type": "message",
                                "label": "修改廠商資料",
                                "text": f"【廠商修改資料】{manufacturer_num[i]}_{str(pagemin+i+1)}～{str(pagemin+i+9)}"
                                },
                                "style": "primary",
                                "color": "#999a9a"
                            }
                            ]
                        }
                        }
            manufacturer_show.append(showall)
        if len(manufacturer_show) >= 9:
            manufacturer_show.append({
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
                                "text": "【廠商列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                            }
                        }
                    ]
                }
            })
        else:
            manufacturer_show.append({
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
                                "label": "已經到底囉！'點我'回到廠商管理功能",
                                "text": "廠商管理"
                            }
                        }
                    ]
                }
            })
    else:
        manufacturer_show = TextSendMessage(text = '目前尚未有廠商資料！請前往「新增廠商」建立')
    return manufacturer_show

#廠商資料修改畫面(左右)
def Manufacturer_edit():
    id = lineboterp.user_id
    message_storage = lineboterp.storage
    pagemin = lineboterp.list_page[lineboterp.user_id+'廠商列表min']
    pagemax = lineboterp.list_page[lineboterp.user_id+'廠商列表max']
    editinfo = Manufacturer_single(message_storage[id+'manufacturer_list_id'],1)
    name = message_storage[id+'manufacturer_list_name']
    principal = message_storage[id+'manufacturer_list_principal']
    localcalls = message_storage[id+'manufacturer_list_localcalls']
    phone = message_storage[id+'manufacturer_list_phone']
    payment = message_storage[id+'manufacturer_list_payment']
    bankname = message_storage[id+'manufacturer_list_bankname']
    bankid = message_storage[id+'manufacturer_list_bankid']
    bankaccount = message_storage[id+'manufacturer_list_bankaccount']

    if message_storage[id+'manufacturer_list_check'] == 'ok':
        manufacturer_edit_show = []
        editpay = [
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "1.修改_廠商名稱",
                    "text": "【廠商修改】廠商名稱"
                    },
                    "style": "primary",
                    "color": "#BEBFC0",
                    "height": "sm"
                },
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "2.修改_廠商負責人/對接人",
                    "text": "【廠商修改】廠商負責人或對接人"
                    },
                    "style": "primary",
                    "color": "#999a9a",
                    "height": "sm",
                    "margin": "sm"
                },
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "3.修改_廠商市話",
                    "text": "【廠商修改】廠商市話"
                    },
                    "style": "primary",
                    "color": "#BEBFC0",
                    "height": "sm",
                    "margin": "sm"
                },
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "4.修改_廠商行動電話",
                    "text": "【廠商修改】廠商行動電話"
                    },
                    "style": "primary",
                    "color": "#999a9a",
                    "height": "sm",
                    "margin": "sm"
                },
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "5.修改_廠商付款方式",
                    "text": "【廠商修改】廠商付款方式"
                    },
                    "style": "primary",
                    "color": "#BEBFC0",
                    "height": "sm",
                    "margin": "sm"
                }
                ]#修改按鈕付款相關
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
            show5 = {
                "type": "button",
                "action": {
                "type": "message",
                "label": "6.修改_廠商行庫/行庫代號",
                "text": "【廠商修改】廠商行庫/行庫代號"
                },
                "style": "primary",
                "color": "#999a9a",
                "height": "sm",
                "margin": "sm"
            }
            editpay.append(show5)
            show6 = {
                "type": "button",
                "action": {
                "type": "message",
                "label": "7.修改_廠商付款帳號",
                "text": "【廠商修改】廠商付款帳號"
                },
                "style": "primary",
                "color": "#BEBFC0",
                "height": "sm",
                "margin": "sm"
            }
            editpay.append(show6)
        show7 = {
                "type": "separator",
                "color": "#564006",
                "margin": "lg"
            }
        editpay.append(show7)

        if localcalls is None:
            localcall = localcalls
        elif localcalls != '略過':
            localcall = f"({localcalls[:-7]}){localcalls[-7:]}"
        else:
            localcall = localcalls
        
        #左側資訊
        show00 = {
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
                        "text": "修改廠商資料",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": f"廠商編號：{message_storage[id+'manufacturer_list_id']}",
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
                        ],
                        "backgroundColor": "#F4F4F4"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": payinfo,
                        "backgroundColor": "#F4F4F4"
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "button",
                        "action": {
                        "type": "message",
                        "label": "退出修改",
                        "text": f"【廠商列表下一頁】{str(pagemin)}～{str(pagemax)}"
                        },
                        "style": "primary",
                        "color": "#564006"
                    }
                    ]
                }
                }
        manufacturer_edit_show.append(show00)

        #右側修改按鈕
        show01 = {
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
                        "text": "修改廠商資料",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": f"廠商編號：{message_storage[id+'manufacturer_list_id']}",
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
                        "contents": editpay
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "button",
                        "action": {
                        "type": "message",
                        "label": "退出修改",
                        "text": f"【廠商列表下一頁】{str(pagemin)}～{str(pagemax)}"
                        },
                        "style": "primary",
                        "color": "#564006"
                    }
                    ]
                }
                }
        manufacturer_edit_show.append(show01)
        showall = FlexSendMessage(
                    alt_text='【管理廠商】廠商列表',
                    contents={
                        "type": "carousel",
                        "contents": manufacturer_edit_show      
                        } 
                    )
    else:
        showall = TextSendMessage(text='此廠商資料讀取發生錯誤，暫時無法修改！請稍後。')
    return showall