from linebot.models import TextSendMessage,FlexSendMessage,QuickReplyButton,MessageAction,QuickReply
import lineboterp
from database import buynow_list,unitsearch,stockonly
from selection_screen import Order_buynow_preorder_screen

#-------------------現購清單----------------------
def product_buynow_list():
    product_show = ''
    db_buynow_list = buynow_list()
    if db_buynow_list == "找不到符合條件的資料。":
        product_show = TextSendMessage(text=db_buynow_list)
    else:
        pagemin = lineboterp.list_page[lineboterp.user_id+'現購min']
        pagemax = lineboterp.list_page[lineboterp.user_id+'現購max']#9
        db_buynow = db_buynow_list[pagemin:pagemax] #最多九個+1more
        show =[]#輸出全部
        product_id = []#商品ID
        product_name = []#商品名稱
        product_img = []#商品圖片
        product_description = []#商品簡介
        product_unit = []#商品單位
        product_price = []#售出單價
        product_price2 = []#售出單價2
        product_stock_quantity = []#庫存數量
        for db_preorder_list in db_buynow:
            if db_preorder_list[0] is None:
                break
            else:
                id = db_preorder_list[0]#商品ID
                product_id.append(id)
                name = db_preorder_list[1]#商品名稱
                #現預購商品
                product_name.append(name)
                if (db_preorder_list[3] is None) or (db_preorder_list[3][:4] != 'http'):
                    img = 'https://i.imgur.com/rGlTAt3.jpg'
                else:
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
                stock_quantity = db_preorder_list[8]#庫存入量
                product_stock_quantity.append(stock_quantity)


        for i in range(len(product_id)):
            if product_price2[i] is None:
                price2 = '暫無其他優惠'
            else:
                price2 = f"2{product_unit[i]}起每{product_unit[i]}{str(product_price2[i])}元"
            show.append({
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
                                "text": "【現購列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
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
                                "label": "已經到底囉！'點我'瀏覽其他商品",
                                "text": "團購商品",
                            }
                        }
                    ]
                }
            })
        product_show = FlexSendMessage(
                    alt_text='【現購商品】列表',
                    contents={
                        "type": "carousel",
                        "contents": show      
                        } 
                    )
    return product_show
#-------------------現購訂單----------------------
def Order_buynow(errormsg):
    user_id = lineboterp.user_id
    user_state = lineboterp.user_state
    product_id = lineboterp.product[user_id+'product_id']
    product = lineboterp.product[user_id+'product']
    product_order_preorder = lineboterp.product_order_preorder
    product_order_preorder[user_id] = '現購'
    #Quick Reply 按鈕數量範圍
    quantity_option = []
    unit = unitsearch(product_id)
    stocknum = stockonly(product_id)
    if stocknum >= 13:
        stocknum = 13
    for i in range(stocknum):
        if unit == '無':
            quantity_option.append(QuickReplyButton(action=MessageAction(label=str(i+1), text=str(i+1))))
        else:
            quantity_option.append(QuickReplyButton(action=MessageAction(label=str(i+1)+unit, text=str(i+1))))
    #------------------------
    user_state[user_id] = 'ordering'#從user_state轉換訂購狀態
    # 建立畫面及Quick Reply 按鈕
    quickreply = QuickReply(items=quantity_option)
    Order_buynow_text = Order_buynow_preorder_screen(product_order_preorder[user_id],product_id,product,quickreply,errormsg)
    return Order_buynow_text

