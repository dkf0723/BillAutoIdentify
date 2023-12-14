from linebot.models import FlexSendMessage,TextSendMessage,ButtonComponent,MessageAction, QuickReply,QuickReplyButton
from linebot.models.flex_message import BubbleContainer, BoxComponent, TextComponent
import info
from datetime import datetime, timedelta
from database import(db_quick_purchase_manufacturers,db_quickmanu_pro,db_stock_manufacturers_name,
                     db_stock_manuinf,db_stock_categoryinf,db_puring_pro,db_pured_pro,db_quick_catepro,nopur_inf,product_ing)
#---------------------庫存管理一開始的畫面-------
def Inventory_management():
    Inventory_management = []
    info1 = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "fit",
                "url": "https://i.imgur.com/vHe8Ee2.jpg"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "新增進貨 / 二次進貨",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
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
                            "text": "※新增現預購商品",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "※商品二次進貨",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
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
                "spacing": "none",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                    "type": "message",
                    "text": "新增及二次進貨商品",
                    "label": "新增進貨 / 二次進貨"
                    },
                    "height": "sm",
                    "color": "#9E93D9"
                }
                ],
                "flex": 0,
                "margin": "none"
            }
            }
    Inventory_management.append(info1)
    info2 ={
            "type": "bubble",
            "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "url": "https://i.imgur.com/3DjZhrd.jpg",
                "align": "center",
                "margin": "none",
                "aspectMode": "cover",
                "offsetBottom": "none",
                "offsetStart": "none",
                "offsetTop": "xxl"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "查詢商品庫存 ",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
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
                            "text": "※庫存警示",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "※所有商品庫存",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
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
                "spacing": "none",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                    "type": "message",
                    "text": "查詢商品庫存 ",
                    "label": "查詢商品庫存 "
                    },
                    "height": "sm",
                    "color": "#9E93D9"
                }
                ],
                "flex": 0,
                "margin": "none"
            }
            }
    Inventory_management.append(info2)
    info3 ={
            "type": "bubble",
            "hero": {
                "type": "image",
                "aspectRatio": "20:13",
                "url": "https://i.imgur.com/bRj2IM8.jpg",
                "align": "center",
                "margin": "none",
                "animated": True,
                "aspectMode": "cover",
                "size": "full",
                "offsetTop": "xxl"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "查詢商品狀態 ",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
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
                            "text": "※商品進貨中列表(點貨用)",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "※商品已到貨列表",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
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
                "spacing": "none",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                    "type": "message",
                    "text": "進貨商品狀態查詢 ",
                    "label": "查詢商品狀態 "
                    },
                    "height": "sm",
                    "color": "#9E93D9"
                }
                ],
                "flex": 0,
                "margin": "none"
            }
            }
    Inventory_management.append(info3)
    screen =FlexSendMessage(
                            alt_text='庫存管理服務選擇',
                            contents={
                                "type": "carousel",
                                "contents": Inventory_management  
                                } 
                            )
    return screen
#--------------------未有進貨資訊的預購商品列表--
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
      pagemin = info.list_page[info.user_id+'廠商數量min']
      pagemax = info.list_page[info.user_id+'廠商數量max']
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
                "text": "【二次進貨】依廠商",
                "weight": "bold",
                "align": "center",
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
                        "text": "※廠商編號：",
                        "size": "md",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f" {mid[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
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
                        "text": "※廠商名稱：",
                        "size": "md",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text":f" {mname[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
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
                "text": f"二次進貨-選擇廠商{mid[i]}"
                },
                "color": "#cfa091"
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
                      "label":"到底囉！點我回'選擇商品查詢方式'",
                      "text": "【進貨商品】二次進貨",
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
      pagemin = info.list_page[info.user_id+'廠商數量min']
      pagemax = info.list_page[info.user_id+'廠商數量max']
      db_quickmanu_pros = quickmanupro_list[pagemin:pagemax]
      quickmanupro_show = []
      pid = []  
      pname = []  
      purtime = []
      statepro = []
      unit = []
      payment = []
      for quickmanupro_list in db_quickmanu_pros:
        zero = quickmanupro_list[0]
        pid.append(zero)
        one = quickmanupro_list[1]
        pname.append(one)
        two = quickmanupro_list[2]
        purtime.append(two)
        three= quickmanupro_list[3]
        statepro.append(three)
        four= quickmanupro_list[4]
        unit.append(four)
        five= quickmanupro_list[5]
        payment.append(five)
      for i in range (len(pid)):
        quickmanupro_show.append({
        "type": "bubble",
        "body":{
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "【廠商】二次進貨商品",
                "weight": "bold",
                "align": "center",
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
                        "text": "※商品ID：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f"{pid[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "weight": "bold",
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
                        "text": "※商品名稱：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f"{pname[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "weight": "bold",
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
                        "text": "※上次進貨時間：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f"{purtime[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "weight": "bold",
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
                        "text": "※現預購商品：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f"{statepro[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "weight": "bold",
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
                "text": f"二次進貨-{statepro[i]}~{pid[i]}!{unit[i]}@{payment[i]}"
                },
                "color": "#C9B0A8"
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
                      "text": "【二次進貨商品列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
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
                    "label":"到底囉！點我回到'所有廠商列表'",
                    "text": "【二次進貨】廠商",
                    }
                }
            ]
        }
    })
    return quickmanupro_show   
#------------------快速進貨->依分類查詢所有商品的商品ID及商品名稱-------------------
def quick_catepro_list(selectedr_category):
    catepro_quick_show = []
    catepro_quick_list = db_quick_catepro(selectedr_category)
    if catepro_quick_list == '找不到符合條件的資料。':
      catepro_quick_show = TextSendMessage(text = catepro_quick_list)
    else:
      pagemin = info.list_page[info.user_id+'廠商數量min']
      pagemax = info.list_page[info.user_id+'廠商數量max']
      db_quick_catepros = catepro_quick_list[pagemin:pagemax] 
      catepro_quick_show = [] 
      pid = [] 
      pname = []
      pur_time = []
      stat_pro = []
      unit = []
      payment = []
      
      for catepro_quick_list in db_quick_catepros: 
        zero = catepro_quick_list[0]
        pid.append(zero)
        one = catepro_quick_list[1]
        pname.append(one)
        two= catepro_quick_list[2]
        pur_time .append(two)
        three = catepro_quick_list[3]
        stat_pro.append(three)
        four= catepro_quick_list[4]
        unit.append(four)
        five= catepro_quick_list[5]
        payment.append(five)
        
      for i in range(len(pid)):
        catepro_quick_show.append({
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "【類別】二次進貨商品",
                "weight": "bold",
                "align": "center",
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
                        "text": "※商品ID：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f"{pid[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "weight": "bold",
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
                        "text": "※商品名稱：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f"{pname[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "weight": "bold",
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
                        "text": "※上次進貨時間：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f"{pur_time[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "weight": "bold",
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
                        "text": "※現預購商品：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f"{stat_pro[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "weight": "bold",
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
                "text": f"二次進貨-{stat_pro[i]}~{pid[i]}!{unit[i]}@{payment[i]}"
                },
                 "color":"#5f5f5f"
            }
            ],
            "flex": 0
        }
        })
      if len(catepro_quick_show) >= 9:
        catepro_quick_show.append({
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
                      "text": "【類別二次進貨商品列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                      }
                    }
                ]
            }
        })
      else: 
        catepro_quick_show.append({
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
                      "label":"到底囉!點我回到'二次進貨類別選項'",
                      "text": "【二次進貨】類別",
                    }
                  }
              ]
          }
      })
    return catepro_quick_show
#-----------------------庫存-查詢所有廠商編號及廠商名------------------------
def stock_manufacturers_name_list(): 
    stock_manufacturers_show = []
    stock_manufacturers_list = db_stock_manufacturers_name()
    if stock_manufacturers_list == '找不到符合條件的資料。':
      stock_manufacturers_show= TextSendMessage(text = stock_manufacturers_list)
    else:
      pagemin = info.list_page[info.user_id+'廠商數量min']
      pagemax = info.list_page[info.user_id+'廠商數量max']
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
                "align": "center",
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
                        "text": "※廠商編號：",
                        "size": "md",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f" {mid[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
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
                         "text": "※廠商名稱：",
                        "size": "md",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text":f" {mname[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
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
                "color": "#cfa091"
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
                      "label":"到底囉！點我回到'選擇商品查詢方式'",
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
      pagemin = info.list_page[info.user_id+'廠商數量min']
      pagemax = info.list_page[info.user_id+'廠商數量max']
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
                "align": "center",
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
                        "text": "※商品ID：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text":f" {pid[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
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
                        "text": "※商品名稱：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f" {pname[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
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
                        "text": "※庫存數量：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f" {stock_num[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
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
                        "text": "※售出單價：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f" {sell_price[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
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
                        "text": "※售出單價２：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f" {sell_price2[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
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
                      "label":"到底囉!點我回'庫存查詢'",
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
      pagemin = info.list_page[info.user_id+'廠商數量min']
      pagemax = info.list_page[info.user_id+'廠商數量max']
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
                "align": "center",
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
                        "text": "※商品ID：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text":f" {pid[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
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
                        "text": "※商品名稱：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f" {pname[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
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
                        "text": "※庫存數量：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f" {stock_num[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
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
                        "text": "※售出單價：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f" {sell_price[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
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
                        "text": "※售出單價２：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f" {sell_price2[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
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
                      "label":"到底囉!點我回'庫存查詢'",
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
      pagemin = info.list_page[info.user_id+'廠商數量min']
      pagemax = info.list_page[info.user_id+'廠商數量max']
      db_puring_pros = pro_puring_list[pagemin:pagemax] 
      pro_puring_show = []
      pid = [] 
      pname = []
      pur_num = []
      pur_sta = []
      pur_time = []
      payment = []
      stat_pro = []

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
        six = pro_puring_list[6]
        stat_pro.append(six)
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
                "size": "xl",
                "align": "center"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "xs",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "※商品ID：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold",
                        "text": f" {pid[i]}"
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
                        "text": "※商品名稱：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold",
                        "text":  f" {pname[i]}"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "※進貨數量：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f" {pur_num[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "※進貨狀態：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f" {pur_sta[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "※進貨時間：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f" {pur_time[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "※付款方式：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text":  f" {payment[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
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
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "商品已到貨",
                "text":f"商品已到貨~{pid[i]}~{payment[i]}~{stat_pro[i]}"
                },
                "style": "primary",
                "color": "#7b97cd"
            }
            ]
        }
        })
        # "type": "bubble",
        # "body": {
        #     "type": "box",
        #     "layout": "vertical",
        #     "contents": [
        #     {
        #         "type": "text",
        #         "text": "【進貨中】查詢商品",
        #         "weight": "bold",
        #         "size": "xl"
        #     },
        #     {
        #         "type": "box",
        #         "layout": "vertical",
        #         "margin": "lg",
        #         "spacing": "sm",
        #         "contents": [
        #         {
        #             "type": "box",
        #             "layout": "vertical",
        #             "spacing": "sm",
        #             "contents": [
        #             {
        #                 "type": "text",
        #                 "text": "商品ID：",
        #                 "size": "sm",
        #                 "flex": 1
        #             },
        #             {
        #                 "type": "text",
        #                 "text": f" {pid[i]}",
        #                 "wrap": True,
        #                 "color": "#666666",
        #                 "size": "sm",
        #                 "flex": 5
        #             }
        #             ]
        #         },
        #         {
        #             "type": "box",
        #             "layout": "vertical",
        #             "spacing": "sm",
        #             "contents": [
        #             {
        #                 "type": "text",
        #                 "text": "商品名稱：",
        #                 "size": "sm",
        #                 "flex": 1
        #             },
        #             {
        #                 "type": "text",
        #                 "text": f" {pname[i]}",
        #                 "wrap": True,
        #                 "color": "#666666",
        #                 "size": "sm",
        #                 "flex": 5
        #             }
        #             ]
        #         },
        #         {
        #             "type": "box",
        #             "layout": "vertical",
        #             "spacing": "sm",
        #             "contents": [
        #             {
        #                 "type": "text",
        #                 "text": "進貨數量：",
        #                 "size": "sm",
        #                 "flex": 1
        #             },
        #             {
        #                 "type": "text",
        #                 "text":  f" {pur_num[i]}",
        #                 "wrap": True,
        #                 "color": "#666666",
        #                 "size": "sm",
        #                 "flex": 5
        #             }
        #             ]
        #         },
        #         {
        #             "type": "box",
        #             "layout": "vertical",
        #             "spacing": "sm",
        #             "contents": [
        #             {
        #                 "type": "text",
        #                 "text": "進貨狀態：",
        #                 "size": "sm",
        #                 "flex": 1
        #             },
        #             {
        #                 "type": "text",
        #                 "text":  f" {pur_sta[i]}",
        #                 "wrap": True,
        #                 "color": "#666666",
        #                 "size": "sm",
        #                 "flex": 5
        #             }
        #             ]
        #         },
        #         {
        #             "type": "box",
        #             "layout": "vertical",
        #             "spacing": "sm",
        #             "contents": [
        #             {
        #                 "type": "text",
        #                 "text": "進貨時間：",
        #                 "size": "sm",
        #                 "flex": 1
        #             },
        #             {
        #                 "type": "text",
        #                 "text":  f" {pur_time[i]}",
        #                 "wrap": True,
        #                 "color": "#666666",
        #                 "size": "sm",
        #                 "flex": 5
        #             }
        #             ]
        #         },
        #         {
        #             "type": "box",
        #             "layout": "vertical",
        #             "spacing": "sm",
        #             "contents": [
        #             {
        #                 "type": "text",
        #                 "text": "付款方式：",
        #                 "size": "sm",
        #                 "flex": 1
        #             },
        #             {
        #                 "type": "text",
        #                 "text":  f" {payment[i]}",
        #                 "wrap": True,
        #                 "color": "#666666",
        #                 "size": "sm",
        #                 "flex": 5
        #             }
        #             ]
        #         }
        #         ]
        #     }
        #     ]
        # },
        # "footer": {
        #     "type": "box",
        #     "layout": "vertical",
        #     "spacing": "sm",
        #     "contents": [
        #     {
        #         "type": "button",
        #         "action": {
        #         "type": "message",
        #         "label": "商品已到貨",
        #         "text": f"商品已到貨~{pid[i]}~{payment[i]}~{stat_pro[i]}",
        #         },
        #         "style": "primary"
        #     }
        #     ],
        #     "flex": 0
        # }
        # })
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
                      "label":"到底囉！點我回'選擇查詢進貨狀態'",
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
      pagemin = info.list_page[info.user_id+'廠商數量min']
      pagemax = info.list_page[info.user_id+'廠商數量max']
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
                "size": "xl",
                "align": "center",
                "gravity": "center"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "xs",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "※商品ID：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold",
                        "text":  f" {pid[i]}",
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
                        "text": "※商品名稱：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "wrap":True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold",
                        "text":  f" {pname[i]}"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "※進貨數量：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f" {pur_num[i]}",
                        "wrap":True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "※進貨狀態：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text":f" {pur_sta[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "※進貨時間：",
                        "size": "sm",
                        "flex": 1,
                        "color": "#3b5a5f",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f" {pur_time[i]}",
                        "wrap": True,
                        "color": "#666666",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
                    }
                    ]
                }
                ]
            }
            ]
        }
        })
#         "type": "bubble",
#         "body": {
#             "type": "box",
#             "layout": "vertical",
#             "contents": [
#             {
#                 "type": "text",
#                 "text": "【已到貨】查詢商品",
#                 "weight": "bold",
#                 "size": "xl"
#             },
#             {
#                 "type": "box",
#                 "layout": "vertical",
#                 "margin": "lg",
#                 "spacing": "sm",
#                 "contents": [
#                 {
#                     "type": "box",
#                     "layout": "vertical",
#                     "spacing": "sm",
#                     "contents": [
#                     {
#                         "type": "text",
#                         "text": "商品ID：",
#                         "size": "sm",
#                         "flex": 1
#                     },
#                     {
#                         "type": "text",
#                         "text": f" {pid[i]}",
#                         "wrap": True,
#                         "color": "#666666",
#                         "size": "sm",
#                         "flex": 5
#                     }
#                     ]
#                 },
#                 {
#                     "type": "box",
#                     "layout": "vertical",
#                     "spacing": "sm",
#                     "contents": [
#                     {
#                         "type": "text",
#                         "text": "商品名稱：",
#                         "size": "sm",
#                         "flex": 1
#                     },
#                     {
#                         "type": "text",
#                         "text": f" {pname[i]}",
#                         "wrap": True,
#                         "color": "#666666",
#                         "size": "sm",
#                         "flex": 5
#                     }
#                     ]
#                 },
#                 {
#                     "type": "box",
#                     "layout": "vertical",
#                     "spacing": "sm",
#                     "contents": [
#                     {
#                         "type": "text",
#                         "text": "進貨數量：",
#                         "size": "sm",
#                         "flex": 1
#                     },
#                     {
#                         "type": "text",
#                         "text":  f" {pur_num[i]}",
#                         "wrap": True,
#                         "color": "#666666",
#                         "size": "sm",
#                         "flex": 5
#                     }
#                     ]
#                 },
#                 {
#                     "type": "box",
#                     "layout": "vertical",
#                     "spacing": "sm",
#                     "contents": [
#                     {
#                         "type": "text",
#                         "text": "進貨狀態：",
#                         "size": "sm",
#                         "flex": 1
#                     },
#                     {
#                         "type": "text",
#                         "text":  f" {pur_sta[i]}",
#                         "wrap": True,
#                         "color": "#666666",
#                         "size": "sm",
#                         "flex": 5
#                     }
#                     ]
#                 },
#                 {
#                     "type": "box",
#                     "layout": "vertical",
#                     "spacing": "sm",
#                     "contents": [
#                     {
#                         "type": "text",
#                         "text": "進貨時間：",
#                         "size": "sm",
#                         "flex": 1
#                     },
#                     {
#                         "type": "text",
#                         "text":  f" {pur_time[i]}",
#                         "wrap": True,
#                         "color": "#666666",
#                         "size": "sm",
#                         "flex": 5
#                       }
#             ]
#           }
#         ]
#       }
#     ]
#   },
#         "footer": {
#             "type": "box",
#             "layout": "vertical",
#             "spacing": "sm",
#             "contents": [],
#             "flex": 0
#         }
#         })
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
                      "label":"到底囉！'點我回'選擇查詢進貨狀態",
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
                "aspectRatio": "20:13",
                "url": "https://i.imgur.com/NLcNzHJ.jpg",
                "align": "center",
                "margin": "none",
                "animated": True,
                "aspectMode": "fit",
                "size": "full",
                "offsetTop": "lg"
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
                            "text": "※最近100筆預購訂單",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "※預購訂單成立由近到遠排序",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "※可顯示預購訂單詳細內容",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
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
                "spacing": "md",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                    "type": "message",
                    "text": "【預購名單】列表  ",
                    "label": "預購名單列表"
                    },
                    "height": "sm",
                    "color": "#E76700"
                }
                ],
                "flex": 0,
                "margin": "sm"
            }
            }
            
    Order_preorder_screen.append(Order)
    preorder = {
  "type": "bubble",
  "hero": {
            "type": "image",
            "aspectRatio": "20:13",
            "url": "https://i.imgur.com/sjgqpvS.jpg",
            "align": "center",
            "margin": "none",
            "animated": True,
            "aspectMode": "fit",
            "size": "full",
            "offsetTop": "lg"
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
                        "text": "※最近100筆預購訂單",
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "※未取訂單成立由近到遠排序",
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "※可顯示預購訂單詳細內容",
                        "color": "#3b5a5f",
                        "size": "md",
                        "flex": 5,
                        "weight": "bold"
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
            "spacing": "md",
            "contents": [
            {
                "type": "button",
                "style": "primary",
                "action": {
                "type": "message",
                "text": "【未取名單】列表  ",
                "label": "未取名單列表"
                },
                "height": "sm",
                "color": "#E76700"
            }
            ],
            "flex": 0,
            "margin": "sm"
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
#暫時無用
def preorderli_list():
    db_preorder = nopur_inf()
    #P.商品ID,P.商品名稱,P.商品單位,廠商名,付款方式
    if db_preorder == "找不到符合條件的資料。":
        preorder_show = TextSendMessage(text=db_preorder)
    else:
        preorder_show = []
        preorder_handlelist = []
    
        while len(db_preorder) > 0:
            ooo_elements = db_preorder[:10]  # 取得10個元素
            preorder_handlelist.append(ooo_elements)  # 將10個元素作為一個子陣列加入結果陣列
            db_preorder = db_preorder[10:]

        for totalooolist in preorder_handlelist:
            buttons = []  # #模塊中10筆資料
            for i in range(len(totalooolist)):
                '''totalooolist[i][0]#pid
                totalooolist[i][1]#pname
                totalooolist[i][2]#unit
                totalooolist[i][3]#manuname
                totalooolist[i][4]#payment'''
                button = {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": f"{totalooolist[i][1]}",
                        "text": f"預購商品ID:{totalooolist[i][0]}~{totalooolist[i][2]}!{totalooolist[i][3]}/{totalooolist[i][4]}"
                    }
                    }
                buttons.append(button)
            preorder_show.append({
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
                                "text": "預購商品查詢",
                                "weight": "bold",
                                "size": "xl",
                                "align": "center",
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
        preorder_show = FlexSendMessage(
                alt_text="預購商品查詢",
                contents={
                "type": "carousel",
                "contents": preorder_show      
                } 
            )
    return preorder_show

#新增進貨(現/預)
def noworderli_list(tp):
    if tp == '現':
        dbdb_preorder = product_ing()
    elif tp == '預':
       dbdb_preorder = nopur_inf()
    #P.商品ID,P.商品名稱,P.商品單位,廠商名,付款方式
    if dbdb_preorder == "找不到符合條件的資料。":
        preorderr_show = TextSendMessage(text=dbdb_preorder)
    else:
        preorderr_show = []
        preorderr_handlelist = []
    
        while len(dbdb_preorder) > 0:
            oooo_elements = dbdb_preorder[:10]  # 取得10個元素
            preorderr_handlelist.append(oooo_elements)  # 將10個元素作為一個子陣列加入結果陣列
            dbdb_preorder = dbdb_preorder[10:]
            
        for totaloooolist in preorderr_handlelist:
            buttons = []  # #模塊中10筆資料
            for i in range(len(totaloooolist)):
                '''totalooolist[i][0]#pid
                totalooolist[i][1]#pname
                totalooolist[i][2]#unit
                totalooolist[i][3]#manuname
                totalooolist[i][4]#payment'''
                if len(totaloooolist[i][1])>40:
                   lotot = totaloooolist[i][1][:40]
                else:
                   lotot = totaloooolist[i][1]
                button = {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": f"{lotot}",
                        "text": f"{tp}購商品ID:{totaloooolist[i][0]}~{totaloooolist[i][2]}!{totaloooolist[i][3]}/{totaloooolist[i][4]}"
                    }
                    }
                buttons.append(button)
            preorderr_show.append({
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
                                "text": f"{tp}購商品查詢",
                                "weight": "bold",
                                "size": "xl",
                                "align": "center",
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
        preorderr_show = FlexSendMessage(
                alt_text=f"{tp}購商品查詢",
                contents={
                "type": "carousel",
                "contents": preorderr_show      
                } 
            )
    return preorderr_show
def report_list_selectionscreen(): # 報表管理
    report_list_screen = []
    cost = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "fit",
                "url": "https://i.imgur.com/5di1yQ6.jpg"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "成本統計",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
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
                            "text": "※月統計",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
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
                            "text": "※年統計",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
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
                "spacing": "xs",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                    "type": "message",
                    "text": "【成本統計】列表",
                    "label": "成本統計列表"
                    },
                    "height": "sm",
                    "color": "#5bb09b"
                }
                ],
                "flex": 0,
                "margin": "xs"
            }
            }
    report_list_screen.append(cost)
    profit = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "fit",
                "url": "https://i.imgur.com/TjtIVXm.jpg"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "利潤統計",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
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
                            "text": "※月統計",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
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
                            "text": "※年統計",
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
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
                "spacing": "xs",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                    "type": "message",
                    "text": "【利潤統計】列表",
                    "label": "利潤統計列表"
                    },
                    "height": "sm",
                    "color": "#5bb09b"
                }
                ],
                "flex": 0,
                "margin": "xs"
            }
            }
    report_list_screen.append(profit)
    popular_products = {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "cover",
                        "url": "https://i.imgur.com/mGn0B5q.jpg"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "熱門商品統計",
                            "weight": "bold",
                            "size": "xl",
                            "align": "center"
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
                                    "text": "※月統計",
                                    "color": "#3b5a5f",
                                    "size": "md",
                                    "flex": 5,
                                    "weight": "bold"
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
                        "spacing": "xs",
                        "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {
                            "type": "message",
                            "text": "【熱門商品統計】列表",
                            "label": "熱門商品統計列表"
                            },
                            "height": "sm",
                            "color": "#5bb09b"
                        }
                        ],
                        "flex": 0,
                        "margin": "xs"
                    }
                    }
    report_list_screen.append(popular_products)
    screen =FlexSendMessage(
                            alt_text='報表管理',
                            contents={
                                "type": "carousel",
                                "contents": report_list_screen   
                                } 
                            )
    return screen
def Report_statistics_selectionscreen(queryObject): # 報表管理各項統計
    Report_statistics_screen = []
    if queryObject == '熱門商品':
        popular_products_monthly = {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "fit",
                        "url": "https://i.imgur.com/vHe8Ee2.jpg"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "熱門商品月統計",
                            "weight": "bold",
                            "size": "xl",
                            "align": "center"
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
                                    "text": "※各廠商熱賣商品",
                                    "color": "#3b5a5f",
                                    "size": "md",
                                    "flex": 5,
                                    "weight": "bold",
                                    "wrap": True
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
                                    "text": "※可自行選擇月份,十年範圍",
                                    "color": "#3b5a5f",
                                    "size": "md",
                                    "flex": 5,
                                    "weight": "bold",
                                    "wrap": True
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
                        "spacing": "xs",
                        "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {
                            "type": "message",
                            "text": "【熱門商品月統計】列表",
                            "label": "熱門商品月統計"
                            },
                            "height": "sm",
                            "color": "#1a9879"
                        }
                        ],
                        "flex": 0,
                        "margin": "xs"
                    }
                    }
        Report_statistics_screen.append(popular_products_monthly)
    else:
        monthly = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/xkAEoti.jpg",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "fit"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": f"{queryObject}月統計",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"※該月{queryObject}統計",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "md",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text":"※可自行選擇月份,十年範圍",
                    "wrap": True,
                    "color": "#3b5a5f",
                    "size": "md",
                    "flex": 5,
                    "margin": "sm",
                    "weight": "bold"
                },
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
                    "label": f"{queryObject}月統計",
                    "text": f"【{queryObject}月統計】"
                    },
                    "color": "#1a9879",
                    "style": "primary"
                }
                ],
                "flex": 0
            }
            }
        Report_statistics_screen.append(monthly)
        yearly = {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://i.imgur.com/AkabFg0.jpg",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "fit"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": f"{queryObject}年統計",
                            "weight": "bold",
                            "size": "xl",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": f"※該年{queryObject}統計",
                            "wrap": True,
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "margin": "md",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text":"※可自行選擇月份,十年範圍",
                            "wrap": True,
                            "color": "#3b5a5f",
                            "size": "md",
                            "flex": 5,
                            "margin": "sm",
                            "weight": "bold"
                        },
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
                            "label": f"{queryObject}年統計",
                            "text": f"【{queryObject}年統計】"
                            },
                            "color": "#1a9879",
                            "style": "primary"
                        }
                        ],
                        "flex": 0
                    }
                    }
        Report_statistics_screen.append(yearly)    
    screen =FlexSendMessage(
                            alt_text='成本/利潤報表統計',
                            contents={
                                "type": "carousel",
                                "contents": Report_statistics_screen   
                                } 
                            )
    return screen
def info_time_choise(now_time): 

    current_datetime = datetime.now()# 取得當前的日期和時間
    modified_datetime = current_datetime + timedelta(hours=8)#時區轉換+8
    order_date = modified_datetime.strftime('%Y')#格式化日期，清除-
    now_time = int(order_date)

    report_year = []
    year_list = [] #近10年的年份
    for i in range(10):
        year_list.append(now_time-i)
    for i in range(len(year_list)):
      report_year.append({
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": f"{year_list[i]}", #前面須加關鍵字才能呼叫選擇月份
              "text": f"【選擇月份】{year_list[i]}"
            }
          }
        ]
      }
    })
    show = FlexSendMessage(
            alt_text='【未取訂單】列表',
            contents= {
                      "type": "carousel",
                      "contents": report_year
                      }
            )

    return show
#-----------------選擇報表年分------------------------------------------------------------------------------
def manager_year_choise(event, line_bot_api, report_type):
    current_datetime = datetime.now()# 取得當前的日期和時間
    modified_datetime = current_datetime + timedelta(hours=8)#時區轉換+8
    order_date = modified_datetime.strftime('%Y')#格式化日期，清除-
    now_time = int(order_date)
    if '年' in report_type: 
        message = TextSendMessage(text='請點選年份',
                quick_reply=QuickReply(items=[
                    QuickReplyButton(action=MessageAction(label=f"{now_time}", text=f"【顯示報表】{now_time}-99{report_type}")),
                    QuickReplyButton(action=MessageAction(label=f"{now_time-1}", text=f"【顯示報表】{now_time-1}-99{report_type}")),
                    QuickReplyButton(action=MessageAction(label=f"{now_time-2}", text=f"【顯示報表】{now_time-2}-99{report_type}")),
                    QuickReplyButton(action=MessageAction(label=f"{now_time-3}", text=f"【顯示報表】{now_time-3}-99{report_type}")),
                    QuickReplyButton(action=MessageAction(label=f"{now_time-4}", text=f"【顯示報表】{now_time-4}-99{report_type}")),
                    QuickReplyButton(action=MessageAction(label=f"{now_time-5}", text=f"【顯示報表】{now_time-5}-99{report_type}")),
                    QuickReplyButton(action=MessageAction(label=f"{now_time-6}", text=f"【顯示報表】{now_time-6}-99{report_type}")),
                    QuickReplyButton(action=MessageAction(label=f"{now_time-7}", text=f"【顯示報表】{now_time-7}-99{report_type}")),
                    QuickReplyButton(action=MessageAction(label=f"{now_time-8}", text=f"【顯示報表】{now_time-8}-99{report_type}")),
                    QuickReplyButton(action=MessageAction(label=f"{now_time-9}", text=f"【顯示報表】{now_time-9}-99{report_type}"))
                ]))
    else:
        message = TextSendMessage(text='請點選年份',
        quick_reply=QuickReply(items=[
            QuickReplyButton(action=MessageAction(label=f"{now_time}", text=f"【選擇月份】{now_time}{report_type}")),
            QuickReplyButton(action=MessageAction(label=f"{now_time-1}", text=f"【選擇月份】{now_time-1}{report_type}")),
            QuickReplyButton(action=MessageAction(label=f"{now_time-2}", text=f"【選擇月份】{now_time-2}{report_type}")),
            QuickReplyButton(action=MessageAction(label=f"{now_time-3}", text=f"【選擇月份】{now_time-3}{report_type}")),
            QuickReplyButton(action=MessageAction(label=f"{now_time-4}", text=f"【選擇月份】{now_time-4}{report_type}")),
            QuickReplyButton(action=MessageAction(label=f"{now_time-5}", text=f"【選擇月份】{now_time-5}{report_type}")),
            QuickReplyButton(action=MessageAction(label=f"{now_time-6}", text=f"【選擇月份】{now_time-6}{report_type}")),
            QuickReplyButton(action=MessageAction(label=f"{now_time-7}", text=f"【選擇月份】{now_time-7}{report_type}")),
            QuickReplyButton(action=MessageAction(label=f"{now_time-8}", text=f"【選擇月份】{now_time-8}{report_type}")),
            QuickReplyButton(action=MessageAction(label=f"{now_time-9}", text=f"【選擇月份】{now_time-9}{report_type}"))
        ]))
    line_bot_api.reply_message(event.reply_token, message) 
#-----------------選擇報表月份------------------------------------------------------------------------------
def manager_month_choise(event, line_bot_api,year_query,report_type): 
    message = TextSendMessage(text='請點選月份',
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label=f"一月", text=f"【顯示報表】{year_query}-01{report_type}")),
                QuickReplyButton(action=MessageAction(label="二月", text=f"【顯示報表】{year_query}-02{report_type}")),
                QuickReplyButton(action=MessageAction(label="三月", text=f"【顯示報表】{year_query}-03{report_type}")),
                QuickReplyButton(action=MessageAction(label="四月", text=f"【顯示報表】{year_query}-04{report_type}")),
                QuickReplyButton(action=MessageAction(label="五月", text=f"【顯示報表】{year_query}-05{report_type}")),
                QuickReplyButton(action=MessageAction(label="六月", text=f"【顯示報表】{year_query}-06{report_type}")),
                QuickReplyButton(action=MessageAction(label="七月", text=f"【顯示報表】{year_query}-07{report_type}")),
                QuickReplyButton(action=MessageAction(label="八月", text=f"【顯示報表】{year_query}-08{report_type}")),
                QuickReplyButton(action=MessageAction(label="九月", text=f"【顯示報表】{year_query}-09{report_type}")),
                QuickReplyButton(action=MessageAction(label="十月", text=f"【顯示報表】{year_query}-10{report_type}")),
                QuickReplyButton(action=MessageAction(label="十一月", text=f"【顯示報表】{year_query}-11{report_type}")),
                QuickReplyButton(action=MessageAction(label="十二月", text=f"【顯示報表】{year_query}-12{report_type}"))
            ]))
    line_bot_api.reply_message(event.reply_token, message)
