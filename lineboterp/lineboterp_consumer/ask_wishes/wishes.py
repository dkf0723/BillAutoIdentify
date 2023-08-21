from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from product.buy_now import *
from product.product_preorder import *
import lineboterp
from database import single_imagetolink,wishessend

def wishes():
    id = lineboterp.user_id
    state = lineboterp.user_state
    message = lineboterp.msg
    message_storage = lineboterp.storage
    msgtype = lineboterp.msgtype
    #商品名稱,商品圖片,推薦原因,願望建立時間,會員_LINE_ID,資料來源
    #使用者行為過濾
    userfilter = ['重新填寫','取消','營業資訊','團購商品','【預購商品】列表','【現購商品】列表','訂單/購物車查詢',
                    '訂單查詢','未取訂單列表','預購訂單列表','歷史訂單列表','【訂單詳細】','【加入購物車】',
                    '查看購物車','【修改數量】','修改購物車清單','【清單移除商品】','取消修改清單',
                    '【送出購物車訂單】','問題提問','許願商品','【立即購買】','【手刀預購】',
                    '【現購列表下一頁】','【預購列表下一頁】','資料庫','測試','圖片']
    #行為過濾比對
    for i in userfilter:
        filterresult = 'ok'#預設值
        if msgtype != 'text':#message 訊息屬性除了text
            if state[id] in ['wishes','wishesreason','wishessource','wishescheck']:#以下狀態皆不需要接收到圖片
                filterresult = 'no'
                break
            elif state[id] == 'wishesimg' and msgtype == 'image':
                filterresult = 'ok'
                break
        else:
            if i in message:
                filterresult = 'no'
                break

    if filterresult == 'ok': #if message not in userfilter:
        if state[id] == 'wishes':
            message_storage[id+'wishesname'] = message #商品名稱
            if len(message) <= 15:
                message_storage[id+'wishesall'] = f"1.許願商品名稱：{message}"
                edit_text = f"{message_storage[id+'wishesall']}\n=>2.推薦原因(100字內)：\n<打字輸入>"
                message_storage[id+'wishesstep'] += 1
                check_text = skip_screen(edit_text,message_storage[id+'wishesstep'])#可略
                message_storage[id+'userfilter'] = check_text
                state[id] = 'wishesreason'
            else:
                check_text = [TextSendMessage(text = f"1.許願商品名稱：「{message}」，長度大於15個字請縮短文字呦～"),initial_fill_screen()]
        elif state[id] == 'wishesreason':
            message_storage[id+'wishesreason'] = message #推薦原因
            if len(message) <= 100:
                message_storage[id+'wishesall'] = f"{message_storage[id+'wishesall']}\n2.推薦原因：{message}"
                edit_text = f"{message_storage[id+'wishesall']}\n=>3.想法來源(可以是連結呦～)：\n<打字輸入>"
                message_storage[id+'wishesstep'] += 1
                check_text = fill_out_the_screen(edit_text,message_storage[id+'wishesstep'])#不可略
                message_storage[id+'userfilter'] = check_text
                state[id] = 'wishessource'
            else:
                check_text = [TextSendMessage(text = f"2.推薦原因：「{message}」，長度大於100個字請縮短文字呦～"),message_storage[id+'userfilter']]
        elif state[id] == 'wishessource':
            message_storage[id+'wishessource'] = message #資料來源
            message_storage[id+'wishesall'] = f"{message_storage[id+'wishesall']}\n3.想法來源：{message}"
            edit_text = f"{message_storage[id+'wishesall']}\n=>4.商品圖片：\n<發送 圖/照片>\n\n◎確認內容產生需要一點時間，發送後請稍等3秒！"
            message_storage[id+'wishesstep'] += 1
            check_text = pictureup_screen(edit_text,message_storage[id+'wishesstep'])#相機相簿功能
            message_storage[id+'userfilter'] = check_text
            state[id] = 'wishesimg'
        elif state[id] == 'wishesimg':
            if ('.jpg' in message_storage[id+'img']) or ('(略過)' in message):#檢查暫存的圖片內容路徑
                if '.jpg' in message_storage[id+'img']:
                    single_imagetolink()#執行圖片轉換連結(單張)
                    message_storage[id+'wishesall'] = f"{message_storage[id+'wishesall']}\n4.上傳的圖片連結：{message_storage[id+'imagelink']}"
                else:
                    message_storage[id+'imagelink'] = 'https://i.imgur.com/rGlTAt3.jpg'
                    message_storage[id+'wishesall'] = f"{message_storage[id+'wishesall']}\n4.上傳的圖片連結：(略過)"
                check_info = {
                            "type": "bubble",
                            "hero": {
                                "type": "image",
                                "url": f"{message_storage[id+'imagelink']}",
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
                                    "text": "許願商品填寫確認",
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
                                        "type": "text",
                                        "text": f"{message_storage[id+'wishesall']}",
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
                                    "label": "許願送出",
                                    "text": "許願送出"
                                    },
                                    "style": "primary",
                                    "color": "#A44528"
                                },
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "height": "sm",
                                    "action": {
                                    "type": "message",
                                    "label": "重新填寫",
                                    "text": "重新填寫"
                                    },
                                    "color": "#5F403B"
                                },
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
                            },
                            "styles": {
                                "body": {
                                "backgroundColor": "#FCFAF1"
                                },
                                "footer": {
                                "backgroundColor": "#FCFAF1"
                                }
                            }
                            }
                check_text =FlexSendMessage(
                            alt_text='願望商品填寫確認',
                            contents={
                                "type": "carousel",
                                "contents": [check_info]   
                                } 
                            )
                message_storage[id+'wishescheck_info'] = check_text
                message_storage[id+'userfilter'] = check_text
                state[id] = 'wishescheck'
            else:
                check_text = [TextSendMessage(text='4.您傳送的不是圖片，請打開聊天室圖片庫發送圖片！'),message_storage[id+'userfilter']]
        elif state[id] == 'wishescheck':
            if message == '許願送出':
                wishesname = message_storage[id+'wishesname']
                wishesreason = message_storage[id+'wishesreason']
                wishessource = message_storage[id+'wishessource']
                imagelink = message_storage[id+'imagelink']
                confirmationmessage = wishessend(wishesname,wishesreason,wishessource,imagelink)
                if confirmationmessage == 'ok':
                    check_text = TextSendMessage(text='許願商品已經成功建立囉～')
                else:
                    check_text = TextSendMessage(text='許願商品建立時發生錯誤！請稍後再試～')
                wishesname = 'NaN'
                wishesreason = 'NaN'
                wishessource = 'NaN'
                message_storage[id+'img'] = 'NaN'
                imagelink = 'NaN'
                message_storage[id+'userfilter'] = 'NaN'
                message_storage[id+'wishescheck_info'] = 'NaN'
                state[id] = 'normal'
            else:
                check_text = [TextSendMessage(text= f"「{message}」不在許願商品填寫確認中的指令喔！請點擊訊息框下方的按鈕。"),message_storage[id+'wishescheck_info']]
    else:
        if message in ['重新填寫','取消']:
            message_storage[id+'userfilter'] = "NaN"
            #取消或重新填寫都將所有有關願望商品的暫存取消
            message_storage[id+'wishesname'] = 'NaN'
            message_storage[id+'wishesreason'] = 'NaN'
            message_storage[id+'wishessource'] = 'NaN'
            message_storage[id+'img'] = 'NaN'
            message_storage[id+'imagelink'] = 'NaN'
            message_storage[id+'wishescheck_info'] = 'NaN'
            if message == '重新填寫':
                state[id] = 'wishes'
                message_storage[id+'wishesstep'] = 1
                check_text = initial_fill_screen()
            elif message == '取消':
                state[id] = 'normal'
                check_text = TextSendMessage(text = '您的許願商品填寫流程\n已經取消囉～')
        else:
            cancelmessage = f"您傳送的訊息「{message}」不在許願商品填寫流程中，如果想取消請點擊下方取消按鈕～"
            if str(message_storage[id+'userfilter']) == 'NaN':
                check_text = [TextSendMessage(text = cancelmessage),initial_fill_screen()]
            else:
                check_text = [TextSendMessage(text = cancelmessage),message_storage[id+'userfilter']]
    return check_text

#填寫畫面1
def initial_fill_screen():
    screen_information = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/rGlTAt3.jpg",
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
                        "text": "許願商品填寫(1/4)",
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
                            "type": "text",
                            "text": "提示：\n※前3步驟，請打字輸入！\n※步驟4，請發送照/圖片！",
                            "wrap": True,
                            "color": "#f6b877",
                            "size": "sm",
                            "flex": 5
                        },
                        {
                            "type": "text",
                            "text": "<下方依序填寫～>",
                            "wrap": True,
                            "color": "#3b5a5f",
                            "size": "lg",
                            "flex": 5,
                            "margin": "lg",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": "=>1.許願商品名稱(15字內)：\n<請打字輸入>",
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
                },
                "styles": {
                    "body": {
                    "backgroundColor": "#FCFAF1"
                    },
                    "footer": {
                    "backgroundColor": "#FCFAF1"
                    }
                }
                }

    initial_fill_screen_show = FlexSendMessage(
                alt_text="許願商品填寫(1/4)",
                contents={
                    "type": "carousel",
                    "contents": [screen_information]   
                    } 
                )
    return initial_fill_screen_show

#可略過，填寫畫面2
def skip_screen(allcontent,wishesstep):
    skip_information = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/rGlTAt3.jpg",
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
                        "text": f"許願商品填寫({wishesstep}/4)",
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
                            "type": "text",
                            "text": "提示：\n※前3步驟，請打字輸入！\n※步驟4，請發送照/圖片！",
                            "wrap": True,
                            "color": "#f6b877",
                            "size": "sm",
                            "flex": 5
                        },
                        {
                            "type": "text",
                            "text": "<下方依序填寫～>",
                            "wrap": True,
                            "color": "#3b5a5f",
                            "size": "lg",
                            "flex": 5,
                            "margin": "lg",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": f"{allcontent}",
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
                        "label": "略過",
                        "text": "(略過)"
                        },
                        "color": "#A44528",
                        "style": "primary"
                    },
                    {
                        "type": "button",
                        "height": "sm",
                        "action": {
                        "type": "message",
                        "label": "重新填寫",
                        "text": "重新填寫"
                        },
                        "color": "#5F403B",
                        "style": "primary"
                    },
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
                },
                "styles": {
                    "body": {
                    "backgroundColor": "#FCFAF1"
                    },
                    "footer": {
                    "backgroundColor": "#FCFAF1"
                    }
                }
                }

    skipscreen_show = FlexSendMessage(
                alt_text=f"許願商品填寫({wishesstep}/4)",
                contents={
                    "type": "carousel",
                    "contents": [skip_information]   
                    } 
                )
    return skipscreen_show

#填寫畫面3
def fill_out_the_screen(allcontent,wishesstep):
    screen_information = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/rGlTAt3.jpg",
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
                        "text": f"許願商品填寫({wishesstep}/4)",
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
                            "type": "text",
                            "text": "提示：\n※前3步驟，請打字輸入！\n※步驟4，請發送照/圖片！",
                            "wrap": True,
                            "color": "#f6b877",
                            "size": "sm",
                            "flex": 5
                        },
                        {
                            "type": "text",
                            "text": "<下方依序填寫～>",
                            "wrap": True,
                            "color": "#3b5a5f",
                            "size": "lg",
                            "flex": 5,
                            "margin": "lg",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": f"{allcontent}",
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
                        "label": "重新填寫",
                        "text": "重新填寫"
                        },
                        "color": "#A44528",
                        "style": "primary"
                    },
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
                },
                "styles": {
                    "body": {
                    "backgroundColor": "#FCFAF1"
                    },
                    "footer": {
                    "backgroundColor": "#FCFAF1"
                    }
                }
                }

    fill_out_the_screen_show = FlexSendMessage(
                alt_text= f"許願商品填寫({wishesstep}/4)",
                contents={
                    "type": "carousel",
                    "contents": [screen_information]   
                    } 
                )
    return fill_out_the_screen_show

#相簿相機，填寫畫面4
def pictureup_screen(allcontent,wishesstep):
    pictureup_information = {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://i.imgur.com/rGlTAt3.jpg",
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
                            "text": f"許願商品填寫({wishesstep}/4)",
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
                                "type": "text",
                                "text": "提示：\n※前3步驟，請打字輸入！\n※步驟4，請發送照/圖片！",
                                "wrap": True,
                                "color": "#f6b877",
                                "size": "sm",
                                "flex": 5
                            },
                            {
                                "type": "text",
                                "text": "<下方依序填寫～>",
                                "wrap": True,
                                "size": "lg",
                                "flex": 5,
                                "weight": "bold",
                                "color": "#3b5a5f",
                                "margin": "lg"
                            },
                            {
                                "type": "text",
                                "text": f"{allcontent}",
                                "wrap": True,
                                "size": "md",
                                "flex": 5,
                                "weight": "bold",
                                "color": "#3b5a5f",
                                "margin": "sm"
                            }
                            ]
                        }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "button",
                            "action": {
                            "type": "uri",
                            "label": "開啟相簿發送",
                            "uri": "https://line.me/R/nv/cameraRoll/single"
                            },
                            "color": "#A44528",
                            "style": "primary",
                            "height": "sm"
                        },
                        {
                            "type": "button",
                            "height": "sm",
                            "action": {
                            "type": "uri",
                            "label": "開啟相機發送",
                            "uri": "https://line.me/R/nv/camera/"
                            },
                            "color": "#5F403B",
                            "style": "primary"
                        },
                        {
                            "type": "button",
                            "height": "sm",
                            "action": {
                            "type": "message",
                            "label": "略過",
                            "text": "(略過)"
                            },
                            "color": "#9C8C6C",
                            "style": "primary"
                        },
                        {
                            "type": "button",
                            "height": "sm",
                            "action": {
                            "type": "message",
                            "label": "重新填寫",
                            "text": "重新填寫"
                            },
                            "color": "#C9B0A8",
                            "style": "primary"
                        },
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
                    },
                    "styles": {
                        "body": {
                        "backgroundColor": "#FCFAF1"
                        },
                        "footer": {
                        "backgroundColor": "#FCFAF1"
                        }
                    }
                    }

    pictureup_show = FlexSendMessage(
                alt_text='許願商品確認',
                contents={
                    "type": "carousel",
                    "contents": [pictureup_information]   
                    } 
                )
    return pictureup_show