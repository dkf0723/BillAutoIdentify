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
        batch_size = 12  # 设置每批消息的最大数量

        for i in range(0, len(result), batch_size):
            batch_result = result[i:i+batch_size]  # 获取当前批次的结果

            # 创建一个列表以存储消息内容
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

                # 添加商品已到货按钮
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
        batch_size = 12  # 设置每批消息的最大数量

        for i in range(0, len(result), batch_size):
            batch_result = result[i:i+batch_size]  # 获取当前批次的结果

            # 创建一个列表以存储消息内容
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

                # 添加商品已到货按钮
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
                        {"type": "text", "text": f"上次進貨時間：{purtime}"},
                        
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
##1008
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
                        {"type": "text", "text": f"上次進貨時間：{purtime}"},
                        
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

##1008
def puring_pro_flex_msg(result): 
    if result is not None and len(result) > 0:
        flex_messages = []
        batch_size = 12  # 设置每批消息的最大数量

        for i in range(0, len(result), batch_size):
            batch_result = result[i:i+batch_size]  # 获取当前批次的结果

            # 创建一个列表以存储消息内容
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

                # 添加商品已到货按钮
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
        batch_size = 12  # 设置每批消息的最大数量

        for i in range(0, len(result), batch_size):
            batch_result = result[i:i+batch_size]  # 获取当前批次的结果

            # 创建一个列表以存储消息内容
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

                # 添加商品已到货按钮
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
