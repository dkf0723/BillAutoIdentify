from linebot.models import FlexSendMessage
from linebot.models.flex_message import BubbleContainer, BoxComponent, TextComponent
from mysql.connector import errorcode
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from relevant_information import imgurinfo
import manager
from database import db_quick_purchase_manufacturers,db_quickmanu_pro,db_stock_manufacturers_name,db_stock_manuinf,db_stock_categoryinf,db_puring_pro,db_pured_pro

#--------------------未有進貨資訊的預購商品列表---------------------------
def nopur_inf_flex_msg(result):
    if result:
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='新增進貨資訊預購商品列表', weight='bold', size='lg'),
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

        flex_message = FlexSendMessage(alt_text='預購商品列表', contents=bubble)
        return flex_message

#----------------------抓取未有進貨資訊的預購商品列表-------------------------
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

#---------------------------快速進貨-依廠商查詢所有廠商名稱-------------------------------
def quick_purchase_manufacturers_list(): 
    qpmanufacturers_name_show = []
    qpmanufacturers_name_list = db_quick_purchase_manufacturers()
    if qpmanufacturers_name_list == '找不到符合條件的資料。':
      qpmanufacturers_name_show= TextSendMessage(text = qpmanufacturers_name_list)
    else:
      pagemin = manager.list_page[manager.user_id+'廠商數量min']
      pagemax = manager.list_page[manager.user_id+'廠商數量max']
      db_quick_purchase_manufacturerss = qpmanufacturers_name_list[pagemin:pagemax] 
      qpmanufacturers_name_show = []
      mid = []
      mname = []
      for qpmanufacturers_name_list in db_quick_purchase_manufacturerss: 
        zero = qpmanufacturers_name_list[0]
        mid.append(zero)
        one = qpmanufacturers_name_list[1]
        mname.append(one)
      for i in range(len(mid)):
        qpmanufacturers_name_show.append({
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "【快速進貨】依廠商",
                "weight": "bold",
                "size": "xl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "廠商編號",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f" {mid[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "廠商名稱",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text":f" {mname[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
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
                "style": "primary",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "選擇此廠商",
                "text": f"快速進貨-選擇廠商{mid[i]}"
                },
                "color": "#EB6C93"
            }
            ],
            "flex": 0
        }
        })
      if len(qpmanufacturers_name_show) >= 9:
        qpmanufacturers_name_show.append({
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
                      "text": "【廠商查詢列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                      }
                    }
                ]
            }
        })
      else: 
        qpmanufacturers_name_show.append({
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
                      "label":"已經到底囉！ '點我回到'選擇商品查詢方式",
                      "text": "【進貨商品】快速進貨",
                    }
                  }
              ]
          }
      })
    return qpmanufacturers_name_show 
#-----------------快速進貨->依廠商查詢所有商品的商品ID及商品名稱-----------------
def quickmanu_pro_list(manufacturerR_id):
    quickmanupro_show = []
    quickmanupro_list = db_quickmanu_pro(manufacturerR_id)
    if quickmanupro_list == '找不到符合條件的資料。':
       quickmanupro_show = TextSendMessage(text =quickmanupro_list) 
    else:
      pagemin = manager.list_page[manager.user_id+'廠商數量min']
      pagemax = manager.list_page[manager.user_id+'廠商數量max']
      db_quickmanu_pros = quickmanupro_list[pagemin:pagemax]
      quickmanupro_show = []
      pid = []  
      pname = []  
      purtime = []
      statepro = []
      for quickmanupro_list in db_quickmanu_pros:
        zero = quickmanupro_list[0]
        pid.append(zero)
        one = quickmanupro_list[1]
        pname.append(one)
        two = quickmanupro_list[2]
        purtime.append(two)
        three= quickmanupro_list[3]
        statepro.append(three)
      for i in range (len(pid)):
        quickmanupro_show.append({
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "【廠商】快速進貨商品",
                "weight": "bold",
                "size": "xl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "商品ID：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f"{pid[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "商品名稱：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f"{pname[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "上次進貨時間：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f"{purtime[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "現預購商品：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f"{statepro[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
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
                "style": "primary",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "選擇此商品",
                "text": f"快速進貨-{statepro[i]}~{pid[i]}"
                },
                "color": "#EF97B2"
            }
            ],
            "flex": 0
        }
        })
    if len(quickmanupro_show) >= 9:
      quickmanupro_show.append({
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
                      "text": "【快速進貨商品列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                        }
                    }
                ]
            }
        })
    else: 
      quickmanupro_show.append({
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
                    "label":"已經到底囉！'點我回到'【所有廠商列表】",
                    "text": "【快速進貨】廠商",
                    }
                }
            ]
        }
    })
    return quickmanupro_show   
#------------------快速進貨->依分類查詢所有商品的商品ID及商品名稱-------------------
###################
def revc_pur_info_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[0]  
            pname = row[1]  
            purtime = row[2]
            statepro = row[3]

            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID：{pid}"},
                        {"type": "text", "text": f"商品名稱：{pname}"},
                        {"type": "text", "text": f"上次進貨時間：\n{purtime}"},
                        {"type": "text", "text": f"現預購商品：\n{statepro}"}
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
                            "text": f"快速進貨-{statepro}商品{pid}"
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

#-----------------------庫存-查詢所有廠商編號及廠商名------------------------
def stock_manufacturers_name_list(): 
    stock_manufacturers_show = []
    stock_manufacturers_list = db_stock_manufacturers_name()
    if stock_manufacturers_list == '找不到符合條件的資料。':
      stock_manufacturers_show= TextSendMessage(text = stock_manufacturers_list)
    else:
      pagemin = manager.list_page[manager.user_id+'廠商數量min']
      pagemax = manager.list_page[manager.user_id+'廠商數量max']
      db_stock_manufacturers_names = stock_manufacturers_list[pagemin:pagemax] 
      stock_manufacturers_show = []
      mid = [] 
      mname = []
      for stock_manufacturers_list in db_stock_manufacturers_names: 
        zero = stock_manufacturers_list[0]
        mid.append(zero)
        one = stock_manufacturers_list[1]
        mname.append(one)
      for i in range(len(mid)):
        stock_manufacturers_show.append({
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "【庫存查詢】依廠商",
                "weight": "bold",
                "size": "xl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "廠商編號",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f" {mid[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "廠商名稱",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text":f" {mname[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
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
                "style": "primary",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "選擇此廠商",
                "text": f"庫存-選擇廠商{mid[i]}"
                },
                "color": "#21C49C"
            }
            ],
            "flex": 0
        }
        })
      if len(stock_manufacturers_show) >= 9:
        stock_manufacturers_show.append({
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
                      "text": "【庫存廠商查詢列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                      }
                    }
                ]
            }
        })
      else: 
        stock_manufacturers_show.append({
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
                      "label":"已經到底囉！ '點我回到'選擇商品查詢方式",
                      "text": "【查詢】所有庫存",
                    }
                  }
              ]
          }
      })
    return stock_manufacturers_show
#-------------------庫存-選擇此廠商的商品庫存資訊------------------------
def stock_manuinf_list(manufacturerZ_id):
    manuinf_show = []
    manuinf_list = db_stock_manuinf(manufacturerZ_id)
    if manuinf_list == '找不到符合條件的資料。':
      manuinf_show = TextSendMessage(text = manuinf_list)
    else:
      pagemin = manager.list_page[manager.user_id+'廠商數量min']
      pagemax = manager.list_page[manager.user_id+'廠商數量max']
      db_stock_manuinfs = manuinf_list[pagemin:pagemax] 
      manuinf_show = [] 
      pid = [] 
      pname = []
      stock_num = []
      sell_price = []
      sell_price2 = []
      for manuinf_list in db_stock_manuinfs: 
        zero = manuinf_list[0]
        pid.append(zero)
        one = manuinf_list[1]
        pname.append(one)
        two= manuinf_list[2]
        stock_num .append(two)
        three = manuinf_list[3]
        sell_price.append(three)
        four = manuinf_list[4]
        sell_price2.append(four)
      for i in range(len(pid)):
        manuinf_show.append({
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "【廠商】庫存查詢商品",
                "weight": "bold",
                "size": "xl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "商品ID：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f" {pid[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "商品名稱：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text":f" {pname[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "庫存數量：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text":f" {stock_num[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "售出單價：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f" {sell_price[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "售出單價２：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f" {sell_price2[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                }
                ]
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [],
            "flex": 0
        }
        })
      if len(manuinf_show) >= 9:
        manuinf_show.append({
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
                      "text": "【庫存商品列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                      }
                    }
                ]
            }
        })
      else: 
        manuinf_show.append({
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
                      "label":"'點我回到'【庫存查詢】",
                      "text": "【庫存查詢】廠商",
                    }
                  }
              ]
          }
      })
    return manuinf_show 
#-------------------庫存->選擇此類別的商品庫存資訊------------------------
def stock_categoryinf_list(selectedD_category):
    categoryinf_show = []
    categoryinf_list = db_stock_categoryinf(selectedD_category)
    if categoryinf_list == '找不到符合條件的資料。':
      categoryinf_show = TextSendMessage(text = categoryinf_list)
    else:
      pagemin = manager.list_page[manager.user_id+'廠商數量min']
      pagemax = manager.list_page[manager.user_id+'廠商數量max']
      db_stock_categoryinfs = categoryinf_list[pagemin:pagemax] 
      categoryinf_show = [] 
      pid = [] 
      pname = []
      stock_num = []
      sell_price = []
      sell_price2 = []
      for categoryinf_list in db_stock_categoryinfs: 
        zero = categoryinf_list[0]
        pid.append(zero)
        one = categoryinf_list[1]
        pname.append(one)
        two= categoryinf_list[2]
        stock_num .append(two)
        three = categoryinf_list[3]
        sell_price.append(three)
        four = categoryinf_list[4]
        sell_price2.append(four)
      for i in range(len(pid)):
        categoryinf_show.append({
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "【類別】庫存查詢商品",
                "weight": "bold",
                "size": "xl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "商品ID：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f" {pid[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "商品名稱：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text":f" {pname[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "庫存數量：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text":f" {stock_num[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "售出單價：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f" {sell_price[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "售出單價２：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f" {sell_price2[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                }
                ]
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [],
            "flex": 0
        }
        })
      if len(categoryinf_show) >= 9:
        categoryinf_show.append({
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
                      "text": "【類別庫存商品列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                      }
                    }
                ]
            }
        })
      else: 
        categoryinf_show.append({
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
                      "label":"'點我回到'【庫存查詢】",
                      "text": "【庫存查詢】類別",
                    }
                  }
              ]
          }
      })
    return categoryinf_show 
#-------------------進貨狀態-抓取進貨中商品------------------------
def puring_pro_list(): 
    pro_puring_show = []
    pro_puring_list = db_puring_pro()
    if pro_puring_list == '找不到符合條件的資料。':
      pro_puring_show= TextSendMessage(text = pro_puring_list)
    else:
      pagemin = manager.list_page[manager.user_id+'廠商數量min']
      pagemax = manager.list_page[manager.user_id+'廠商數量max']
      db_puring_pros = pro_puring_list[pagemin:pagemax] 
      pro_puring_show = []
      pid = [] 
      pname = []
      pur_num = []
      pur_sta = []
      pur_time = []
      payment = []

      for pro_puring_list in db_puring_pros: 
        zero = pro_puring_list[0]
        pid.append(zero)
        one = pro_puring_list[1]
        pname.append(one)
        two = pro_puring_list[2]
        pur_num.append(two)
        three = pro_puring_list[3]
        pur_sta.append(three)
        four = pro_puring_list[4]
        pur_time.append(four)
        five = pro_puring_list[5]
        payment.append(five)
      for i in range(len(pid)):
        pro_puring_show.append({
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "【進貨中】查詢商品",
                "weight": "bold",
                "size": "xl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "商品ID：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f" {pid[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "商品名稱：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f" {pname[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "進貨數量：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text":  f" {pur_num[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "進貨狀態：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text":  f" {pur_sta[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "進貨時間：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text":  f" {pur_time[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "付款方式：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text":  f" {payment[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
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
                "action": {
                "type": "message",
                "label": "商品已到貨",
                "text": f"商品已到貨~{pid[i]}~{payment[i]}",
                },
                "style": "primary"
            }
            ],
            "flex": 0
        }
        })
      if len(pro_puring_show) >= 9:
        pro_puring_show.append({
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
                      "text": "【進貨中商品查詢列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                      }
                    }
                ]
            }
        })
      else: 
        pro_puring_show.append({
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
                      "label":"已經到底囉！ '點我回到'選擇查詢進貨狀態",
                      "text": "進貨商品狀態查詢",
                    }
                  }
              ]
          }
      })
    return pro_puring_show
#-------------------進貨狀態-抓取已到貨商品-------------------------
def pured_pro_list():
    pro_pured_show = []
    pro_pured_list = db_pured_pro()
    if pro_pured_list == '找不到符合條件的資料。':
      pro_pured_show= TextSendMessage(text = pro_pured_list)
    else:
      pagemin = manager.list_page[manager.user_id+'廠商數量min']
      pagemax = manager.list_page[manager.user_id+'廠商數量max']
      db_pured_pros = pro_pured_list[pagemin:pagemax] 
      pro_pured_show = []
      pid = [] 
      pname = []
      pur_num = []
      pur_sta = []
      pur_time = []
      

      for pro_pured_list in db_pured_pros: 
        zero = pro_pured_list[0]
        pid.append(zero)
        one = pro_pured_list[1]
        pname.append(one)
        two = pro_pured_list[2]
        pur_num.append(two)
        three = pro_pured_list[3]
        pur_sta.append(three)
        four = pro_pured_list[4]
        pur_time.append(four)
      for i in range(len(pid)):
        pro_pured_show.append({
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "【已到貨】查詢商品",
                "weight": "bold",
                "size": "xl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "商品ID：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f" {pid[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "商品名稱：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f" {pname[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "進貨數量：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text":  f" {pur_num[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "進貨狀態：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text":  f" {pur_sta[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "進貨時間：",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text":  f" {pur_time[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                      }
            ]
          }
        ]
      }
    ]
  },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [],
            "flex": 0
        }
        })
      if len(pro_pured_show) >= 9:
        pro_pured_show.append({
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
                      "text": "【已到貨商品查詢列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                      }
                    }
                ]
            }
        })
      else: 
        pro_pured_show.append({
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
                      "label":"已經到底囉！ '點我回到'選擇查詢進貨狀態",
                      "text": "進貨商品狀態查詢",
                    }
                  }
              ]
          }
      })
    return pro_pured_show
##############################################################################################
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


