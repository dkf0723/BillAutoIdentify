from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import lineboterp
#-------------------現購清單----------------------
def product_buynow_list():
    product_name = ["椅子", "商品1", "商品2"]  # 最多九個(要加more一個)
    price = ["50", "60", "70"]
    unit = ["個", "件", "箱"]
    statement_time = ["總數量：60", "總數量：20", "總數量：5"]
    product_description = ["非常棒好用的產品快來買喔！", "非常棒好用的產品快來買喔！非常棒好用的產品快來買喔！", "非常棒好用的產品快來買喔！非常棒好用的產品快來買喔！非常棒好用的產品快來買喔！"]
    product_show = []

    for i in range(len(product_name)):
        name = product_name[i]
        price_value = price[i]
        unit_value = unit[i]
        statement = statement_time[i]
        description = product_description[i]

        product_show.append({
            "type": "bubble",
            "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_5_carousel.png"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "text",
                        "text": name,
                        "weight": "bold",
                        "size": "xxl",
                        "align": "center",
                        "flex": 1,
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": "NT." + price_value + " / 每" + unit_value + " ",
                        "align": "start",
                        "size": "lg",
                        "style": "italic"
                    },
                    {
                        "type": "text",
                        "text": statement,
                        "size": "xxs",
                        "align": "start"
                    },
                    {
                        "type": "text",
                        "text": description,
                        "align": "start",
                        "wrap": True
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
                        "style": "primary",
                        "action": {
                            "type": "message",
                            "label": "立即購買",
                            "text": "【立即購買】" + name
                        }
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "加入購物車",
                            "text": "【加入購物車】" + name
                        },
                        "style": "secondary"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "查看購物車",
                            "text": "查看購物車"
                        }
                    }
                ]
            }
        })

    product_show.append({
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
                        "label": "更多內容",
                        "text": "更多內容"
                    }
                }
            ]
        }
    })
    return product_show
#-------------------現購訂單----------------------
def Order_buynow():
    user_id = lineboterp.user_id
    user_state = lineboterp.user_state
    product = lineboterp.product[user_id+'product']
    product_order_preorder = lineboterp.product_order_preorder
    product_order_preorder[user_id] = '訂購'
    #Quick Reply 按鈕數量範圍
    quantity_option = []
    for i in range(10):
        quantity_option.append(QuickReplyButton(action=MessageAction(label=str(i+1), text=str(i+1))))
    #------------------------

    user_state[user_id] = 'ordering'#從user_state轉換訂購狀態
    # 建立 Quick Reply 按鈕
    quick_reply_message = TextSendMessage(
        text='商品名稱：%s\n=>請輸入訂購數量：' %(product),
        quick_reply=QuickReply(items=quantity_option)
    )
    Order_buynow_text = TextSendMessage(text='訂/預購流程中，如想取消請打字輸入" 取消 "'),quick_reply_message
        # 傳送回應訊息給使用者
    return Order_buynow_text