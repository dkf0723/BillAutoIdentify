from linebot.models import TextSendMessage,FlexSendMessage
import manager
import database
from database import Now_Product,Per_Product, db_manufacturers,db_products_manufacturers,db_categoryate
#-------------商品管理一開始的畫面-------
def Product_management():
    Product_management = []
    info1 = {
            "type": "bubble",
            "hero": {
              "type": "image",
              "size": "full",
              "aspectRatio": "20:13",
              "aspectMode": "fit",
              "url": "https://i.imgur.com/iajkZJY.jpg"
            },
            "body": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": "商品 查詢 / 修改 / 下架",
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
                          "text": "※商品資料列表與修改",
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
                          "text": "※商品停售下架",
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
                    "text": "【查詢/修改/下架】",
                    "label": "查詢 / 修改 / 下架"
                  },
                  "height": "sm",
                  "color": "#7b97cd"
                }
              ],
              "flex": 0,
              "margin": "xs"
            }
          }
    Product_management.append(info1)
    info2 = {
            "type": "bubble",
            "hero": {
              "type": "image",
              "size": "full",
              "aspectRatio": "20:13",
              "aspectMode": "fit",
              "url": "https://i.imgur.com/ggOl79q.jpg"
            },
            "body": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": "停售及截止商品",
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
                          "text": "※停售及截止商品列表顯示",
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
                    "text": "【停售及截止商品列表 】",
                    "label": "停售及截止商品"
                  },
                  "height": "sm",
                  "color": "#7b97cd"
                }
              ],
              "flex": 0,
              "margin": "xs"
            }
          }
    Product_management.append(info2)
    info3 = {
            "type": "bubble",
            "hero": {
              "type": "image",
              "size": "full",
              "aspectRatio": "20:13",
              "aspectMode": "fit",
              "url": "https://i.imgur.com/TdoRVYb.jpg"
            },
            "body": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": "新增商品",
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
                          "text": "※新增商品資訊",
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
                    "text": "【新增上架】",
                    "label": "新增商品"
                  },
                  "height": "sm",
                  "color": "#7b97cd"
                }
              ],
              "flex": 0,
              "margin": "xs"
            }
          }
    Product_management.append(info3)
    screen =FlexSendMessage(
                            alt_text='商品管理服務選擇',
                            contents={
                                "type": "carousel",
                                "contents": Product_management  
                                } 
                            )
    return screen
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
        "align": "center",
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
                      "text": "【廠商列表下一頁1】"+ str(pagemax+1) +"～"+ str(pagemax+9)
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
                "color": "#7b97cd",
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
                  "color": "#db4d4d",
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
                "color": "#db4d4d",
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
                "color": "#db4d4d",
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
              "align": "center",
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
                      "text": f"商品ID: {pid[i]}",
                      "weight": "bold",
                      "margin": "xs"
                    },
                    {
                      "type": "text",
                      "text": f"商品名稱：{pname[i]}",
                      "flex": 0,
                      "margin": "sm",
                      "weight": "bold",
                      "contents": []
                    },
                    {
                      "type": "text",
                      "text": f"庫存數量: {stock_num[i]}",
                      "weight": "bold",
                      "margin": "sm"
                    },
                    {
                      "type": "text",
                      "text": f"商品單位: {pname_unit[i]}",
                      "weight": "bold",
                      "margin": "sm"
                    },
                    {
                      "type": "text",
                      "text": f"進貨單價: {purchase_price[i]}",
                      "weight": "bold",
                      "margin": "sm"
                    },
                    {
                      "type": "text",
                      "text": f"售出單價: {sell_price[i]}",
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
      pagemin = manager.list_page[manager.user_id+'類別商品數量min']
      pagemax = manager.list_page[manager.user_id+'類別商品數量max']#9
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
                "color": "#7b97cd",
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
                  "color": "#db4d4d",
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
                  "color": "#db4d4d",
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
                "align": "center",
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
                        "text": f"商品ID: {pid[i]}",
                        "weight": "bold",
                        "margin": "xs"
                      },
                      {
                        "type": "text",
                        "text": f"商品名稱：{pname[i]}",
                        "flex": 0,
                        "margin": "sm",
                        "weight": "bold",
                        "contents": []
                      },
                      {
                        "type": "text",
                        "text": f"庫存數量: {stock_num[i]}",
                        "weight": "bold",
                        "margin": "sm"
                      },
                      {
                        "type": "text",
                        "text": f"商品單位: {pname_unit[i]}",
                        "weight": "bold",
                        "margin": "sm"
                      },
                      {
                        "type": "text",
                        "text": f"進貨單價: {purchase_price[i]}",
                        "weight": "bold",
                        "margin": "sm"
                      },
                      {
                        "type": "text",
                        "text": f"售出單價: {sell_price[i]}",
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
                "label": "5.修改_商品預購倍數",
                "text": "【修改商品資訊】預購倍數"
              },
              "style": "secondary",
              "color": "#CE8467"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "6.修改_商品預購截止時間",
                "text": "【修改商品資訊】預購截止時間"
              },
              "style": "secondary",
              "color": "#CE8467"
            },
             {
              "type": "button",
              "action": {
                "type": "message",
                "label": "7.更換商品圖片",
                "text": "【修改商品資訊】更換商品圖片"
              },
              "color": "#CE8467",
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
def showOrder():
    Notpickedup_preordered_history_screen = []
    id = manager.user_id
    global_Storage= manager.global_Storage
    for i in global_Storage[id+'orders'][global_Storage[id+'base']:global_Storage[id+'base'] + 10 ] :        
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
                sum = int(j[2])*int(j[3])
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
    if len(global_Storage[id+'orders'])>global_Storage[id+'base']+10:
          Notpickedup_preordered_history_screen.append({
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
                      "text": "下一頁"
                      }
                    }
                ]
            }
        })
    screen =FlexSendMessage(
                            alt_text='未取/預購/歷史訂單選擇',
                            contents={
                                "type": "carousel",
                                "contents": Notpickedup_preordered_history_screen   
                                } 
                            )
    return screen

def create_now_purchase_product(id):
  storage = manager.global_Storage
  pname = storage[id+'pname']
  category= storage[id+'category']
  unit= storage[id+'unit']
  introduction= storage[id+'introduction']
  unitPrice= storage[id+'unitPrice']
  unitPrice2= storage[id+'unitPrice2']
  picture= storage[id+'picture']
  returnProduct= storage[id+'returnProduct']
  bubble = {
              "type": "bubble",
              "hero": {
                "type": "image",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_2_restaurant.png",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                  "type": "uri",
                  "uri": "https://linecorp.com"
                }
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "action": {
                  "type": "uri",
                  "uri": "https://linecorp.com"
                },
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{pname[:100]}",
                      "text": '修改品名'
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{category[:100]}",
                      "text": f"修改商品類別"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{unit[:100]}",
                      "text": f"修改商品單位"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{introduction[:100]}",
                      "text": f"修改商品簡介"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{unitPrice[:100]}",
                      "text": f"修改商品售出單價"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{unitPrice2[:100]}",
                      "text": f"修改商品售出單價2"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{picture[:100]}",
                      "text": f"修改商品圖片"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{returnProduct[:100]}",
                      "text": f"修改可否退換貨"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "style": "secondary",
                    "color": "#EAD880",
                    "margin": "xs",
                    "action": {
                      "type": "message",
                      "label": "建立商品",
                      "text": "建立商品"
                    },
                    "height": "md"
                  }
                ],
                "spacing": "md",
                "margin": "md"
              }
            }
  screen =FlexSendMessage(
                            alt_text='未取/預購/歷史訂單選擇',
                            contents = bubble
                            )
  return screen


def create_preorder(id):
  storage = manager.global_Storage
  pname = storage[id+'pname']
  category= storage[id+'category']
  unit= storage[id+'unit']
  introduction= storage[id+'introduction']
  unitPrice= storage[id+'unitPrice']
  unitPrice2= storage[id+'unitPrice2']
  picture= storage[id+'picture']
  multiple= storage[id+'multiple']
  deadline= storage[id+'deadline']
  bubble = {
              "type": "bubble",
              "hero": {
                "type": "image",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_2_restaurant.png",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                  "type": "uri",
                  "uri": "https://linecorp.com"
                }
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "action": {
                  "type": "uri",
                  "uri": "https://linecorp.com"
                },
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{pname[:100]}",
                      "text": '修改品名'
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{category[:100]}",
                      "text": f"修改商品類別"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{unit[:100]}",
                      "text": f"修改商品單位"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{introduction[:100]}",
                      "text": f"修改商品簡介"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{unitPrice[:100]}",
                      "text": f"修改商品售出單價"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{unitPrice2[:100]}",
                      "text": f"修改商品售出單價2"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{picture[:100]}",
                      "text": f"修改商品圖片"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{multiple[:100]}",
                      "text": f"修改商品預購倍數"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{deadline[:100]}",
                      "text": f"修改商品預購截止時間"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "style": "secondary",
                    "color": "#EAD880",
                    "margin": "xs",
                    "action": {
                      "type": "message",
                      "label": "建立商品",
                      "text": "建立商品"
                    },
                    "height": "md"
                  }
                ],
                "spacing": "md",
                "margin": "md"
              }
            }

  screen =FlexSendMessage(
                            alt_text='未取/預購/歷史訂單選擇',
                            contents = bubble
                            )
  return screen

def template_message(check_text,datetime):
  template_message = FlexSendMessage(
                            alt_text='預購截止時間選擇',
                            contents={
                                "type": "carousel",
                                "contents": [{
                                "type": "bubble",
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "選擇日期時間",
                                        "weight": "bold",
                                        "size": "xl"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"{check_text}",
                                        "wrap": True,
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
                                        "style": "link",
                                        "height": "sm",
                                        "action": {
                                        "type": "datetimepicker",
                                        "label": "點擊選擇日期與時間",
                                        "data": "預購截止時間",
                                        "mode": "datetime",
                                        "min": f"{datetime}"
                                        }
                                    }
                                    ],
                                    "flex": 0
                                }
                                }]   
                                } 
                            )
  return template_message