from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from database  import order_list, orderdt
import manager
#---------------預購/未取------------
def manager_order_list(queryObject):
    db_nottaken = order_list(queryObject)
    if db_nottaken=="找不到符合條件的資料。":
      ordernottaken_show = TextSendMessage(text=db_nottaken)
    else:
      ordernottaken_show = []
      ordernottaken_handlelist = []
      
      while len(db_nottaken) > 0:
        two_elements = db_nottaken[:10]  # 取得10個元素
        ordernottaken_handlelist.append(two_elements)  # 將10個元素作為一個子陣列加入結果陣列
        db_nottaken = db_nottaken[10:]

      for totallist in ordernottaken_handlelist:
          buttons = []  # #模塊中10筆資料
          for i in range(len(totallist)):
              lumpsum = totallist[i][4]
              if lumpsum is not None:
                  lumpsum_formatted = '{:,}'.format(lumpsum)
              dtime = totallist[i][3].strftime('%Y-%m-%d %H:%M')
              button = {
                  "type": "button",
                  "action": {
                      "type": "message",
                      "label": f"[{dtime}] NT${lumpsum_formatted}",
                      "text": f"【訂單詳細】{dtime}\n{totallist[i][0]}"
                  }
                }
              buttons.append(button)
          ordernottaken_show.append({
                  "type": "bubble",
                  "body": {
                  "type": "box",
                  "layout": "vertical",
                        "contents": [
                            {
                            "type": "text",
                            "text": "高逸嚴選",
                            "weight": "bold",
                            "color": "#1DB446",
                            "size": "sm"
                            },
                            {
                            "type": "text",
                            "text": "未取訂單查詢",
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
                        "styles": {
                        "footer": {
                            "separator": True
                        }
                        }
                    })
      ordernottaken_show = FlexSendMessage(
            alt_text="未取訂單查詢",
            contents={
              "type": "carousel",
              "contents": ordernottaken_show      
            } 
        )
    return ordernottaken_show

#-------------------訂單詳細資料----------------------
def orderdtsearch():
    db_orderdt = orderdt()
    if db_orderdt=='找不到符合條件的資料。':
        show = TextSendMessage(text=db_orderdt)
    else:
        '''訂單編號,電話,訂單狀態未取已取,商品ID,商品名稱,商品單位,訂購數量,商品小計,總額,訂單成立時間,取貨完成時間'''
        if db_orderdt[0][10] is None:
            pickup = '<無>'
        else:
            pickup = str(db_orderdt[0][10])
        show = f"""===訂單詳細資料===
*訂單編號：\n   {str(db_orderdt[0][0])}
*訂單成立時間：\n   {str(db_orderdt[0][9])}
*取貨完成或訂單取消時間：\n   {pickup}
*狀態：{db_orderdt[0][2]}
*電話號碼：{str(db_orderdt[0][1])}

"""
        showlater = f"""訂單總額：NT${str('{:,}'.format(db_orderdt[0][8]))}"""     
        num = 1
        while len(db_orderdt) > 0:
            dt = f"""=>商品{num}
品名：{db_orderdt[0][4]}
數量：{db_orderdt[0][6]}{db_orderdt[0][5]}
小計：{str('{:,}'.format(db_orderdt[0][7]))}
----------------------------
"""
            show += dt
            num += 1
            db_orderdt = db_orderdt[1:]  # 移除已取得的元素
        show += showlater
        show = TextSendMessage(text=show)
    return show
#---------------預購/未取------------
# def manager_order_list(queryObject):
#     show = []
#     db_preorder_list = order_list(queryObject)

#     if db_preorder_list == '找不到符合條件的資料。':
#         show = TextSendMessage(text=db_preorder_list)
#     else:
#         pagemin = 0
#         pagemax = 8
#         db_preorder = db_preorder_list[pagemin:pagemax]
#         show = []
#         OrderId = [] #預購的訂單編號
#         LineId = [] #預購訂單的LindId
#         PhoneNumber = [] #預購訂單的電話
#         OrderTime = [] #預購訂單的下訂時間
#         Amount = [] #預購訂單的總額
#         order_deatils_ProductId = [] #商品ID
#         order_deatils_amount = [] #商品個別數量
#         order_deatils_total = [] #商品個別小計

#         #預購訂單賦值
#         for db_preorder_list in db_preorder:
#                 OrderId.append(db_preorder_list[0])
#                 LineId.append(db_preorder_list[1])
#                 PhoneNumber.append(db_preorder_list[2])
#                 OrderTime.append(db_preorder_list[3])
#                 Amount.append(db_preorder_list[4])
#                 order_deatils_ProductId.append(db_preorder_list[5])
#                 order_deatils_amount.append(db_preorder_list[6])
#                 order_deatils_total.append(db_preorder_list[7])
    
#         #列表
#         for i in range(len(OrderId)):
#             show.append({
#                     "type": "bubble",
#                     "body": {
#                       "type": "box",
#                       "layout": "vertical",
#                       "spacing": "none",
#                       "contents": [
#                         {
#                           "type": "text",
#                           "text": "高逸嚴選",
#                           "wrap": True,
#                           "weight": "bold",
#                           "size": "sm",
#                           "color": "#1DB446",
#                           "align": "start"
#                         },
#                         {
#                           "type": "text",
#                           "text": f"{queryObject}資訊",
#                           "margin": "xs",
#                           "size": "xxl",
#                           "weight": "bold"
#                         },
#                         {
#                           "type": "box",
#                           "layout": "vertical",
#                           "contents": [
#                             {
#                               "type": "box",
#                               "layout": "horizontal",
#                               "contents": [
#                                 {
#                                   "type": "text",
#                                   "text":OrderId[i],
#                                   "size": "lg",
#                                   "margin": "none",
#                                   "flex": 0
#                                 },
#                                 {
#                                   "type": "text",
#                                   "text": LineId[i],
#                                   "margin": "none",
#                                   "size": "xl",
#                                   "offsetStart": "none",
#                                   "offsetEnd": "none",
#                                   "offsetBottom": "none",
#                                   "offsetTop": "none",
#                                   "style": "italic"
#                                 }
#                               ]
#                             },
#                             {
#                               "type": "box",
#                               "layout": "horizontal",
#                               "contents": [
#                                 {
#                                   "type": "text",
#                                   "text": OrderTime[i],
#                                   "size": "lg",
#                                   "margin": "none",
#                                   "flex": 0
#                                 },
#                                 {
#                                   "type": "text",
#                                   "text": "112/08/02",
#                                   "size": "xl",
#                                   "margin": "xs",
#                                   "style": "italic"
#                                 }
#                               ]
#                             },
#                             {
#                               "type": "box",
#                               "layout": "horizontal",
#                               "contents": [
#                                 {
#                                   "type": "text",
#                                   "text": PhoneNumber[i],
#                                   "size": "lg",
#                                   "flex": 0
#                                 },
#                                 {
#                                   "type": "text",
#                                   "text": "0978215471",
#                                   "size": "xl",
#                                   "margin": "xs",
#                                   "style": "italic"
#                                 }
#                               ]
#                             },
#                             {
#                               "type": "box",
#                               "layout": "horizontal",
#                               "contents": [
#                                 {
#                                   "type": "text",
#                                   "text": Amount[i],
#                                   "size": "lg",
#                                   "margin": "none",
#                                   "flex": 0
#                                 },
#                                 {
#                                   "type": "text",
#                                   "text": "$1250",
#                                   "size": "xl",
#                                   "margin": "xs",
#                                   "style": "italic"
#                                 }
#                               ]
#                             },
#                             {
#                               "type": "separator",
#                               "margin": "xxl"
#                             }
#                           ],
#                           "margin": "lg"
#                         },
#                         #訂單內容
#                         {
#                           "type": "box",
#                           "layout": "vertical",
#                           "contents": [
#                             {
#                               "type": "box",
#                               "layout": "horizontal",
#                               "contents": [
#                                 {
#                                   "type": "text",
#                                   "text": "訂單內容",
#                                   "margin": "xs",
#                                   "size": "xxl",
#                                   "weight": "bold",
#                                   "color": "#004D99"
#                                 }
#                               ],
#                               "margin": "lg"
#                             },
#                             #商品數for迴圈上標
#                             {
#                               "type": "box",
#                               "layout": "vertical",
#                               "contents": [
#                                 {
#                                   "type": "text",
#                                   "text": "商品ID :"+order_deatils_ProductId+"/商品數量:"+order_deatils_amount+"/小計:"+order_deatils_total,
#                                   "wrap": True,
#                                   "margin": "md",
#                                   "size": "md",
#                                   "color": "#004D99"
#                                 },
#                               ],
#                               "margin": "none"
#                             }
#                             #商品數for迴圈下標
#                           ]
#                         }
#                       ],
#                       "margin": "xl"
#                     }
#               })
#             if len(show) >= 9:
#               show.append({
#                 "type": "bubble",
#                 "body": {
#                     "type": "box",
#                     "layout": "vertical",
#                     "spacing": "sm",
#                     "contents": [
#                         {
#                             "type": "button",
#                             "flex": 1,
#                             "gravity": "center",
#                             "action": {
#                                 "type": "message",
#                                 "label": "''點我''下一頁",
#                                 "text": "【未取列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
#                               }
#                           }
#                       ]
#                   }
#               })
#             else:
#               show.append({
#                 "type": "bubble",
#                 "body": {
#                     "type": "box",
#                     "layout": "vertical",
#                     "spacing": "sm",
#                     "contents": [
#                         {
#                             "type": "button",
#                             "flex": 1,
#                             "gravity": "center",
#                             "action": {
#                                 "type": "message",
#                                 "label": "已經到底囉！'點我'瀏覽預購/未取名單",
#                                 "text": "預購/未取名單",
#                             }
#                         }
#                     ]
#                 }
#             })
#     show = FlexSendMessage(
#             alt_text='【未取訂單】列表',
#             contents= show
#             )

#     return show