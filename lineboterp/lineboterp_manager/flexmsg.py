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
    if result is not None and len(result) > 0:
        flex_messages = []
        batch_size = 12  

        for i in range(0, len(result), batch_size):
            batch_result = result[i:i+batch_size] 

            
            message_contents = []

            for row in batch_result:
                mid = row[0]
                mname = row[1]

                message_content = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "md",
                        "contents": [
                            {"type": "text", "text": f"廠商編號: {mid}", "size": "md"},
                            {"type": "text", "text": f"廠商名稱: {mname}", "size": "md"}
                        ]
                    }
                }

               
                message_content['footer'] = {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {"type": "message", "label": "選擇此廠商", "text": f"庫存-選擇廠商 {mid}"}
                        }
                    ]
                }

                message_contents.append(message_content)

            flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "carousel", "contents": message_contents})
            flex_messages.append(flex_message)

        return flex_messages
    else:
        flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "text", "text": "找不到符合條件的廠商。"})
        return [flex_message]

def allr_manufacturers_name_flex_msg(result): 
    if result is not None and len(result) > 0:
        flex_messages = []
        batch_size = 12 

        for i in range(0, len(result), batch_size):
            batch_result = result[i:i+batch_size] 

          
            message_contents = []

            for row in batch_result:
                mid = row[0]
                mname = row[1]

                message_content = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "md",
                        "contents": [
                            {"type": "text", "text": f"廠商編號: {mid}", "size": "md"},
                            {"type": "text", "text": f"廠商名稱: {mname}", "size": "md"}
                        ]
                    }
                }

              
                message_content['footer'] = {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {"type": "message", "label": "選擇此廠商", "text": f"快速進貨-選擇廠商{mid}"}
                        }
                    ]
                }

                message_contents.append(message_content)

            flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "carousel", "contents": message_contents})
            flex_messages.append(flex_message)

        return flex_messages
    else:
        flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "text", "text": "找不到符合條件的廠商。"})
        return [flex_message]


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
#1010與下面進貨時間無法換行
def rev_pur_info_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[1]  # '商品名稱'
            purtime = row[2]

            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID：{pid}"},
                        {"type": "text", "text": f"商品名稱：{pname}"},
                        {"type": "text", "text": f"上次進貨時間：\n{purtime}"}
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
                            "label": "快速進貨商品",
                            "text": f"快速進貨-商品{pid}"
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
            purtime = row[2]

            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID：{pid}"},
                        {"type": "text", "text": f"商品名稱：{pname}"},
                        {"type": "text", "text": f"上次進貨時間：\n{purtime}"},
                        
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
                            "label": "快速進貨商品",
                            "text": f"快速進貨-商品{pid}"
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


def puring_pro_flex_msg(result): 
    if result is not None and len(result) > 0:
        flex_messages = []
        batch_size = 12  

        for i in range(0, len(result), batch_size):
            batch_result = result[i:i+batch_size]  

            
            message_contents = []

            for row in batch_result:
                pid = row[0]
                pname = row[1]
                purnum = row[2]
                purstate = row[3]
                purtime = row[4]

                message_content = {
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
                    }
                }

               
                message_content['footer'] = {
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

                message_contents.append(message_content)

            flex_message = FlexSendMessage(alt_text="進貨中商品列表", contents={"type": "carousel", "contents": message_contents})
            flex_messages.append(flex_message)

        return flex_messages
    else:
        flex_message = FlexSendMessage(alt_text="進貨中商品列表", contents={"type": "text", "text": "找不到符合條件的商品。"})
        return [flex_message]

def pured_pro_flex_msg(result):
    if result is not None and len(result) > 0:
        flex_messages = []
        batch_size = 12  

        for i in range(0, len(result), batch_size):
            batch_result = result[i:i+batch_size]  

           
            message_contents = []

            for row in batch_result:
                pid = row[0]
                pname = row[1]
                purnum = row[2]
                purstate = row[3]
                purtime = row[4]

                message_content = {
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
                    }
                }

              
                message_content['footer'] = {
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

                message_contents.append(message_content)

            flex_message = FlexSendMessage(alt_text="進貨中商品列表", contents={"type": "carousel", "contents": message_contents})
            flex_messages.append(flex_message)

        return flex_messages
    else:
        flex_message = FlexSendMessage(alt_text="進貨中商品列表", contents={"type": "text", "text": "找不到符合條件的商品。"})
        return [flex_message]

def nopur_inf_flex_msg(result):
    if result:
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='新增進貨資訊商品列表', weight='bold', size='lg'),
                ],
            ),
        )

        for row in result:
            button = ButtonComponent(
                style='link',
                height='sm',
                action = MessageAction(label=row[1],text=f"預購商品ID:{str(row[0])}~{str(row[2])}!{str(row[3])}/{str(row[4])}"
                )
            )
            bubble.body.contents.append(button)

        flex_message = FlexSendMessage(alt_text='商品ID列表', contents=bubble)
        return flex_message

def product_ing_flex_msg(result):
    if result:
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='新增現購進貨資訊商品列表', weight='bold', size='lg'),
                ],
            ),
        )

        for row in result:
            button = ButtonComponent(
                style='link',
                height='sm',
                action=MessageAction(label=row[1], text=f"現購商品ID:{str(row[0])+str(row[2])}")
            )
            bubble.body.contents.append(button)

        flex_message = FlexSendMessage(alt_text='商品ID列表', contents=bubble)
        return flex_message

##新增現購成功訊息
def check_okok(purchase_pid):
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
                    "text": "您已成功新增預購進貨商品",
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
                        "text": f"您已成功新增現購進貨商品 {purchase_pid}"
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


def checkquick_ok(purchase_pid):
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
                    "text": "您已成功快速進貨商品",
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
                        "text": f"您已成功快速進貨商品 {purchase_pid}"
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

def Order_preorder_selectionscreen(): #管理者-預購/未取
    Order_preorder_screen = []
    Order = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/vLCC99Q.jpg",
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
                    "text": "預購名單",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "※最近100筆預購訂單",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "md",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "預購訂單成立由近到遠排序",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "sm",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "可顯示預購訂單詳細內容",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "sm",
                    "weight": "bold"
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
                    "label": "預購名單列表",
                    "text": "【預購名單】列表"
                    },
                    "color": "#1a9879",
                    "style": "primary"
                }
                ],
                "flex": 0
            }
            }
    Order_preorder_screen.append(Order)
    preorder = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/5ksWY7Y.jpg",
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
                        "text": "未取名單",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "※最近100筆未取訂單",
                        "wrap": True,
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "margin": "md",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "※未取訂單成立由近到遠排序",
                        "wrap": True,
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "margin": "sm",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "※可顯示未取訂單詳細內容",
                        "wrap": True,
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "margin": "sm",
                        "weight": "bold"
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
                        "label": "未取名單列表",
                        "text": "【未取名單】列表"
                        },
                        "color": "#c42149",
                        "style": "primary"
                    }
                    ],
                    "flex": 0
                }
                }
    Order_preorder_screen.append(preorder)
    screen =FlexSendMessage(
                            alt_text='預購/未取名單列表',
                            contents={
                                "type": "carousel",
                                "contents": Order_preorder_screen   
                                } 
                            )
    return screen


