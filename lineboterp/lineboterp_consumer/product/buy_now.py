from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import lineboterp
from database import buynow_list

#-------------------現購清單----------------------
def product_buynow_list():
    db_buynow_list = buynow_list()
    if db_buynow_list == "找不到符合條件的資料。":
        product_show = TextSendMessage(text=db_buynow_list)
    else:
        pagemin = lineboterp.list_page[lineboterp.user_id+'現購min']
        pagemax = lineboterp.list_page[lineboterp.user_id+'現購max']#9
        db_preorder = db_buynow_list[pagemin:pagemax] #最多九個+1more
        product_show =[]#輸出全部
        product_id = []#商品ID
        product_name = []#商品名稱
        product_img = []#商品圖片
        product_description = []#商品簡介
        product_unit = []#商品單位
        product_price = []#售出單價
        product_price2 = []#售出單價2
        product_stock_quantity = []#庫存數量
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
                stock_quantity = db_preorder_list[8]#預購數量限制_倍數
                product_stock_quantity.append(stock_quantity)


        for i in range(len(product_id)):
            if product_price2[i] is None:
                price2 = '暫無其他優惠'
            else:
                price2 = f"2{product_unit[i]}起每{product_unit[i]}{str(product_price2[i])}元"
            product_show.append({
                "type": "bubble",
                "size": "mega",
                "direction": "ltr",
                "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                    "type": "message",
                    "label": "action",
                    "text": "【商品簡介】"+('\n%s\n%s\n'%(product_name[i],product_description[i]))
                },
                "url": product_img[i]
                },
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": product_name[i],
                    "weight": "bold",
                    "size": "lg"
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
                            "text": f"【商品剩餘數量 {str(product_stock_quantity[i])}】",
                            "wrap": True,
                            "color": "#FF0000",
                            "size": "sm",
                            "flex": 15
                            }
                        ]
                        },
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
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "text": "完成訂購流程即可前往店面取貨呦～",
                            "flex": 15
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                            "type": "text",
                            "text": f"1{product_unit[i]}{str(product_price[i])}元",
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 15
                            }
                        ],
                        "flex": 20
                        },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                            "type": "text",
                            "text": price2,
                            "wrap": True,
                            "size": "md",
                            "flex": 15,
                            "color": "#FF0000"
                            }
                        ],
                        "flex": 20
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
                        "label": "立即購買",
                        "text": "【立即購買】"+product_id[i]+"_"+product_name[i]
                    }
                    },
                    {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "加入購物車",
                        "text": "【加入購物車】"+product_id[i]+"_"+product_name[i]
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
                                "text": "【現購列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
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
                                "text": "團購商品",
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
    product_id = lineboterp.product[user_id+'product_id']
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
        text='商品ID：%s\n商品名稱：%s\n=>請輸入訂購數量：' %(product_id,product),
        quick_reply=QuickReply(items=quantity_option)
    )
    Order_buynow_text = TextSendMessage(text='訂/預購流程中，如想取消請打字輸入" 取消 "'),quick_reply_message
        # 傳送回應訊息給使用者
    return Order_buynow_text