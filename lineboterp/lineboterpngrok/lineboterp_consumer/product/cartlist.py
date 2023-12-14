from linebot.models import TextSendMessage,FlexSendMessage,QuickReplyButton,MessageAction,QuickReply
import info
from database import cartsearch,unitsearch,stock,removecart,revise,cartsubtotal,stockonly,cartcheckprice
from selection_screen import Cart_add_screen

#-------------------購物車資料查詢----------------------
def cart_list():
    user_id = info.user_id
    db_cartshow = cartsearch()
    if db_cartshow=='資料庫搜尋不到':
        cart_show = TextSendMessage(text='您的購物車中尚無商品資料')
    else:
        cart_show = []
        buttons = []  #模塊中5筆資料
        num = 1
        changelist = '\n'
        listnum = 0
        #訂單編號, 商品ID, 商品名稱, 訂購數量, 商品單位, 商品小計
        totalcost = 0
        for totallist in db_cartshow:
            changesub = cartcheckprice(totallist[1],totallist[3],totallist[5])#修正金額
            dbstock,dbrnum,order = stock(totallist[1],totallist[3])
            if dbstock == 'ok':
                if totallist[3] == dbrnum:
                    changenum = str(totallist[3])
                    subtotal = changesub 
                    add = changesub 
                else:
                    changenum = str(dbrnum)
                    listnum += 1
                    changelist += f"{str(listnum)}.修改購物車商品：{str(totallist[2])}，已幫您修改至目前庫存剩餘最大數量{dbrnum}{totallist[4]}！\n"
                    text = revise(user_id,totallist[1],int(dbrnum))
                    subtotal = cartsubtotal(totallist[1])
                    add = subtotal
                text ={
                    "type": "text",
                    "text": f"商品{str(num)}",
                    "weight": "bold",
                    "offsetTop": "none",
                    "size": "xl",
                    "margin": "md"
                    }
                text1 ={
                    "type": "text",
                    "text": f"{str(totallist[2])}x{changenum}{totallist[4]}",
                    "size": "md",
                    "wrap": True
                    }
                text2 ={
                    "type": "text",
                    "text": f"小計NT${str('{:,}'.format(subtotal))}",
                    "weight": "bold",
                    "size": "md",
                    "wrap": True,
                    "margin": "md",
                    "align": "end"
                    }
                button ={
                    "type": "button",
                    "action": {
                        "type": "message",
                        "text": f"【修改數量】{totallist[1]}_{str(totallist[2])}",
                        "label": f"修改商品{str(num)}數量"
                    },
                    "margin": "xs",
                    "height": "sm",
                    "style": "secondary"
                    }
                separator ={
                        "type": "separator",
                        "margin": "xl"
                    }
                for i in [text,text1,text2,button,separator]:
                    buttons.append(i)
                num += 1
            elif dbstock == 'no':
                listnum += 1
                changelist += f"{str(listnum)}.移除購物車清單：{str(totallist[2])}，已無庫存！\n"
                move = removecart(user_id, totallist[1])
                add = 0
            totalcost += add
        buttons.append( {
            "type": "text",
            "text": f"總計NT${str('{:,}'.format(totalcost))}",
            "weight": "bold",
            "size": "md",
            "wrap": True,
            "margin": "md",
            "align": "end"
          })
        
        if len(changelist) >= 2:
            buttons.append( {
            "type": "text",
            "wrap": True,
            "color": "#3b5a5f",
            "size": "sm",
            "flex": 5,
            "weight": "bold",
            "text": f"\n◎購物車自檢結果：{changelist}"
          })
        
        cart_show.append({
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "高逸嚴選",
                "weight": "bold",
                "color": "#A44528",
                "size": "sm"
            },
            {
                "type": "text",
                "text": "我的購物車",
                "weight": "bold",
                "size": "xxl",
                "margin": "md"
            },
            {
                "type": "separator",
                "margin": "xxl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "md",
                "contents": buttons
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "送出購物車訂單",
                "text": "【送出購物車訂單】"
                }
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "修改購物車清單",
                "text": "修改購物車清單"
                }
            }
            ],
            "spacing": "none",
            "paddingAll": "sm"
        },
        "styles": {
            "footer": {
            "separator": True
            }
        }
        })
        if buttons == []:
            cart_show = TextSendMessage(text='您的購物車中尚無商品資料')
        else:
            cart_show = FlexSendMessage(
                    alt_text='我的購物車',
                    contents={
                        "type": "carousel",
                        "contents": cart_show      
                        } 
                    )
    return cart_show

#-------------------購物車商品新增----------------------
def addcart(errormsg):
    user_id = info.user_id
    user_state = info.user_state
    product_id = info.product[user_id+'cartproduct_id']
    product = info.product[user_id+'cartproduct']

    #購物車清單數量確認最大5筆
    db_cartcheck = cartsearch()
    #訂單編號, 商品ID, 商品名稱, 訂購數量, 商品單位, 商品小計
    cartproductid = []#存放購物車中已有的商品ID
    if db_cartcheck!='資料庫搜尋不到':
        for productcartid in db_cartcheck:
            cartproductid.append(productcartid[1])
    if isinstance(db_cartcheck, str) or len(db_cartcheck) < 5:#等於字串或小於5
        #檢查現在想加入的商品有沒有在購物車中
        if product_id in cartproductid:
            cart = TextSendMessage(text='您的購物車清單中已存在此商品囉～')
        else:
            #Quick Reply 按鈕數量範圍
            quantity_option = []
            unit = unitsearch(product_id)
            for i in range(10):
                if unit == '無':
                    quantity_option.append(QuickReplyButton(action=MessageAction(label=str(i+1), text=str(i+1))))
                else:
                    quantity_option.append(QuickReplyButton(action=MessageAction(label=str(i+1)+unit, text=str(i+1))))
            #------------------------
            user_state[user_id] = 'cartnum'#從user_state轉換輸入購物車數量狀態
            # 建立 Quick Reply 按鈕
            quickreply = QuickReply(items=quantity_option)
            cart = Cart_add_screen(product_id,product,quickreply,errormsg)
                # 傳送回應訊息給使用者
    else:
        cart = TextSendMessage(text='您的購物車清單筆數已達5個商品上限！無法再新增商品至購物車！')
    return cart

#-------------------修改購物車單項商品數量----------------------
def cartrevise(errormsg):
    user_id = info.user_id
    user_state = info.user_state
    product_id = info.product[user_id+'cartreviseproduct_id']
    product= info.product[user_id+'cartreviseproduct_name']
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
    user_state[user_id] = 'cartrevise'#從user_state轉換輸入購物車數量狀態
    # 建立 Quick Reply 按鈕
    quickreply = QuickReply(items=quantity_option)

    if errormsg == 'no':
        errormsg = '無'
    else:
        errormsg = str(errormsg)
    msg = {
        "type": "text",
        "text": f"◎錯誤：{errormsg}",
        "wrap": True,
        "color": "#c42149",
        "size": "sm",
        "flex": 5,
        "weight": "bold"
        }
    
    recart = {
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
                    "text": "購物車修改數量(1/1)",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "margin": "xl"
                },
                {
                    "type": "separator",
                    "color": "#77105b",
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
                                "text": "◇商品編號：",
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
                                "text": f"{product_id}",
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
                                "text": "◇商品名稱：",
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
                                "text": f"{product}",
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
                        "type": "text",
                        "text": "<下方依序填寫～>",
                        "wrap": True,
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "margin": "xl",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "=>1.請選擇修改數量：",
                        "wrap": True,
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "margin": "sm",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "※提示：可以自行輸入更多的數量",
                        "wrap": True,
                        "color": "#f6b877",
                        "size": "sm",
                        "flex": 5,
                        "weight": "bold"
                    },
                    msg
                    ]
                }
                ],
                "backgroundColor": "#FCFAF1"
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
            }
            }
    screen =FlexSendMessage(
                            alt_text="購物車修改數量(1/1)",
                            contents={
                                "type": "carousel",
                                "contents": [recart]   
                                },
                            quick_reply = quickreply
                            )
    return screen

#-------------------修改購物車清單----------------------
def editcart():
    db_cartshow = cartsearch()
    if db_cartshow=='資料庫搜尋不到':
        edcart_show = TextSendMessage(text='您的購物車中尚無商品資料')
    else:
        edcart_show = []
        buttons = []  #模塊中5筆資料
        num = 1
        #訂單編號, 商品ID, 商品名稱, 訂購數量, 商品單位, 商品小計
        totalcost = 0 #計算總額
        for totallist in db_cartshow:
            totalcost += totallist[5]
            text ={
                "type": "text",
                "text": f"商品{str(num)}",
                "weight": "bold",
                "offsetTop": "none",
                "size": "xl",
                "margin": "md"
                }
            text1 ={
                "type": "text",
                "text": f"{str(totallist[2])}x{str(totallist[3])}{totallist[4]}",
                "size": "md",
                "wrap": True
                }
            text2 ={
                "type": "text",
                "text": f"小計NT${str('{:,}'.format(totallist[5]))}",
                "weight": "bold",
                "size": "md",
                "wrap": True,
                "margin": "md",
                "align": "end"
                }
            button ={
                "type": "button",
                "action": {
                    "type": "message",
                    "text": f"【清單移除商品】{totallist[1]}_{str(totallist[2])}",
                    "label": f"從清單移除商品{str(num)}"
                },
                "margin": "xs",
                "height": "sm",
                "style": "secondary"
                }
            separator ={
                    "type": "separator",
                    "margin": "xl"
                }
            for i in [text,text1,text2,button,separator]:
                buttons.append(i)
            num += 1
        buttons.append( {
            "type": "text",
            "text": f"總計NT${str('{:,}'.format(totalcost))}",
            "weight": "bold",
            "size": "md",
            "wrap": True,
            "margin": "md",
            "align": "end"
          })
        edcart_show.append({
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "高逸嚴選",
                "weight": "bold",
                "color": "#A44528",
                "size": "sm"
            },
            {
                "type": "text",
                "text": "我的購物車",
                "weight": "bold",
                "size": "xxl",
                "margin": "md"
            },
            {
                "type": "separator",
                "margin": "xxl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "md",
                "contents": buttons
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "取消修改清單",
                "text": "取消修改清單"
                }
            }
            ],
            "spacing": "none",
            "paddingAll": "sm"
        },
        "styles": {
            "footer": {
            "separator": True
            }
        }
        })
        edcart_show = FlexSendMessage(
                alt_text='我的購物車',
                contents={
                    "type": "carousel",
                    "contents": edcart_show      
                    } 
                )
    return edcart_show

def checkcart(content,lumpsum):
    screen_information = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "高逸嚴選",
                    "weight": "bold",
                    "color": "#A44528",
                    "size": "sm"
                },
                {
                    "type": "text",
                    "text": "購物車訂單確認",
                    "weight": "bold",
                    "size": "xl",
                    "margin": "md",
                    "align": "center"
                },
                {
                    "type": "separator",
                    "color": "#77105b",
                    "margin": "xxl"
                },
                {
                    "type": "text",
                    "text": f"{content}",#訂單內容
                    "size": "lg",
                    "margin": "lg",
                    "wrap": True
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "text",
                    "text": f"總額：NT${str('{:,}'.format(lumpsum))}",#總額
                    "size": "lg",
                    "margin": "lg",
                    "align": "end",
                    "weight": "bold"
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "【1.確認】",
                    "text": "1"
                    }
                },
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "【2.取消】",
                    "text": "2"
                    }
                }
                ],
                "spacing": "none",
                "paddingAll": "sm"
            },
            "styles": {
                "footer": {
                "separator": True
                }
            }
            }
    
    checkcart_show = FlexSendMessage(
                alt_text='購物車訂單確認',
                contents={
                    "type": "carousel",
                    "contents": [screen_information]   
                    } 
                )
    return checkcart_show