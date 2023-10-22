from linebot.models import *
import database
def showOrder(orderDetails):
    Notpickedup_preordered_history_screen = []
    for i in orderDetails :        
        orderDetail = {
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
                                "text": "購物車訂單確認",
                                "weight": "bold",
                                "size": "xl",
                                "margin": "md",
                                "align": "center"
                            },
                            {
                                "type": "separator",
                                "margin": "xxl"
                            },
                            {
                                "type": "text",
                                "text": "訂單內容",
                                "size": "sm",
                                "margin": "lg",
                                "wrap": True
                            },
                           
                            {
                                "type": "separator",
                                "margin": "xxl"
                            },
                            {
                                "type": "text",
                                "text": f"總額：NT${database.getTotalByOrder(i[0][0])}",
                                "size": "md",
                                "margin": "lg",
                                "align": "center",
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
                                "text": "【確認】"
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                "type": "message",
                                "label": "【2.取消】",
                                "text": "【取消】"
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
        count = 5
        for j in i :
                sum=int(j[2])*int(j[3])
                a={
                      "type": "text",
                      "text":f'{j[1]}',
                      "margin": "10px"
                  }
                b={
                    "type": "text",
                    "text": f"{ j[2]}*{j[3]}={sum}$",
                    "align": "end"
                }
                orderDetail['body']['contents'].insert(count,a)
                orderDetail['body']['contents'].insert(count+1,b)
                count += 2
        Notpickedup_preordered_history_screen.append(orderDetail)
    screen =FlexSendMessage(
                            alt_text='未取/預購/歷史訂單選擇',
                            contents={
                                "type": "carousel",
                                "contents": Notpickedup_preordered_history_screen   
                                } 
                            )
    return screen