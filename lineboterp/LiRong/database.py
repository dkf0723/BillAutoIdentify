import mysql.connector
import requests
from mysql.connector import errorcode
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from relevant_information import dbinfo,imgurinfo
import os, io, pyimgur, glob
#安裝 Python 的 MySQL 連接器及其相依性>pip install mysql-connector-python
#安裝Python 的 pyimgur套件> pip install pyimgur
# Obtain connection string information from the portal

#-------------------資料庫連線----------------------
def databasetest():
  #取得資料庫資訊
  dbdata = dbinfo()  
  config = {
  'host': dbdata['host'],
  'user': dbdata['user'],
  'password': dbdata['password'],
  'database': dbdata['database']
  }
  # Construct connection string
  try:
    conn = mysql.connector.connect(**config)
    databasetest_msg = '資料庫連接成功'
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      databasetest_msg = '使用者或密碼有錯'
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      databasetest_msg = '資料庫不存在或其他錯誤'
    else:
      databasetest_msg = err
  else:
    cursor = conn.cursor()
  return {'databasetest_msg': databasetest_msg, 'conn':conn, 'cursor':cursor, 'config':config}

#查詢資料SELECT
def test_datasearch():
  #測試讀取資料庫願望清單(所有)
  implement = databasetest()
  conn = implement['conn']
  cursor = implement['cursor']
  query = "SELECT * FROM wishlist;"
  cursor.execute(query)
  result = cursor.fetchall()
  if result is not None:
    testmsg = "願望清單讀取內容：\n"
    for row in result:
      # 透過欄位名稱獲取資料
      uid = row[0]#'UID'
      name = row[1]#'商品名稱'
      #商品圖片
      reason = row[3]#'推薦原因'
      time = row[4]#'願望建立時間'
      member = row[5]#'會員_LINE_ID'
      # 在這裡進行資料處理或其他操作
      testmsg += ('第%s筆\n推薦會員:\n%s\n商品名稱：\n%s\n推薦原因：\n%s\n願望建立時間：\n%s\n---\n' %(uid,member,name,reason,time))
  else:
    testmsg = "找不到符合條件的資料。"
  # 關閉游標與連線
  testmsg += "(end)"
  cursor.close()
  conn.close()
  return testmsg

#修改資料UPDATE
def test_dataUPDATE():
  return

#-------------------圖片取得並發送----------------------
def imagesent():
    implement = databasetest()  # 定義 databasetest() 函式並返回相關物件
    img = []
    send = []
    conn = implement['conn']
    cursor = implement['cursor']
    #query = "SELECT 商品名稱, 商品圖片 FROM Product_information LIMIT 1 OFFSET 0;"#0開始1筆
    query = "SELECT 商品名稱, 商品圖片 FROM Product_information LIMIT 2 OFFSET 0;"
    cursor.execute(query)
    result = cursor.fetchall()
    
    if result is not None:
        for row in result:
            productname = row[0] # 圖片商品名稱
            output_path = row[1] # 圖片連結
            # 發送圖片
            text_msg = TextSendMessage(text=productname)
            image_msg = ImageSendMessage(
                original_content_url=output_path,  # 圖片原圖
                preview_image_url=output_path  # 圖片縮圖
            )
            img.append(text_msg)
            img.append(image_msg)
    else:
        img.append(TextSendMessage(text='找不到符合條件的資料。'))
    
    # 關閉游標與連線
    cursor.close()
    conn.close()
    send = tuple(img)  # 將列表轉換為元組最多五個
    return send

#-------------------刪除images資料夾中所有----------------------
def delete_images():
    folder_path = 'images'  # 資料夾路徑
    file_list = os.listdir(folder_path)
    
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"已刪除圖片檔案：{file_path}")

#-------------------images資料夾中圖片轉連結----------------------
def imagetolink():
  imgurdata = imgurinfo()
  image_storage = []
  folder_path = 'images'# 設定資料夾路徑
  # 使用 glob 模組取得資料夾中的 JPG 和 PNG 圖片檔案
  image_files = glob.glob(f"{folder_path}/*.jpg") + glob.glob(f"{folder_path}/*.png")
  # 讀取所有圖片檔案
  for file in image_files:
    # 獲取檔案名稱及副檔名
    filename, file_extension = os.path.splitext(file)
    filename = filename+file_extension# 檔案位置加副檔名
    image_storage.append(filename)

  #執行轉換連結
  for img_path in image_storage:
    CLIENT_ID = imgurdata['CLIENT_ID_data']
    PATH = img_path #A Filepath to an image on your computer"
    title = img_path
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    #image = uploaded_image.title + "連結：" + uploaded_image.link
    imagetitle = uploaded_image.title
    imagelink = uploaded_image.link
    print( imagetitle + "連結：" + imagelink)
    #delete_images()#刪除images檔案圖片
  return {'imagetitle':imagetitle,'imagelink':imagelink}

#-------------------取出未取名單---------------------------------

def order_details():
  OrderId = []
  LineId = []
  PhoneNumber = []
  OrderTime = []
  PickuptTime = []
  amount = []
  count = 0
  #讀取訂單資料(所有)
  implement = databasetest()
  conn = implement['conn']
  cursor = implement['cursor']
  query = "SELECT * FROM Order_information;"
  cursor.execute(query)
  result = cursor.fetchall()
  if result is not None:
    testmsg = "願望清單讀取內容：\n"
    for row in result:
      if row[5] == "未取":
        # 透過欄位名稱獲取資料
        OrderId.append(row[0])#'訂單編號'
        LineId.append(row[1])#'LineId'
        PhoneNumber.append(row[2])#電話
        OrderTime.append(row[3])#'下定時間'
        PickuptTime.append(row[4])#'取貨完成時間'
        amount.append(row[10])#'總額'
        # 在這裡進行資料處理或其他操作
        testmsg += ('共%s筆未取訂單\n---\n' %(count))
  else:
    testmsg = "找不到符合條件的資料。"
  # 關閉游標與連線
  testmsg += "(end)"
  cursor.close()
  conn.close()
  return testmsg
#-------------所有廠商名稱列出(FM)---------------
def test_manufacturers():
    testimplement = databasetest()
    conn = testimplement['conn']
    cursor = testimplement['cursor']
    query = "SELECT * FROM Manufacturer_Information;"
    cursor.execute(query)
    result = cursor.fetchall()
    
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
                          "text": f"廠商的編號 : {mid}",
                          "weight": "bold",
                          "margin": "xs",
                          "flex": 0},
                        {
                          "type": "text",
                          "text": f"廠商名稱 : {mname}",
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
                      "color": "#BB5E00",
                      "margin": "none",
                      "action": {
                                 "type": "message",
                                 "label": "選我選我",
                                 "text": f"選我選我 {mid}"
                                 },
                                 "height": "md",
                                 "offsetEnd": "none",
                                 "offsetBottom": "sm"}
                                ],
                                  "spacing": "none",
                                  "margin": "none"}
                                }
            bubbles.append(bubble)       
        flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "carousel", "contents": bubbles})
    else:
      flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "text", "text": "找不到符合條件的廠商。"})    
    cursor.close()
    conn.close()
    return flex_message
 #---------------此廠商所有商品(已變數/FM)-------------------------
def products_manufacturers(manufacturer_id):
    testAimplement = databasetest()
    conn = testAimplement['conn']
    cursor = testAimplement['cursor']
    query = f"SELECT * FROM Manufacturer_Information NATURAL JOIN Product_information natural join Purchase_Information WHERE 廠商編號 = '{manufacturer_id}'"
    cursor.execute(query)
    result = cursor.fetchall()
    
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[11]  # '商品名稱'
            stock_num = row[15]  # '庫存數量'
            pname_unit = row[1]  #  '商品單位'
            purchase_price = row[28] #'進貨單價'
            sell_price = row[16]  # '售出單價'
            bubble = {
                "type": "bubble",
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
                      "text": "hello"
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
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "text", "text": "找不到符合條件的廠商商品。"})
    
    cursor.close()
    conn.close()
    return flex_message
#----------------分類下所有商品列表(已變數)------------------------------
def test_categoryate(selected_category):
    testBimplement = databasetest()
    conn = testBimplement['conn']
    cursor = testBimplement['cursor']
    query = f"SELECT * FROM Manufacturer_Information NATURAL JOIN Product_information NATURAL JOIN Purchase_Information WHERE 商品ID LIKE '{selected_category}%'"
    cursor.execute(query)
    result = cursor.fetchall()
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[11]  # '商品名稱'
            stock_num = row[15]  # '庫存數量'
            pname_unit = row[1]  #  '商品單位'
            purchase_price = row[28] #'進貨單價'
            sell_price = row[16]  # '售出單價'
            bubble = {
                  "type": "bubble",
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
                        "text": "hello"
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
    cursor.close()
    conn.close()
    return flex_message