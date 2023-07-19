from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import lineboterp
from database import preorder_list
#-------------------預購清單----------------------
def product_preorder_list():
    db_preorder_list = preorder_list()
    if db_preorder_list == "找不到符合條件的資料。":
        product_show = TextSendMessage(text=db_preorder_list)
    else:
        pagemin = lineboterp.list_page[lineboterp.user_id+'預購min']
        pagemax = lineboterp.list_page[lineboterp.user_id+'預購max']#9
        db_preorder = db_preorder_list[pagemin:pagemax] #最多九個+1more
        product_show =[]#輸出全部
        product_id = []#商品ID
        product_name = []#商品名稱
        product_img = []#商品圖片
        product_description = []#商品簡介
        product_unit = []#商品單位
        product_price = []#售出單價
        product_price2 = []#售出單價2
        product_multiple = []#預購數量限制_倍數
        product_deadline = []#預購截止時間
        for db_preorder_list in db_preorder:
            if db_preorder_list[0] is None:
                break
            else:
                id = db_preorder_list[0]#商品ID
                product_id.append(id)
                name = db_preorder_list[1]#商品名稱
                #現預購商品
                product_name.append(name)
                img = db_preorder_list[3]#商品圖片
                product_img.append(img)
                description = db_preorder_list[4]#商品簡介
                product_description.append(description)
                unit = db_preorder_list[5]#商品單位
                product_unit.append(unit)
                price = db_preorder_list[6]#售出單價
                product_price.append(price)
                price2 = db_preorder_list[7]#售出單價2
                product_price2.append(price2)
                multiple = db_preorder_list[8]#預購數量限制_倍數
                product_multiple.append(multiple)
                deadline = db_preorder_list[9]#預購截止時間
                product_deadline.append(deadline)


        for i in range(len(product_id)):
            if product_price2[i] is None:
                price2 = '--'
            else:
                price2 = "2"+ product_unit[i] + "起每包$" + str(product_price2[i])
            product_show.append({
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": product_img[i],
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                    "type": "message",
                    "label": "action",
                    "text": "【商品簡介】"+('\n%s\n%s\n'%(product_name[i],product_description[i]))
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": product_name[i],
                        "weight": "bold",
                        "size": "lg",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "icon",
                                "size": "sm",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                            },
                            {
                                "type": "icon",
                                "size": "sm",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                            },
                            {
                                "type": "icon",
                                "size": "sm",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                            },
                            {
                                "type": "icon",
                                "size": "sm",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                            },
                            {
                                "type": "icon",
                                "size": "sm",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                            },
                            {
                                "type": "text",
                                "text": "4.0",
                                "size": "sm",
                                "color": "#999999",
                                "margin": "md",
                                "flex": 0
                            }
                        ]
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
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": "預購成立後將於預購截止日發送是否成功訊息",
                                        "wrap": True,
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 15
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "1"+ product_unit[i] + "$" + str(product_price[i]),
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": price2,
                                        "wrap": True,
                                        "color": "#FF1212",
                                        "size": "sm",
                                        "flex": 5
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
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "手刀預購",
                            "text": "【手刀預購】"+product_name[i]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "加入購物車",
                            "text": "【加入購物車】"+product_name[i]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "查看購物車",
                            "text": "查看購物車"
                        }
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "margin": "sm"
                    }
                ],
                "flex": 0,
                "cornerRadius": "sm"
            }
        })

        if len(product_show) >= 9:
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
                                "label": "''點我''下一頁",
                                "text": "【預購列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                            }
                        }
                    ]
                }
            })
        else:
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
                                "label": "已經到底囉！'點我'瀏覽其他商品",
                                "text": "團購商品"
                            }
                        }
                    ]
                }
            })
    return product_show
#-------------------預購訂單----------------------
def Order_preorder():
    user_id = lineboterp.user_id
    user_state = lineboterp.user_state
    product = lineboterp.product[user_id+'product']
    product_order_preorder = lineboterp.product_order_preorder
    product_order_preorder[user_id] = '預購'
    #Quick Reply 按鈕數量範圍
    quantity_option = []
    for i in range(10):
        quantity_option.append(QuickReplyButton(action=MessageAction(label=str(i+1), text=str(i+1))))
    #------------------------
    
    user_state[user_id] = 'preorder'#從user_state轉換預購狀態
    # 建立 Quick Reply 按鈕
    quick_reply_message = TextSendMessage(
        text='商品名稱：%s\n=>請輸入預購數量：' %(product),
        quick_reply=QuickReply(items=quantity_option)
    )    
    Order_preorder_text = TextSendMessage(text='訂/預購流程中，如想取消請打字輸入" 取消 "'),quick_reply_message
        # 傳送回應訊息給使用者
    return Order_preorder_text