from linebot.models import TextSendMessage,FlexSendMessage
from database  import preorder_list, orderdt
#---------------預購/未取------------
def manager_preorder_list():
    db_nottaken = preorder_list()
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
                            "text": "預購訂單查詢",
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
