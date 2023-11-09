from linebot.models import TextSendMessage,FlexSendMessage
import manager
from database import Now_Product,Per_Product, db_manufacturers,db_products_manufacturers,db_categoryate
#-------------所有廠商列出---------------
def manager_manufacturers_list():
    manufacturers_show = []
    manufacturers_list = db_manufacturers()
    if manufacturers_list == '找不到符合條件的資料。':
      manufacturers_show = TextSendMessage(text = manufacturers_list)#這邊有點不瞭解 但程式正常就沒差
    else:
      pagemin = manager.list_page[manager.user_id+'廠商數量min']
      pagemax = manager.list_page[manager.user_id+'廠商數量max']#9
      db_manufacturerss = manufacturers_list[pagemin:pagemax] 
      manufacturers_show = [] 
      mid = [] #廠商的編號
      mname = []#廠商名稱
      for manufacturers_list in db_manufacturerss: 
        zero = manufacturers_list[0]
        mid.append(zero)
        one = manufacturers_list[1]
        mname.append(one)

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
          "text": "※廠商編號：",
          "size": "md",
          "flex": 1,
          "color": "#3b5a5f",
          "weight": "bold"},
          {
           "type": "text",
            "text": f" {mid[i]}",
            "wrap": True,
            "color": "#666666",
            "size": "md",
            "flex": 5,
            "weight": "bold"}
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
        "contents": [
        {
        "type": "button",
        "style": "primary",
        "color": "#cfa091",
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
                      "label":"已底囉！點我回到【查詢/修改/下架】",
                      "text": "【查詢/修改/下架】",
                    }
                  }
              ]
          }
      })
    return manufacturers_show 
#---------------此廠商所有商品列出-------------------------
def manager_products_manufacturers_list(manufacturer_id,choose): 
    products_manufacturers_show = []
    products_manufacturers_list = db_products_manufacturers(manufacturer_id,choose)
    if products_manufacturers_list == '找不到符合條件的資料。':
      products_manufacturers_show= TextSendMessage(text =products_manufacturers_list)
    else:
      if choose != 'stop':
        page = '廠商'
        test1 = '【依廠商】查詢'
        test2 = '【依廠商】查詢'
      else:
        page = 'stop'
        test1 = '【停售及截止商品 】'
        test2 = '【停售及截止商品列表 】'
      pagemin = manager.list_page[manager.user_id+page+'數量min']
      pagemax = manager.list_page[manager.user_id+page+'數量max']#9
      db_products_manufacturerss = products_manufacturers_list[pagemin:pagemax]
      products_manufacturers_show = []
      pid = []  # '商品ID'
      pname = []  # '商品名稱'
      pphoto = [] # '商品圖片'
      stock_num = []  # '庫存數量'
      pname_unit = []  #  '商品單位'
      purchase_price = [] #'進貨單價'
      sell_price = []  # '售出單價'
      status = [] # '現預購狀態'
      for products_manufacturers_list in db_products_manufacturerss:
        zero = products_manufacturers_list[0] # '商品ID'
        pid.append(zero)
        one = products_manufacturers_list[1]# '商品名稱'
        pname.append(one)
        if (products_manufacturers_list[2] is None) or (products_manufacturers_list[2][:4]!= 'http'):
          img = 'https://i.imgur.com/rGlTAt3.jpg'
        else:
          img = products_manufacturers_list[2] # '商品圖片'
        pphoto.append(img)
        three = products_manufacturers_list[3]# '庫存數量'
        stock_num.append(three)
        four = products_manufacturers_list[4] # '商品單位'
        pname_unit.append(four)
        five = products_manufacturers_list[5] #'進貨單價'
        purchase_price.append(five)
        six = products_manufacturers_list[6] # '售出單價'
        sell_price.append(six)
        seven = products_manufacturers_list[7]# '現預購狀態'
        status.append(seven)

      for i in range(len(pid)):
        button = [{
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "修改商品資訊",
                  "text":f"【修改商品資訊】{pid[i]}"
                },
                "style": "primary",
                "color": "#46A3FF",
                "margin": "none",
                "height": "md",
                "offsetBottom": "sm",
                "offsetEnd": "none",
                "offsetStart": "xs"
              }]
        if status[i] == '現購':
            button.append(
                {
                  "type": "button",
                  "style": "primary",
                  "color": "#FF7575",
                  "margin": "none",
                  "action": {
                    "type": "message",
                    "label": "停售",
                    "text": f"【停售】{pid[i]}"
                  },
                  "height": "md",
                  "offsetEnd": "none",
                  "offsetBottom": "sm",
                  "offsetStart": "none"
                }
              )
        elif status[i] == '現購停售':
          button = [
                    {
                "type": "text",
                "text": "此商品已停售",
                "color": "#AE0000",
                "weight": "bold",
                "align": "center",
                "size": "lg",
                "margin": "none"
              }
          ]
        elif status[i] == '預購截止':
          button = [
                   {
                "type": "text",
                "text": "此商品已預購截止",
                "color": "#AE0000",
                "weight": "bold",
                "align": "center",
                "size": "lg",
                "margin": "none"
              }
          ]
           
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
            "contents": button,
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
                        "text": "【此廠商商品列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
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
                      "label":f"已到底囉！點我回到{test1}",
                      "text": f"{test2}",
                      }
                  }
              ]
          }
      })
    return products_manufacturers_show
#----------------分類下所有商品列表------------------------------
def manager_categoryate_list(selected_category):
    categoryate_show = []
    categoryate_list = db_categoryate(selected_category)
    if categoryate_list == '找不到符合條件的資料。':
       categoryate_show = TextSendMessage(text =categoryate_list) 
    else:
      pagemin = manager.list_page[manager.user_id+'廠商數量min']
      pagemax = manager.list_page[manager.user_id+'廠商數量max']#9
      db_categoryates = categoryate_list[pagemin:pagemax]
      categoryate_show = []
      pid = []  # '商品ID'
      pname = []  # '商品名稱'
      pphoto = [] # '商品圖片'
      stock_num = []  # '庫存數量'
      pname_unit = []  #  '商品單位'
      purchase_price = [] #'進貨單價'
      sell_price = []  # '售出單價'
      status = [] # '現預購狀態'
      for categoryate_list in  db_categoryates :
          zero = categoryate_list[0]
          pid.append(zero)
          one = categoryate_list[1]# '商品名稱'
          pname.append(one)
          if (categoryate_list[2] is None) or (categoryate_list[2][:4]!= 'http'):
            img = 'https://i.imgur.com/rGlTAt3.jpg'
          else:
            img = categoryate_list[2] # '商品圖片'
          pphoto.append(img)
          three = categoryate_list[3]# '庫存數量'
          stock_num.append(three)
          four = categoryate_list[4] #  '商品單位'
          pname_unit.append(four)
          five = categoryate_list[5] #'進貨單價'
          purchase_price.append(five)
          six = categoryate_list[6] # '售出單價'
          sell_price.append(six)
          seven = categoryate_list[7]# '現預購狀態'
          status.append(seven)
      for i in range(len(pid)):
          button = [{
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "修改商品資訊",
                  "text":f"【修改商品資訊】{pid[i]}"
                },
                "style": "primary",
                "color": "#46A3FF",
                "margin": "none",
                "height": "md",
                "offsetBottom": "sm",
                "offsetEnd": "none",
                "offsetStart": "xs"
              }]
          if status[i] == '現購':
            button.append(
                {
                  "type": "button",
                  "style": "primary",
                  "color": "#FF7575",
                  "margin": "none",
                  "action": {
                    "type": "message",
                    "label": "停售",
                    "text": f"【停售】{pid[i]}"
                  },
                  "height": "md",
                  "offsetEnd": "none",
                  "offsetBottom": "sm",
                  "offsetStart": "none"
                }
              )
          elif status[i] == '現購停售':
            button = [
                      {
                  "type": "text",
                  "text": "此商品已停售",
                  "color": "#AE0000",
                  "align": "center",
                  "size": "md",
                  "weight": "bold"
                }
            ]
          categoryate_show.append({ 
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
            "contents": button,
            "spacing": "none",
            "margin": "none"
          }
        })
    if len(categoryate_show) >= 9:
      categoryate_show.append({
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
                      "text": "【商品列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                        }
                    }
                ]
            }
        })
    else: 
      categoryate_show.append({
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
                    "label":"已到底囉！點我回到【查詢/修改/下架】",
                    "text": "【查詢/修改/下架】查詢",
                    }
                }
            ]
        }
    })
    return categoryate_show
#---------該商品所有資訊(現購/依廠商或類別查詢)測試---------------------
def Now_Product_Modification_FM(id):
    result = Now_Product(id)
    if result and len(result) > 0:
      bubbles = []
      pname = result[0][0] 
      introduction = result[0][1] 
      sell_price = result[0][2] 
      sell_price2 = result[0][3]
      
      if (result[0][4] is None) or (result[0][4][:4]!= 'http') :
        picture = "https://i.imgur.com/rGlTAt3.jpg"
      else:
        picture = result[0][4]
      
        # 建立 bubble1
      bubble1 = {
         "type": "bubble",
      "hero": {
        "type": "image",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "url": picture
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "現購商品所有資訊",
            "wrap": True,
            "weight": "bold",
            "size": "lg",
            "align": "center"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "1.商品名稱： ",
                "size": "md",
                "margin": "none",
                "weight": "bold",
                "color": "#A2B59F",
                "flex": 1
              },
              {
                "type": "text",
                "text": f" {pname}",
                "wrap": True,
                "flex": 2
              }
            ],
            "margin": "xxl",
            "spacing": "none",
            "position": "relative"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "2.商品簡介: ",
                "weight": "bold",
                "margin": "none",
                "size": "md",
                "color": "#A2B59F",
                "flex": 1
              },
              {
                "type": "text",
                "text": f" {introduction}",
                "flex": 2,
                "wrap": True
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "3.商品單價： ",
                "weight": "bold",
                "size": "md",
                "margin": "none",
                "color": "#A2B59F",
                "flex": 1
              },
              {
                "type": "text",
                "text": f" {sell_price}",
                "flex": 2,
                "wrap": True
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "4.商品單價2： ",
                "weight": "bold",
                "size": "md",
                "margin": "none",
                "color": "#A2B59F",
                "flex": 1
              },
              {
                "type": "text",
                "text": f" {sell_price2}",
                "flex": 2,
                "wrap": True
              }
            ]
          }
        ],
        "margin": "xs"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "separator"
          },
          {
            "type": "button",
            "style": "secondary",
            "action": {
              "type": "message",
             "label": "退出修改動作",
              "text": "退出修改"
            },
            "color": "#EAD880",
            "margin": "xl"
          }
        ]
      }
    }
        # 建立 bubble2
      bubble2 = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "xxl",
            "contents": [
                {
                  "type": "text",
                  "text": "修改現購商品所有資訊",
                  "align": "center",
                  "weight": "bold",
                  "margin": "none",
                  "size": "xl",
                },
                {
                  "type": "separator",
                  "margin": "md",
                  "color": "#A9A9A9"
                },
                {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [],
                  "spacing": "none",
                  "margin": "none"
                },
                  {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "1.修改_商品名稱",
                    "text": "【修改商品資訊】商品名稱"
                  },
                  "color": "#B1D3C5",
                  "style": "secondary",
                  "margin": "xxl"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "2.修改_商品簡介",
                    "text": "【修改商品資訊】商品簡介"
                  },
                  "color": "#B1D3C5",
                  "style": "secondary"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "3.修改_商品售出單價",
                    "text": "【修改商品資訊】商品售出單價"
                  },
                  "color": "#B1D3C5",
                  "style": "secondary"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "4.修改_商品售出單價2",
                    "text": "【修改商品資訊】商品售出單價2"
                  },
                  "color": "#B1D3C5",
                  "style": "secondary"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "5.更換商品圖片",
                    "text": "【修改商品資訊】更換商品圖片"
                  },
                  "color": "#B1D3C5",
                  "style": "secondary"
                }
              ]
            },
            "footer": {
              "type": "box",
              "layout": "vertical",
              "spacing": "sm",
              "contents": [
                {
                  "type": "separator",
                  "margin": "none"
                },
                {
                  "type": "button",
                  "flex": 2,
                  "style": "secondary",
                  "color": "#EAD880",
                  "action": {
                    "type": "message",
                    "text": "退出修改",
                    "label": "退出修改動作"
                  },
                  "margin": "xl"
                }
              ]
            }
          }
      # 將 bubble1 和 bubble2 放入 carousel 中
      bubbles.append(bubble1)
      bubbles.append(bubble2)
      # 將 carousel 包裝成 Flex Message
      flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = TextSendMessage(text="找不到符合條件的廠商商品。")
    return flex_message
#------該商品所有資訊(預購/依廠商或類別查詢)測試---------------------
def Pre_Product_Modification_FM(id):
    result = Per_Product(id)
    if result and len(result) > 0:
      bubbles = []
      pname = result[0][0] 
      introduction = result[0][1] 
      sell_price = result[0][2] 
      sell_price2 = result[0][3]
      
      if (result[0][4]  is None) or (result[0][4][:4]!= 'http'):
        picture = "https://i.imgur.com/rGlTAt3.jpg"
      else:
        picture = result[0][4]

      order_multiple = result[0][5]
      deadline = result[0][6]

      bubble1 = {
        "type": "bubble",
      "hero": {
        "type": "image",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "url": picture
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "預購商品所有資訊",
            "wrap": True,
            "weight": "bold",
            "size": "lg",
            "align": "center"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "1.商品名稱：",
                "size": "md",
                "margin": "none",
                "weight": "bold",
                "color": "#CE8467",
                "flex": 1
              },
              {
                "type": "text",
                "text": f" {pname}",
                "wrap": True,
                "flex": 2
              }
            ],
            "margin": "xxl",
            "spacing": "none",
            "position": "relative"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text":"2.商品簡介：",
                "weight": "bold",
                "margin": "none",
                "size": "md",
                "color": "#CE8467",
                "flex": 1
              },
              {
                "type": "text",
                "wrap": True,
                "flex": 2,
                "text": f" {introduction}"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text":"3.商品單價：",
                "weight": "bold",
                "size": "md",
                "margin": "none",
                "flex": 1,
                "color": "#CE8467"
              },
              {
                "type": "text",
                "text": f" {sell_price}",
                "flex": 2,
                "wrap": True
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text":"4.商品單價2：",
                "weight": "bold",
                "size": "md",
                "margin": "none",
                "flex": 1,
                "color": "#CE8467"
              },
              {
                "type": "text",
                "text": f" {sell_price2}",
                "flex": 2,
                "wrap": True
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text":"5.預購數量限制_倍數： ",
                "margin": "none",
                "size": "md",
                "weight": "bold",
                "flex": 1,
                "color": "#CE8467"
              },
              {
                "type": "text",
                "text": f" {order_multiple}",
                "wrap": True,
                "flex": 2
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text":"6.預購截止時間：",
                "size": "md",
                "margin": "none",
                "weight": "bold",
                "flex": 1,
                "color": "#CE8467"
              },
              {
                "type": "text",
                "text": f" {deadline}",
                "wrap": True,
                "flex": 2
              }
            ]
          }
        ],
        "margin": "xs"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "separator"
          },
          {
            "type": "button",
            "style": "secondary",
            "action": {
              "type": "message",
              "label": "退出修改動作",
              "text": "退出修改"
            },
            "color": "#EAD880",
            "margin": "xl"
          }
        ]
      }
    }
      bubble2 = {
        "type": "bubble",
        "body": {
          "type": "box",
          "layout": "vertical",
          "spacing": "xxl",
          "contents": [
            {
              "type": "text",
              "text": "修改預購商品所有資訊",
              "align": "center",
              "weight": "bold",
              "margin": "none",
              "size": "xl"
            },
            {
              "type": "separator",
              "margin": "md",
              "color": "#A9A9A9"
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": [],
              "spacing": "none",
              "margin": "none"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "1.修改_商品名稱",
                "text": "【修改商品資訊】商品名稱"
              },
              "color": "#CE8467",
              "style": "secondary",
              "margin": "xxl"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "2.修改_商品簡介",
                "text": "【修改商品資訊】商品簡介"
              },
              "color": "#CE8467",
              "style": "secondary"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "3.修改_商品售出單價",
                "text": "【修改商品資訊】商品售出單價"
              },
              "color": "#CE8467",
              "style": "secondary"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "4.修改_商品售出單價2",
                "text": "【修改商品資訊】商品售出單價2"
              },
              "color": "#CE8467",
              "style": "secondary"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "5.更換商品圖片",
                "text": "【修改商品資訊】更換商品圖片"
              },
              "color": "#CE8467",
              "style": "secondary"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "6.修改_商品預購倍數",
                "text": "【修改商品資訊】預購倍數"
              },
              "style": "secondary",
              "color": "#CE8467"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "7.修改_商品預購截止時間",
                "text": "【修改商品資訊】預購截止時間"
              },
              "style": "secondary",
              "color": "#CE8467"
            }
          ]
        },
        "footer": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "separator",
              "margin": "none"
            },
            {
              "type": "button",
              "flex": 2,
              "style": "secondary",
              "color": "#EAD880",
              "action": {
                "type": "message",
                 "text": "退出修改",
                "label": "退出修改動作"
              },
              "margin": "xl"
            }
          ]
        }
      }
               # 將 bubble1 和 bubble2 放入 carousel 中
      bubbles.append(bubble1)
      bubbles.append(bubble2)
      # 將 carousel 包裝成 Flex Message
      flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = TextSendMessage(text="找不到符合條件的廠商商品。")
    return flex_message