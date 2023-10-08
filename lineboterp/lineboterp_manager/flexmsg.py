from linebot.models import FlexSendMessage
from linebot.models.flex_message import BubbleContainer, BoxComponent, TextComponent
import mysql.connector
import requests
from datetime import datetime, timedelta
import time
from mysql.connector import errorcode
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from relevant_information import imgurinfo
import os, io, pyimgur, glob
import manager



def alls_manufacturers_name_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            mid = row[0]
            mname = row[1]
            bubble = {               
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                {
                    "type": "text",
                    "text": "廠商查詢",
                    "size": "xl",
                    "weight": "bold"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": f"【廠商編號】: {mid}",
                            "weight": "bold",
                            "margin": "sm",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": f"【廠商名稱】: {mname}",
                            "flex": 0,
                            "margin": "sm",
                            "weight": "bold"
                        }
                        ]
                    }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#888888"
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#905c44",
                    "margin": "none",
                    "action": {
                    "type": "message",
                    "label": "選擇此廠商",
                    "text": f"庫存-選擇廠商 {mid}"
                    },
                    "height": "md",
                    "offsetEnd": "none",
                    "offsetBottom": "sm"
                }
                ],
                "spacing": "none",
                "margin": "none"
            }
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "text", "text": "找不到符合條件的廠商。"})
    
    return flex_message


def allp_manufacturers_name_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            mid = row[0]
            mname = row[1]
            bubble = {               
              "type": "bubble",
              "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                  {
                    "type": "text",
                    "text": "廠商查詢",
                    "size": "xl",
                    "weight": "bold"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": f"【廠商編號】: {mid}",
                            "weight": "bold",
                            "margin": "sm",
                            "flex": 0
                          },
                          {
                            "type": "text",
                            "text": f"【廠商名稱】: {mname}",
                            "flex": 0,
                            "margin": "sm",
                            "weight": "bold"
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#888888"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "style": "primary",
                    "color": "#905c44",
                    "margin": "none",
                    "action": {
                      "type": "message",
                      "label": "選擇此廠商",
                      "text": f"進貨-選擇廠商 {mid}"
                    },
                    "height": "md",
                    "offsetEnd": "none",
                    "offsetBottom": "sm"
                  }
                ],
                "spacing": "none",
                "margin": "none"
              }
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "text", "text": "找不到符合條件的廠商。"})
    
    return flex_message


#----------------修改-查詢所有廠商名稱--------------------
def allr_manufacturers_name_flex_msg(result):    
    if result is not None:
        bubbles = []
        for row in result:
            mid = row[0]
            mname = row[1]
            bubble = {               
              "type": "bubble",
              "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                  {
                    "type": "text",
                    "text": "廠商查詢",
                    "size": "xl",
                    "weight": "bold"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": f"【廠商編號】: {mid}",
                            "weight": "bold",
                            "margin": "sm",
                            "flex": 0
                          },
                          {
                            "type": "text",
                            "text": f"【廠商名稱】: {mname}",
                            "flex": 0,
                            "margin": "sm",
                            "weight": "bold"
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#888888"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "style": "primary",
                    "color": "#905c44",
                    "margin": "none",
                    "action": {
                      "type": "message",
                      "label": "選擇此廠商",
                      "text": f"修改-選擇廠商 {mid}"
                    },
                    "height": "md",
                    "offsetEnd": "none",
                    "offsetBottom": "sm"
                  }
                ],
                "spacing": "none",
                "margin": "none"
              }
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "text", "text": "找不到符合條件的廠商。"})
    
    return flex_message

#--------------依廠商->庫存資訊---------------
def stock_manufacturers_flex_msg(result):
    if result:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[1]  # '商品名稱'
            stock_num = row[2]  # '庫存數量'
            sell_price = row[3]  # '售出單價'

            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID: {pid}"},
                        {"type": "text", "text": f"商品名稱: {pname}"},
                        {"type": "text", "text": f"庫存數量: {stock_num}"},
                        {"type": "text", "text": f"售出單價: {sell_price}"}
                    ]
                },
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "text", "text": "找不到符合條件的廠商商品。"})
    return flex_message
'''def stock_manufacturers_flex_msg(result):
    if result:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[1]  # '商品名稱'
            stock_num = row[2]  # '庫存數量'
            sell_price = row[3]  # '售出單價'

            bubble = {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "商品信息", "color": "#ffffff", "align": "start", "size": "sm"},
                        {"type": "text", "text": f"商品名稱: {pname}", "color": "#ffffff", "size": "lg", "margin": "md"},
                    ],
                    "backgroundColor": "#0074c2",
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {"type": "text", "text": f"商品ID: {pid}", "size": "sm", "color": "#555555"},
                        {"type": "text", "text": f"庫存數量: {stock_num}", "size": "sm", "color": "#555555"},
                        {"type": "text", "text": f"售出單價: {sell_price}", "size": "sm", "color": "#555555"},
                    ],
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "button", "style": "primary", "color": "#0074c2", "action": {"type": "message", "label": "查看詳細", "text": f"詳細 {pid}"}},
                        {"type": "button", "style": "secondary", "color": "#dddddd", "action": {"type": "message", "label": "加入購物車", "text": f"加入購物車 {pid}"}},
                    ],
                },
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "text", "text": "找不到符合條件的廠商商品。"})
    return flex_message'''


#-----------------依分類->庫存資訊-----------------
def stock_categoryate_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[1]  # '商品名稱'
            stock_num = row[2]  # '庫存數量'
            sell_price = row[3]  # '售出單價'

            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID：{pid}"},
                        {"type": "text", "text": f"商品名稱：{pname}"},
                        {"type": "text", "text": f"庫存數量：{stock_num}"},
                        {"type": "text", "text": f"售出單價：{sell_price}"},
                    ]
                }
            }
            bubbles.append(bubble)

        flex_message = FlexSendMessage(
            alt_text="類別下所有商品",
            contents={
                "type": "carousel",
                "contents": bubbles
            }
        )
    else:
        flex_message = FlexSendMessage(
            alt_text="類別下所有商品",
            contents={
                "type": "text",
                "text": "找不到符合條件的資料。"
            }
        )
    return flex_message

#--------------依廠商->進貨資訊---------------
def purchase_manufacturers_flex_msg(result):
    if result:
        bubbles = []
        for row in result:
            pid = row[1]  # '商品ID'
            pname = row[19]  # '商品名稱'
            purch_num = row[13]  # '進貨數量'
            purch_price = row[14]  # '進貨單價'
            purch_time = row[15]  # '進貨時間'
            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID: {pid}"},
                        {"type": "text", "text": f"商品名稱: {pname}"},
                        {"type": "text", "text": f"進貨數量: {purch_num}"},
                        {"type": "text", "text": f"進貨單價: {purch_price}"},
                        {"type": "text", "text": f"進貨時間: {purch_time}"}

                    ]
                },
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "text", "text": "找不到符合條件的廠商商品。"})
    return flex_message

#-----------------依分類->進貨資訊-----------------
def purchase_categoryate_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[1]  # '商品ID'
            pname = row[19]  # '商品名稱'
            purch_num = row[13]  # '進貨數量'
            purch_price = row[14]  # '進貨單價'
            purch_time = row[15]  # '進貨時間'

            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID: {pid}"},
                        {"type": "text", "text": f"商品名稱: {pname}"},
                        {"type": "text", "text": f"進貨數量: {purch_num}"},
                        {"type": "text", "text": f"進貨單價: {purch_price}"},
                        {"type": "text", "text": f"進貨時間: {purch_time}"}
                    ]
                },
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "text", "text": "找不到符合條件的廠商商品。"})
    return flex_message


def new_pur_info_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[1]  # '商品ID'
            mid = row[0]  # '廠商編號'

            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID：{pid}"},
                        {"type": "text", "text": f"廠商編號：{mid}"},
                        
                    ]
                }
            }
            bubbles.append(bubble)

        flex_message = FlexSendMessage(
            alt_text="類別下所有商品",
            contents={
                "type": "carousel",
                "contents": bubbles
            }
        )
    else:
        flex_message = FlexSendMessage(
            alt_text="類別下所有商品",
            contents={
                "type": "text",
                "text": "找不到符合條件的資料。"
            }
        )
    return flex_message

def rev_pur_info_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[1]  # '商品名稱'

            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID：{pid}"},
                        {"type": "text", "text": f"商品名稱：{pname}"},
                        
                    ]
                },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#905c44",
                            "margin": "none",
                            "action": {
                            "type": "message",
                            "label": "修改此商品進貨資訊",
                            "text": f"修改-商品{pid}"
                            },
                            "height": "md",
                            "offsetEnd": "none",
                            "offsetBottom": "sm"
                        }
                        ],
                        "spacing": "none",
                        "margin": "none"
                    }
                    }
            bubbles.append(bubble)

        flex_message = FlexSendMessage(
            alt_text="類別下所有商品",
            contents={
                "type": "carousel",
                "contents": bubbles
            }
        )
    else:
        flex_message = FlexSendMessage(
            alt_text="類別下所有商品",
            contents={
                "type": "text",
                "text": "找不到符合條件的資料。"
            }
        )
    return flex_message

def revc_pur_info_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[1]  # '商品名稱'

            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID：{pid}"},
                        {"type": "text", "text": f"商品名稱：{pname}"},
                        
                    ]
                },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#905c44",
                            "margin": "none",
                            "action": {
                            "type": "message",
                            "label": "修改此商品進貨資訊",
                            "text": f"修改-商品{pid}"
                            },
                            "height": "md",
                            "offsetEnd": "none",
                            "offsetBottom": "sm"
                        }
                        ],
                        "spacing": "none",
                        "margin": "none"
                    }
                    }
            bubbles.append(bubble)

        flex_message = FlexSendMessage(
            alt_text="類別下所有商品",
            contents={
                "type": "carousel",
                "contents": bubbles
            }
        )
    else:
        flex_message = FlexSendMessage(
            alt_text="類別下所有商品",
            contents={
                "type": "text",
                "text": "找不到符合條件的資料。"
            }
        )
    return flex_message

##1008調整怎麼加入12個以上的卡片資訊
def puring_pro_flex_msg(result):
    if result is not None and len(result) > 0:
        all_flex_messages = []
        batch_size = 12  # 设置每批消息的最大数量

        for i in range(0, len(result), batch_size):
            batch_result = result[i:i+batch_size]  # 获取当前批次的结果

            bubbles = []
            for row in batch_result:
                pid = row[0]
                pname = row[1]
                purnum = row[2]
                purstate = row[3]
                purtime = row[4]

                bubble = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "md",
                        "contents": [
                            {"type": "text", "text": f"商品ID: {pid}", "weight": "bold", "size": "xl"},
                            {"type": "text", "text": f"商品名稱: {pname}", "weight": "bold", "size": "xl"},
                            {"type": "text", "text": f"進貨數量: {purnum}", "size": "md"},
                            {"type": "text", "text": f"進貨狀態: {purstate}", "size": "md"},
                            {"type": "text", "text": f"進貨時間: {purtime}", "size": "md"}
                        ]
                    },
                }

                # 添加商品已到货按钮
                bubble['footer'] = {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {"type": "message", "label": "商品已到貨", "text": f"商品已到貨{pid}"}
                        }
                    ]
                }

                bubbles.append(bubble)

            flex_message = FlexSendMessage(alt_text="此商品已到貨列表", contents={"type": "carousel", "contents": bubbles})
            all_flex_messages.append(flex_message)

        return all_flex_messages
    else:
        flex_message = FlexSendMessage(alt_text="此商品已到貨列表", contents={"type": "text", "text": "找不到符合條件的商品。"})
        return [flex_message]


    
def pured_pro_flex_msg(result):
    if result is not None and len(result) > 0:
        all_flex_messagess = []
        batch_size = 12  # 设置每批消息的最大数量

        for i in range(0, len(result), batch_size):
            batch_result = result[i:i+batch_size]  # 获取当前批次的结果

            bubbles = []
            for row in batch_result:
                pid = row[0]
                pname = row[1]
                purnum = row[2]
                purstate = row[3]
                purtime = row[4]

                bubble = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "md",
                        "contents": [
                            {"type": "text", "text": f"商品ID: {pid}", "weight": "bold", "size": "xl"},
                            {"type": "text", "text": f"商品名稱: {pname}", "weight": "bold", "size": "xl"},
                            {"type": "text", "text": f"進貨數量: {purnum}", "size": "md"},
                            {"type": "text", "text": f"進貨狀態: {purstate}", "size": "md"},
                            {"type": "text", "text": f"進貨時間: {purtime}", "size": "md"}
                        ]
                    },
                }
                bubbles.append(bubble)

            flex_message = FlexSendMessage(alt_text="此商品已到貨列表", contents={"type": "carousel", "contents": bubbles})
            all_flex_messagess.append(flex_message)

        return all_flex_messagess
    else:
        flex_message = FlexSendMessage(alt_text="此商品已到貨列表", contents={"type": "text", "text": "找不到符合條件的商品。"})
        return [flex_message]  # 返回包含单个消息的列表
    
def order_inf_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[0] # '商品ID'
            ordernum = row[1] # '訂單編號'
            orderstate = row[2] # '訂單狀態未取已取'
            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID: {pid}"},
                        {"type": "text", "text": f"訂單編號: {ordernum}"},
                        {"type": "text", "text": f"訂單狀態: {orderstate}"}
                    ]
                },
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="此商品已到貨列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="此商品已到貨列表", contents={"type": "text", "text": "找不到符合條件的廠商商品。"})
    return flex_message

def preorder_end_flex_msg(result):
    if result is not None and len(result) > 0:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[1]  # '商品名稱'
            nowprepro = row[2] # '現預購商品'
    
            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {"type": "text", "text": f"商品ID: {pid}","size": "md" },
                        {"type": "text", "text": f"商品名稱: {pname}","size": "md" },
                        {"type": "text", "text": f"現預購商品: {nowprepro}", "size": "md"},
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {
                                "type": "message",
                                "label": "預購進貨",
                                "text": f"預購進貨 {pid}" 
                            }
                        }
                    ]
                }
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="此商品已到貨列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="此商品已到貨列表", contents={"type": "text", "text": "找不到符合條件的廠商商品。"})
    return flex_message

def nopur_inf_flex_msg(result):
    if result:
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='新增進貨資訊商品ID列表', weight='bold', size='lg'),
                ],
            ),
        )

        for row in result:
            button = ButtonComponent(
                style='link',
                height='sm',
                action=MessageAction(label=row[1], text=f"商品ID:{str(row[0])+str(row[2])}")
            )
            bubble.body.contents.append(button)

        flex_message = FlexSendMessage(alt_text='商品ID列表', contents=bubble)
        return flex_message

def check_ok(purchase_pid):
    bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "weight": "bold",
                    "size": "xl",
                    "margin": "none",
                    "text": "您已成功新增進貨商品",
                    "gravity": "center",
                    "align": "center"
                },
                {
                    "type": "separator",
                    "margin": "sm"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "button",
                        "action": {
                        "type": "message",
                        "label": "完成",
                        "text": f"您已成功新增進貨商品 {purchase_pid}"
                        },
                        "margin": "xs",
                        "position": "relative",
                        "style": "primary",
                        "gravity": "center"
                    }
                    ],
                    "spacing": "xs"
                }
                ],
                "margin": "none",
                "spacing": "none"
            },
            "styles": {
                "footer": {
                "separator": True
                }
            }
            }
    return FlexSendMessage(alt_text="新增確認選項", contents = bubble)
