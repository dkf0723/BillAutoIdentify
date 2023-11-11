from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from database import gettime
import manager

#新增進貨資訊填寫及確認畫面
#----測試1111輸入進貨資訊--------
def Purchase_fillin_and_check_screen(errormsg):
    id = manager.user_id
    message_storage = manager.storage
    edit_step = message_storage[id+'Purchase_edit_step']#編寫到第幾步驟
    if edit_step in [2,3]:
        message_storage[id+'give_money'] = message_storage[id+'purchase_num'] * message_storage[id+'purchase_cost']#金額
        message_storage[id+'purchase_time'] = gettime()['formatted_datetime']#進貨時間
    if edit_step < 3:
        title = f"進貨資料填寫({str(edit_step+1)}/3)"
    else:
        title = "進貨資料確認"
    purchase_fillin_and_check_screen = []
    hint = ['2.請打字輸入進貨單價：\n(必須大於0的整數)',
            '3.請輸入匯款時間']#編寫提示訊息
    Completed = ['進貨數量','進貨單價','匯款時間','匯款金額','進貨時間']#填寫後的欄位顯示最後確認後2
    field_value = ['purchase_num','purchase_cost','money_time','give_money',
                   'purchase_time']
    fillin = []#填寫訊息合併暫存
    if edit_step == 0:
        fill = {
                "type": "text",
                "text": "=>1.請打字輸入進貨數量：\n(必須大於0的整數)",
                "wrap": True,
                "color": "#3b5a5f",
                "weight": "bold"
            }
        fillin.append(fill)
    else:
        if edit_step < 3:
            step = edit_step
        else:
            step = 5
        for step in range(step): #1~2
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
                        "width": "100px"
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
        if edit_step < 2:    
            fill_3 = {
                    "type": "text",
                    "text": f"=>{hint[edit_step-1]}",
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
    labelshow = '重新填寫'
    txtshow = '重新填寫'
    msgshow = '取消'

    if edit_step == 3:
        txtshow = '1'
        msgshow = '2'
        labelshow = '送出'

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
                    "color": "#9E93D9"
                }
        buttonshow.append(button1)
    
    button2 = {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "取消",
                    "text": f"{msgshow}"
                    },
                    "height": "sm",
                    "style": "primary",
                    "margin": "md",
                    "color": "#C1BAE7"
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

    purchase_fillin_and_check_screen.append(fillin_screen)
    screen =FlexSendMessage(
                            alt_text='進貨資訊填寫或確認',
                            contents={
                                "type": "carousel",
                                "contents": purchase_fillin_and_check_screen   
                                } 
                            )
    return screen

#新增廠商建立成功畫面
def Purchase_establishment_screen(purchase_pid,purchase_num,purchase_cost,purchase_unit,purchase_time,give_money,money_time):
    manufacturer_establishment_screen = []
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
                    "text": "進貨成功建立！",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "margin": "xl"
                },
                {
                    "type": "text",
                    "text": f"商品編號：{purchase_pid}",
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
                                "text": "◇進貨數量：",
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
                                "text": f"{purchase_num}",
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
                                "text": "◇進貨單價：",
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
                                "text": f"{purchase_cost}",
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
                                "text": "◇商品單位：",
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
                                "text": f"{purchase_unit}",
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
                                "text": "◇進貨金額：",
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
                                "text": f"{give_money}",
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
                                "text": "◇匯款時間：",
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
                                "text": f"{money_time}",
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
                                "text": "◇進貨時間：",
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
                                "text": f"{purchase_time}",
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
            }
            }
    manufacturer_establishment_screen.append(showall)
    screen =FlexSendMessage(
                            alt_text='進貨建立成功！',
                            contents={
                                "type": "carousel",
                                "contents": manufacturer_establishment_screen   
                                } 
                            )
    return screen
