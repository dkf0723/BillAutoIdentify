import mysql.connector
import requests
from datetime import datetime, timedelta
from mysql.connector import errorcode
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from relevant_information import dbinfo,imgurinfo
import os, io, pyimgur, glob
import manager
from database import db_manufacturers,db_products_manufacturers
#-------------所有廠商名稱列出---------------
def manager_manufacturers_list():
    manufacturers_show = []
    manufacturers_list = db_manufacturers()
    if manufacturers_list == '找不到符合條件的資料。':
      manufacturers_show = TextSendMessage(text = manufacturers_list)#這邊有點不瞭解 但程式正常就沒差
    else:
      pagemin = manager.list_page[manager.user_id+'廠商數量min']
      pagemax = manager.list_page[manager.user_id+'廠商數量max']#9
      db_manufacturerss = manufacturers_list[pagemin:pagemax] #把第16行放進來 前方變數記得不要取相同名字
      manufacturers_show = [] #與第15行一樣
      mid = [] #廠商的編號
      mname = []#廠商名稱
      for manufacturers_list in db_manufacturerss: #第22行
          mid.append(manufacturers_list[0])
          mname.append(manufacturers_list[1])

      for i in range(len(mid)):
          manufacturers_show.append({
          "type": "bubble",
          "body": {
          "type": "box",
          "layout": "vertical",
          "spacing": "xxl",
          "contents": [
          {
          "type": "text",
          "text": "【依廠商】查詢",
          "size": "xl",
          "weight": "bold"},
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
            "text": f"廠商的編號 : {mid[i]}",
            "weight": "bold",
            "margin": "xs",
            "flex": 0},
            {
            "type": "text",
            "text": f"廠商名稱 : {mname[i]}",
            "flex": 0,
            "margin": "sm",
            "weight": "bold"}
            ]
            }
            ]
          },
            {
            "type": "separator",
            "margin": "lg",
            "color": "#888888"}
            ]
          },
          "footer": {
          "type": "box",
          "layout": "vertical",
          "contents": [
          {
          "type": "button",
          "style": "primary",
          "color": "#019858",
          "margin": "none",
          "action": {
                    "type": "message",
                    "label": "選我選我",
                    "text": f"選我選我 {mid[i]}"
                    },
                    "height": "md",
                    "offsetEnd": "none",
                    "offsetBottom": "sm"}
                    ],
                    "spacing": "none",
                    "margin": "none"}
                     })
      if len(manufacturers_show) >= 9:
             manufacturers_show.append({
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
                                "text": "【廠商列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                              }
                          }
                      ]
                  }
              })
      else: 
              manufacturers_show.append({
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
                                "label":"已經到底囉！ '點我回到'【查詢/修改/下架】",
                                "text": "【查詢/修改/下架】",
                            }
                        }
                    ]
                }
            })
      return manufacturers_show 
#---------------此廠商所有商品(已變數/FM)-------------------------
# def products_manufacturers_FM(result):
#   if result != []:
#     bubbles = []
#     for row in result:
#       pid = row[0]  # '商品ID'
#       pname = row[1]  # '商品名稱'
#       pphoto = row[2] # '商品圖片'
#       stock_num = row[3]  # '庫存數量'
#       pname_unit = row[4]  #  '商品單位'
#       purchase_price = row[5] #'進貨單價'
#       sell_price = row[6]  # '售出單價'
#       bubble = {
#           "type": "bubble",
#           "hero": {
#           "type": "image",
#           "url": "{}".format(pphoto),
#           "size": "full",
#           "align": "start",
#           "margin": "none",
#           "offsetTop": "none",
#           "aspectRatio": "20:14",
#           "aspectMode": "cover",
#           "offsetBottom": "xs"
#         },
#           "body": {
#           "type": "box",
#           "layout": "vertical",
#           "spacing": "xxl",
#           "contents": [
#             {
#               "type": "text",
#               "text": "【商品資訊】",
#               "size": "xl",
#               "weight": "bold"
#             },
#             {
#               "type": "box",
#               "layout": "vertical",
#               "spacing": "xl",
#               "contents": [
#                 {
#                   "type": "box",
#                   "layout": "vertical",
#                   "contents": [
#                     {
#                       "type": "text",
#                       "text": f"1.商品ID: {pid}",
#                       "weight": "bold",
#                       "margin": "xs"
#                     },
#                     {
#                       "type": "text",
#                       "text": f"2.商品名稱：{pname}",
#                       "flex": 0,
#                       "margin": "sm",
#                       "weight": "bold",
#                       "contents": []
#                     },
#                     {
#                       "type": "text",
#                       "text": f"3.庫存數量: {stock_num}",
#                       "weight": "bold",
#                       "margin": "sm"
#                     },
#                     {
#                       "type": "text",
#                       "text": f"4.商品單位: {pname_unit}",
#                       "weight": "bold",
#                       "margin": "sm"
#                     },
#                     {
#                       "type": "text",
#                       "text": f"5.進貨單價: {purchase_price}",
#                       "weight": "bold",
#                       "margin": "sm"
#                     },
#                     {
#                       "type": "text",
#                       "text": f"6.售出單價: {sell_price}",
#                       "weight": "bold",
#                       "margin": "sm"
#                     }
#                   ]
#                 }
#               ],
#               "margin": "xs"
#             },
#             {
#               "type": "separator",
#               "margin": "lg",
#               "color": "#888888"
#             }
#           ]
#         },
#         "footer": {
#           "type": "box",
#           "layout": "horizontal",
#           "contents": [
#             {
#               "type": "button",
#               "style": "primary",
#               "color": "#FF7575",
#               "margin": "none",
#               "action": {
#                 "type": "message",
#                 "label": "停售",
#                 "text": "停售"
#               },
#               "height": "md",
#               "offsetEnd": "none",
#               "offsetBottom": "sm",
#               "offsetStart": "none"
#             },
#             {
#               "type": "button",
#               "action": {
#                 "type": "message",
#                 "label": "修改商品資訊",
#                 "text": f"【修改商品資訊】{pid}"
#               },
#               "style": "primary",
#               "color": "#46A3FF",
#               "margin": "none",
#               "height": "md",
#               "offsetBottom": "sm",
#               "offsetEnd": "none",
#               "offsetStart": "xs"
#             }
#           ],
#           "spacing": "none",
#           "margin": "none"
#         }
#       }
#       bubbles.append(bubble)
#     flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "carousel", "contents": bubbles})
#   else:
#     flex_message = TextSendMessage(text =  "找不到符合條件的廠商商品。")
#   return flex_message

def manager_products_manufacturers_list(manufacturer_id): #此廠商所有商品
    products_manufacturers_show = []
    products_manufacturers_list = db_products_manufacturers(manufacturer_id)
    # products_manufacturers_list = db_products_manufacturers()
    if products_manufacturers_list == '找不到符合條件的資料。':
       products_manufacturers_show= TextSendMessage(text =products_manufacturers_list)
    else:
      pagemin = manager.list_page[manager.user_id+'廠商數量min']
      pagemax = manager.list_page[manager.user_id+'廠商數量max']#9
      db_products_manufacturerss = products_manufacturers_list[pagemin:pagemax]
      products_manufacturers_show = []
      pid = []  # '商品ID'
      pname = []  # '商品名稱'
      pphoto = [] # '商品圖片'
      stock_num = []  # '庫存數量'
      pname_unit = []  #  '商品單位'
      purchase_price = [] #'進貨單價'
      sell_price = []  # '售出單價'
      for products_manufacturers_list in db_products_manufacturerss:
          if products_manufacturers_list is None:
              break
          else:
              pid.append(products_manufacturers_list[0])
              pname.append(products_manufacturers_list[1])
              if products_manufacturers_list[2] is None:
                  img = 'https://i.imgur.com/rGlTAt3.jpg'
              else:
                  img = products_manufacturers_list[2]#商品圖片
              pphoto.append(img)
              stock_num.append(products_manufacturers_list[3])
              pname_unit.append(products_manufacturers_list[4])
              purchase_price.append(products_manufacturers_list[5])
              sell_price.append(products_manufacturers_list[6])

      for i in range(len(pid)):
          products_manufacturers_show.append({   
          "type": "bubble",
          "hero": {
          "type": "image",
          "url": pphoto[i],
          "size": "full",
          "align": "start",
          "margin": "none",
          "offsetTop": "none",
          "aspectRatio": "20:14",
          "aspectMode": "cover",
          "offsetBottom": "xs"
        },
          "body": {
          "type": "box",
          "layout": "vertical",
          "spacing": "xxl",
          "contents": [
            {
              "type": "text",
              "text": "【商品資訊】",
              "size": "xl",
              "weight": "bold"
            },
            {
              "type": "box",
              "layout": "vertical",
              "spacing": "xl",
              "contents": [
                {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                    {
                      "type": "text",
                      "text": f"1.商品ID: {pid[i]}",
                      "weight": "bold",
                      "margin": "xs"
                    },
                    {
                      "type": "text",
                      "text": f"2.商品名稱：{pname[i]}",
                      "flex": 0,
                      "margin": "sm",
                      "weight": "bold",
                      "contents": []
                    },
                    {
                      "type": "text",
                      "text": f"3.庫存數量: {stock_num[i]}",
                      "weight": "bold",
                      "margin": "sm"
                    },
                    {
                      "type": "text",
                      "text": f"4.商品單位: {pname_unit[i]}",
                      "weight": "bold",
                      "margin": "sm"
                    },
                    {
                      "type": "text",
                      "text": f"5.進貨單價: {purchase_price[i]}",
                      "weight": "bold",
                      "margin": "sm"
                    },
                    {
                      "type": "text",
                      "text": f"6.售出單價: {sell_price[i]}",
                      "weight": "bold",
                      "margin": "sm"
                    }
                  ]
                }
              ],
              "margin": "xs"
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
          "layout": "horizontal",
          "contents": [
            {
              "type": "button",
              "style": "primary",
              "color": "#FF7575",
              "margin": "none",
              "action": {
                "type": "message",
                "label": "停售",
                "text": "停售"
              },
              "height": "md",
              "offsetEnd": "none",
              "offsetBottom": "sm",
              "offsetStart": "none"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "修改商品資訊",
                "text": f"【修改商品資訊】{pid[i]}"
              },
                  "style": "primary",
                  "color": "#46A3FF",
                  "margin": "none",
                  "height": "md",
                  "offsetBottom": "sm",
                  "offsetEnd": "none",
                  "offsetStart": "xs"
                }
              ],
              "spacing": "none",
              "margin": "none"
            }
          })
      if len(products_manufacturers_show) >= 9:
                  products_manufacturers_show.append({
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
                                      "text": "【廠商列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                                    }
                                }
                            ]
                        }
                    })
      else: 
              products_manufacturers_show.append({
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
                                "label":"已經到底囉！ '點我回到'【依廠商】查詢",
                                "text": "【依廠商】查詢",
                            }
                        }
                    ]
                }
            })
      return products_manufacturers_show
#----------------分類下所有商品列表(已變數)------------------------------
def test_categoryate_FM(result):
  if result != []:
    bubbles = []
    for row in result:
      pid = row[0]  # '商品ID'
      pname = row[1]  # '商品名稱'
      pphoto = row[2] # '商品圖片'
      stock_num = row[3]  # '庫存數量'
      pname_unit = row[4]  #  '商品單位'
      purchase_price = row[5] #'進貨單價'
      sell_price = row[6]  # '售出單價'
      bubble = {
            "type": "bubble",
            "hero": {
            "type": "image",
            "url": "{}".format(pphoto),
            "size": "full",
            "align": "start",
            "margin": "none",
            "offsetTop": "none",
            "aspectRatio": "20:14",
            "aspectMode": "cover",
            "offsetBottom": "xs"
          },
            "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "xxl",
            "contents": [
              {
                "type": "text",
                "text": "【商品資訊】",
                "size": "xl",
                "weight": "bold"
              },
              {
                "type": "box",
                "layout": "vertical",
                "spacing": "xl",
                "contents": [
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": f"1.商品ID: {pid}",
                        "weight": "bold",
                        "margin": "xs"
                      },
                      {
                        "type": "text",
                        "text": f"2.商品名稱：{pname}",
                        "flex": 0,
                        "margin": "sm",
                        "weight": "bold",
                        "contents": []
                      },
                      {
                        "type": "text",
                        "text": f"3.庫存數量: {stock_num}",
                        "weight": "bold",
                        "margin": "sm"
                      },
                      {
                        "type": "text",
                        "text": f"4.商品單位: {pname_unit}",
                        "weight": "bold",
                        "margin": "sm"
                      },
                      {
                        "type": "text",
                        "text": f"5.進貨單價: {purchase_price}",
                        "weight": "bold",
                        "margin": "sm"
                      },
                      {
                        "type": "text",
                        "text": f"6.售出單價: {sell_price}",
                        "weight": "bold",
                        "margin": "sm"
                      }
                    ]
                  }
                ],
                "margin": "xs"
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
            "layout": "horizontal",
            "contents": [
              {
                "type": "button",
                "style": "primary",
                "color": "#FF7575",
                "margin": "none",
                "action": {
                  "type": "message",
                  "label": "停售",
                  "text": "停售"
                },
                "height": "md",
                "offsetEnd": "none",
                "offsetBottom": "sm",
                "offsetStart": "none"
              },
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "修該商品資訊",
                  "text":f"【修改商品資訊】{pid}"
                },
                "style": "primary",
                "color": "#46A3FF",
                "margin": "none",
                "height": "md",
                "offsetBottom": "sm",
                "offsetEnd": "none",
                "offsetStart": "xs"
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
#------該商品所有資訊(現購/依廠商或類別查詢)--------------------
# def Now_Product_Modification_FM(product_id):
#   bubble = {
#             "type": "bubble",
#             "body": {
#               "type": "box",
#               "layout": "vertical",
#               "contents": [
#                 {
#                   "type": "text",
#                   "text": "該商品所有資訊",
#                   "weight": "bold",
#                   "size": "xl",
#                   "margin": "sm",
#                   "style": "normal",
#                   "contents": []
#                 },
#                 {
#                   "type": "separator",
#                   "margin": "sm"
#                 },
#                 {
#                   "type": "box",
#                   "layout": "vertical",
#                   "margin": "md",
#                   "contents": [
#                     {
#                       "type": "button",
#                       "action": {
#                         "type": "message",
#                         "label": "修改商品名稱",
#                         "text": "【修改商品資訊】商品名稱"
#                       },
#                       "color": "#B1D3C5",
#                       "style": "secondary"
#                     },
#                     {
#                       "type": "button",
#                       "action": {
#                         "type": "message",
#                         "label": "修改商品簡介",
#                         "text": "【修改商品資訊】商品簡介"
#                       },
#                       "style": "secondary",
#                       "color": "#B1D3C5"
#                     },
#                     {
#                       "type": "button",
#                       "action": {
#                         "type": "message",
#                         "label": "修改商品售出單價",
#                         "text": "【修改商品資訊】售出單價"
#                       },
#                       "style": "secondary",
#                       "color": "#B1D3C5"
#                     },
#                     {
#                       "type": "button",
#                       "action": {
#                         "type": "message",
#                         "label": "修改商品售出單價2",
#                         "text": "【修改商品資訊】售出單價2"
#                       },
#                       "style": "secondary",
#                       "color": "#B1D3C5"
#                     },
#                     {
#                       "type": "button",
#                       "action": {
#                         "type": "message",
#                         "label": "更換商品圖片",
#                         "text": "【修改商品資訊】更換商品圖片"
#                       },
#                       "style": "secondary",
#                       "color": "#B1D3C5"
#                     }
#                   ],
#                   "spacing": "xs"
#                 }
#               ]
#             },
#             "footer": {
#               "type": "box",
#               "layout": "vertical",
#               "contents": [
#                 {
#                   "type": "button",
#                   "action": {
#                     "type": "message",
#                     "label": "取消修改動作",
#                     "text": "取消"
#                   },
#                   "style": "secondary",
#                   "color": "#EAD880"
#                 }
#               ],
#               "spacing": "xs",
#               "margin": "md"
#             },
#             "styles": {
#               "footer": {
#                 "separator": True
#               }
#             }
#           }
#   return FlexSendMessage(alt_text="產品修改選項", contents=bubble)
#------該商品所有資訊(預購/依廠商或類別查詢)---------------------
# def Pre_Product_Modification_FM(product_id):
#   bubble = {        
#             "type": "bubble",
#             "body": {
#               "type": "box",
#               "layout": "vertical",
#               "contents": [
#                 {
#                   "type": "text",
#                   "text": "該商品所有資訊",
#                   "weight": "bold",
#                   "size": "xl",
#                   "margin": "sm",
#                   "style": "normal",
#                   "contents": []
#                 },
#                 {
#                   "type": "separator",
#                   "margin": "sm"
#                 },
#                 {
#                   "type": "box",
#                   "layout": "vertical",
#                   "margin": "md",
#                   "contents": [
#                     {
#                       "type": "button",
#                       "action": {
#                         "type": "message",
#                         "label": "修改商品名稱",
#                         "text": "【修改商品資訊】商品名稱"
#                       },
#                       "color": "#CE8467",
#                       "style": "secondary"
#                     },
#                     {
#                       "type": "button",
#                       "action": {
#                         "type": "message",
#                         "label": "修改商品簡介",
#                         "text": "【修改商品資訊】商品簡介"
#                       },
#                       "style": "secondary",
#                       "color": "#CE8467"
#                     },
#                     {
#                       "type": "button",
#                       "action": {
#                         "type": "message",
#                         "label": "修改商品售出單價",
#                         "text": "【修改商品資訊】售出單價"
#                       },
#                       "style": "secondary",
#                       "color": "#CE8467"
#                     },
#                     {
#                       "type": "button",
#                       "action": {
#                         "type": "message",
#                         "label": "修改商品售出單價2",
#                         "text": "【修改商品資訊】售出單價2"
#                       },
#                       "style": "secondary",
#                       "color": "#CE8467"
#                     },
#                     {
#                       "type": "button",
#                       "action": {
#                         "type": "message",
#                         "label": "修改商品預購倍數",
#                         "text": "【修改商品資訊】預購倍數"
#                       },
#                       "style": "secondary",
#                       "color": "#CE8467"
#                     },
#                     {
#                       "type": "button",
#                       "action": {
#                         "type": "message",
#                         "label": "修改商品預購截止時間",
#                         "text": "【修改商品資訊】預購截止時間"
#                       },
#                       "color": "#CE8467",
#                       "style": "secondary"
#                     },
#                     {
#                       "type": "button",
#                       "action": {
#                         "type": "message",
#                         "label": "更換商品圖片",
#                         "text": "【修改商品資訊】更換商品圖片"
#                       },
#                       "color": "#CE8467",
#                       "style": "secondary"
#                     }
#                   ],
#                   "spacing": "xs"
#                 }
#               ]
#             },
#             "footer": {
#               "type": "box",
#               "layout": "vertical",
#               "contents": [
#                 {
#                   "type": "button",
#                   "action": {
#                     "type": "message",
#                     "label": "取消修改動作",
#                     "text": "取消"
#                   },
#                   "style": "secondary",
#                   "color": "#EAD880"
#                 }
#               ],
#               "spacing": "xs",
#             },
#              "styles": {
#                "footer": {
#                  "separator": True
#                }
#              }
#            }
#   return FlexSendMessage(alt_text="產品修改選項", contents=bubble)
#---------該商品所有資訊(現購/依廠商或類別查詢)測試---------------------
def Now_Product_Modification_FM(product_id):
    bubble =  {
              "type": "bubble",
              # "hero": {
              #   "type": "image",
              #   "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
              #   "size": "full",
              #   "aspectRatio": "20:13",
              #   "aspectMode": "cover"
              # },
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "現購商品所有資訊",
                    "weight": "bold",
                    "size": "xl",
                    "margin": "none",
                    "style": "normal",
                    "contents": [],
                    "align": "center"
                  },
                  {
                    "type": "text",
                    "text": "1.商品名稱：",
                    "margin": "md",
                    "weight": "bold"
                  },
                  {
                    "type": "text",
                    "text": "2.商品簡介：",
                    "margin": "sm",
                    "weight": "bold"
                  },
                  {
                    "type": "text",
                    "text": "4.商品單價：",
                    "weight": "bold",
                    "margin": "sm"
                  },
                  {
                    "type": "text",
                    "text": "4.商品單價2：",
                    "margin": "sm",
                    "weight": "bold"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "contents": [
                      {
                        "type": "button",
                        "action": {
                          "type": "message",
                          "label": "修改商品名稱",
                          "text":"【修改商品資訊】商品名稱"
                        },
                        "color": "#B1D3C5",
                        "style": "secondary"
                      },
                      {
                        "type": "button",
                        "action": {
                          "type": "message",
                          "label": "修改商品簡介",
                          "text": "【修改商品資訊】商品簡介"
                        },
                        "style": "secondary",
                        "color": "#B1D3C5"
                      },
                      {
                        "type": "button",
                        "action": {
                          "type": "message",
                          "label": "修改商品售出單價",
                          "text": "【修改商品資訊】售出單價"
                        },
                        "style": "secondary",
                        "color": "#B1D3C5"
                      },
                      {
                        "type": "button",
                        "action": {
                          "type": "message",
                          "label": "修改商品售出單價2",
                          "text": "【修改商品資訊】售出單價2"
                        },
                        "style": "secondary",
                        "color": "#B1D3C5"
                      },
                      {
                        "type": "button",
                        "action": {
                          "type": "message",
                          "label": "更換商品圖片",
                          "text": "【修改商品資訊】更換商品圖片"
                        },
                        "style": "secondary",
                        "color": "#B1D3C5"
                      }
                    ],
                    "spacing": "xs"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "取消修改動作",
                      "text": "取消"
                    },
                    "style": "secondary",
                    "color": "#EAD880"
                  }
                ],
                "spacing": "xs",
                "margin": "md"
              },
              "styles": {
                "footer": {
                  "separator": True
                }
              }
            }
    return FlexSendMessage(alt_text="產品修改選項", contents=bubble)
#------該商品所有資訊(預購/依廠商或類別查詢)測試---------------------
def Pre_Product_Modification_FM(product_id):
  bubble = {
            "type": "bubble",
            # "hero": {
            #   "type": "image",
            #   "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
            #   "size": "full",
            #   "aspectMode": "cover",
            #   "aspectRatio": "20:13"
            # },
            "body": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": "預購商品所有資訊",
                  "weight": "bold",
                  "size": "xl",
                  "margin": "none",
                  "style": "normal",
                  "contents": [],
                  "decoration": "none",
                  "align": "center"
                },
                {
                  "type": "text",
                  "text": "1.商品名稱 :",
                  "weight": "bold",
                  "margin": "md"
                },
                {
                  "type": "text",
                  "text": "2.商品簡介 :",
                  "weight": "bold",
                  "margin": "sm"
                },
                {
                  "type": "text",
                  "text": "3.商品售出單價 :",
                  "weight": "bold",
                  "margin": "sm"
                },
                {
                  "type": "text",
                  "text": "4.商品售出單價2:",
                  "weight": "bold",
                  "margin": "sm"
                },
                {
                  "type": "separator",
                  "margin": "sm"
                },
                {
                  "type": "box",
                  "layout": "vertical",
                  "margin": "md",
                  "contents": [
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品名稱",
                        "text": "【修改商品資訊】商品名稱"
                      },
                      "color": "#CE8467",
                      "style": "secondary"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品簡介",
                        "text": "【修改商品資訊】商品簡介"
                      },
                      "style": "secondary",
                      "color": "#CE8467"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品售出單價",
                        "text": "【修改商品資訊】售出單價"
                      },
                      "style": "secondary",
                      "color": "#CE8467"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品售出單價2",
                        "text": "【修改商品資訊】售出單價2"
                      },
                      "style": "secondary",
                      "color": "#CE8467"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品預購倍數",
                        "text": "【修改商品資訊】預購倍數"
                      },
                      "style": "secondary",
                      "color": "#CE8467"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品預購截止時間",
                        "text": "【修改商品資訊】預購截止時間"
                      },
                      "color": "#CE8467",
                      "style": "secondary"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "更換商品圖片",
                        "text": "【修改商品資訊】更換商品圖片"
                      },
                      "color": "#CE8467",
                      "style": "secondary"
                    }
                  ],
                  "spacing": "xs"
                }
              ]
            },
            "footer": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "取消修改動作",
                    "text": "取消"
                  },
                  "style": "secondary",
                  "color": "#EAD880"
                }
              ],
              "spacing": "xs",
              "margin": "md"
            },
            "styles": {
              "footer": {
                "separator": True
              }
            }
          }
  return FlexSendMessage(alt_text="產品修改選項", contents=bubble)