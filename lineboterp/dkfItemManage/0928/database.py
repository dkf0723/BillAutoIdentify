from linebot.models import FlexSendMessage
import mysql.connector
import requests
from datetime import datetime, timedelta
from mysql.connector import errorcode
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from relevant_information import imgurinfo
import os, io, pyimgur, glob
import manager
import time
import random #隨機產生
#-------------------取得現在時間----------------------
def gettime():
  current_datetime = datetime.now()# 取得當前的日期和時間
  modified_datetime = current_datetime + timedelta(hours=8)#時區轉換+8
  formatted_millisecond = modified_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
  formatted_datetime = modified_datetime.strftime('%Y-%m-%d %H:%M:%S')# 格式化日期和時間，不包含毫秒部分
  formatted_datetime2 = modified_datetime.strftime('%Y-%m-%dT%H:%M')# 格式化日期和時間，不包含毫秒部分
  formatted_date = modified_datetime.strftime('%Y-%m-%d')#格式化日期
  order_date = modified_datetime.strftime('%Y%m%d')#格式化日期，清除-
  return {'formatted_datetime':formatted_datetime,'formatted_date':formatted_date,'order_date':order_date,'formatted_millisecond':formatted_millisecond,'formatted_datetime2':formatted_datetime2}
#-------------------資料庫連線----------------------
#連線
def databasetest(db_pool, serial_number):
  db = manager.db
  timeget = gettime()
  formatted_datetime = timeget['formatted_datetime']
  #錯誤重新執行最大3次
  max_retries = 3  # 最大重試次數
  retry_count = 0  # 初始化重試計數
  conn = None
  while retry_count<max_retries:
    try:
      conn = db_pool.get_connection()
      databasetest_msg = '資料庫連接成功'
      break
    except mysql.connector.Error as err:
      if conn:
        conn.close()
      elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        databasetest_msg = '使用者或密碼有錯'
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        databasetest_msg = '資料庫不存在或其他錯誤'
      else:
        databasetest_msg = err
      conn = None
  
  if serial_number == 1:
    new_formatted_datetime = next_conn_time(formatted_datetime, 1)#取得下次執行時間
    db['databasetest_msg'] = databasetest_msg
    db['databaseup'] = formatted_datetime
    db['databasenext'] = new_formatted_datetime
    db['conn'] = conn
  elif serial_number == 2:
    new_formatted_datetime = next_conn_time(formatted_datetime, 2)#取得下次執行時間
    db['databasetest_msg1'] = databasetest_msg
    db['databaseup1'] = formatted_datetime
    db['databasenext1'] = new_formatted_datetime
    db['conn1'] = conn
  elif serial_number == 3:
    new_formatted_datetime = next_conn_time(formatted_datetime, 3)#取得下次執行時間
    if db['conn'] is not None:
      try:
        db['conn'].close()
      except mysql.connector.Error as err:
        conn = err
    db['databasetest_msg'] = databasetest_msg
    db['databaseup'] = formatted_datetime
    db['databasenext'] = new_formatted_datetime
    db['conn'] = conn
  elif serial_number == 4:
    new_formatted_datetime = next_conn_time(formatted_datetime, 4)#取得下次執行時間
    if db['conn'] is not None:
      try:
        db['conn1'].close()
      except mysql.connector.Error as err:
        conn = err
    db['databasetest_msg1'] = databasetest_msg
    db['databaseup1'] = formatted_datetime
    db['databasenext1'] = new_formatted_datetime
    db['conn1'] = conn

#下次更新時間計算
def next_conn_time(formatted_datetime, serial_number):
  nowtime = datetime.strptime(formatted_datetime, '%Y-%m-%d %H:%M:%S')
  check = nowtime.minute
  if serial_number in [1,3]:
    check1 = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57]
    addhours = []#小時進位分鐘
    for i in range(57,60):#57～59
      addhours.append(i)
    modified_add = next_time(check, check1, nowtime, addhours)#下次更新分鐘取得

  if serial_number in [2,4]:
    check1 = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    addhours = []#小時進位分鐘
    for i in range(55,60):#55～59
      addhours.append(i)
    modified_add = next_time(check, check1, nowtime, addhours)#下次更新分鐘取得
  new_formatted_datetime = modified_add.strftime('%Y-%m-%d %H:%M:%S')
  return new_formatted_datetime

#下次更新分鐘取得
def next_time(check, check1,nowtime, addhours):
  if check in addhours:
    modified_add = nowtime + timedelta(hours=1)
    modified_add = modified_add.replace(minute=0)
  else:
    next_minute = min([i for i in check1 if i > check])
    modified_add = nowtime.replace(minute=next_minute)
  return modified_add

#-------------------錯誤重試----------------------
def retry(category,query):#select/notselect
  block = 0#結束點是1
  step = 0 #第幾輪
  stepout = 0 #離開標記
  while block == 0:
    max = 3  # 最大重試次數
    count = 0  # 初始化重試計數
    connobtain = 'ok' #檢查是否取得conn連線資料
    while count<max:
      try:
        if step == 0:
          conn = manager.db['conn']
          cursor = conn.cursor()#重新建立游標
          break
        elif step == 1:
          conn = manager.db['conn1']
          cursor = conn.cursor()#重新建立游標
          stepout = 1 #第二輪標記，完成下面動作可退出
          break
      except (mysql.connector.Error,AttributeError):
        if conn: #如果conn的值不是None(有其他值)
          conn.rollback()
        count += 1 #重試次數累加
        connobtain = 'no'
        
    count = 0  # 重試次數歸零，用於後面的步驟
    if connobtain == 'ok':
      while count<max:
        step = 1 #下一輪設定
        stepout = 0 #回合恢復
        try:
          if category == 'select':
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()#游標關閉
            result2 = 'no'#不是購物車新增的內容
          elif category == 'notselect':
            cursor.execute(query)
            conn.commit()
            cursor.close()#游標關閉
            result = 'ok'
            result2 = 'ok'#購物車新增用
          stepout = 1 #不進行第二輪
          break
        except mysql.connector.Error as e:
          conn.rollback()  # 撤銷操作恢復到操作前的狀態
          count += 1 #重試次數累加
          result = [] #錯誤回傳內容
          result2 = 'no'#購物車新增用
          step = 1
          stepout = 1
          time.sleep(1)
      if stepout == 1:#成功取得資料後退出或兩輪都失敗退出迴圈
        block = 1
    else:
      if step == 1:
        cursor.close()#關閉第一輪游標的
      step = 1 #conn沒取到進入切換conn1
      if stepout == 1 and step == 1:#兩輪都失敗退出迴圈
        block = 1
        result = []
        result2 = 'no'
  return result
#-------------所有廠商名稱列出---------------
def test_manufacturers():
  query = "SELECT * FROM Manufacturer_Information;"
  category = 'select' #重試類別 select/notselect
  result = retry(category,query)
  return result
#---------------此廠商所有商品----------------
# def products_manufacturers(manufacturer_id):
#   query = f"SELECT * FROM Manufacturer_Information NATURAL JOIN Product_information natural join Purchase_Information WHERE 廠商編號 = '{manufacturer_id}'"
#   category = 'select' #重試類別 select/notselect
#   result = retry(category,query)
#   return result
def products_manufacturers(manufacturer_id):
  query = f"SELECT * FROM Manufacturer_Information NATURAL JOIN Product_information natural join Purchase_Information WHERE 廠商編號 = '{manufacturer_id}'"
  category = 'select'  # 重試類別 select/notselect
  result = retry(category, query)
  return result

def product_info(product_id):
  query = f"SELECT * FROM Product_information WHERE 商品ID = '{product_id}'"
  category = 'select'  # 重試類別 select/notselect
  result = retry(category, query)
  return result
#---------------此廠商下商品所有資訊----------------
def MP_information(product_name): 
  id = manager.user_id
  pid = manager.product[id + 'Product_Modification_Product_Name']
  query =f"UPDATE Product_information SET 商品名稱 = '{product_name}' WHERE 商品ID = '{pid}'"
  category = 'notselect' #重試類別 select/notselect
  result = retry(category,query) #成功回傳ok
  return result
#----------------分類下所有商品列表------------
def test_categoryate(selected_category):
  query = f"SELECT * FROM Manufacturer_Information NATURAL JOIN Product_information NATURAL JOIN Purchase_Information WHERE 商品ID LIKE '{selected_category}%'"
  category = 'select' #重試類別 select/notselect
  result = retry(category,query)
  return result

#-----------------正在測試中------------
# def test_Product_Modification(pid):
#   query = f"SELECT 現預購商品,商品名稱,商品ID FROM Product_information WHERE 商品ID = '{pid}'"
#   category = 'select'  # 重試類別 select/notselect
#   result = retry(category, query)
#   return result

def test_Product_Modification(pid):
  query = f"SELECT 現預購商品,商品名稱,商品ID FROM Product_information WHERE 商品ID = '{pid}'"
  category = 'select'  # 重試類別 select/notselect
  result = retry(category, query)
  if result != []:
    product_status = result[0][0]
  else:
    product_status = '查無'
  return product_status
                                                                    
# #-------------------查詢資料SELECT-------------
# def test_datasearch():
#   #測試讀取資料庫願望清單(所有)
#   implement = databasetest()
#   conn = implement['conn']
#   cursor = implement['cursor']
#   query = "SELECT * FROM wishlist;"
#   cursor.execute(query)
#   result = cursor.fetchall()
#   if result is not None:
#     testmsg = "願望清單讀取內容：\n"
#     for row in result:
#       # 透過欄位名稱獲取資料
#       uid = row[0]#'UID'
#       name = row[1]#'商品名稱'
#       #商品圖片
#       reason = row[3]#'推薦原因'
#       time = row[4]#'願望建立時間'
#       member = row[5]#'會員_LINE_ID'
#       # 在這裡進行資料處理或其他操作
#       testmsg += ('第%s筆\n推薦會員:\n%s\n商品名稱：\n%s\n推薦原因：\n%s\n願望建立時間：\n%s\n---\n' %(uid,member,name,reason,time))
#   else:
#     testmsg = "找不到符合條件的資料。"
#   # -----------------關閉游標與連線--------------------------
#   testmsg += "(end)"
#   cursor.close()
#   conn.close()
#   return testmsg

# #修改資料UPDATE
# def test_dataUPDATE():
#   return
# #-------------------圖片取得並發送----------------------
# def imagesent():
#     implement = databasetest()  # 定義 databasetest() 函式並返回相關物件
#     img = []
#     send = []
#     conn = implement['conn']
#     cursor = implement['cursor']
#     #query = "SELECT 商品名稱, 商品圖片 FROM Product_information LIMIT 1 OFFSET 0;"#0開始1筆
#     query = "SELECT 商品名稱, 商品圖片 FROM Product_information LIMIT 2 OFFSET 0;"
#     cursor.execute(query)
#     result = cursor.fetchall()
    
#     if result is not None:
#         for row in result:
#             productname = row[0] # 圖片商品名稱
#             output_path = row[1] # 圖片連結
#             # 發送圖片
#             text_msg = TextSendMessage(text=productname)
#             image_msg = ImageSendMessage(
#                 original_content_url=output_path,  # 圖片原圖
#                 preview_image_url=output_path  # 圖片縮圖
#             )
#             img.append(text_msg)
#             img.append(image_msg)
#     else:
#         img.append(TextSendMessage(text='找不到符合條件的資料。'))
    
#     # 關閉游標與連線
#     cursor.close()
#     conn.close()
#     send = tuple(img)  # 將列表轉換為元組最多五個
#     return send

# #-------------------刪除images資料夾中所有----------------------
# def delete_images():
#     folder_path = 'images'  # 資料夾路徑
#     file_list = os.listdir(folder_path)
    
#     for file_name in file_list:
#         file_path = os.path.join(folder_path, file_name)
#         if os.path.isfile(file_path):
#             os.remove(file_path)
#             print(f"已刪除圖片檔案：{file_path}")

# #-------------------images資料夾中圖片轉連結----------------------
# def imagetolink():
#   imgurdata = imgurinfo()
#   image_storage = []
#   folder_path = 'images'# 設定資料夾路徑
#   # 使用 glob 模組取得資料夾中的 JPG 和 PNG 圖片檔案
#   image_files = glob.glob(f"{folder_path}/*.jpg") + glob.glob(f"{folder_path}/*.png")
#   # 讀取所有圖片檔案
#   for file in image_files:
#     # 獲取檔案名稱及副檔名
#     filename, file_extension = os.path.splitext(file)
#     filename = filename+file_extension# 檔案位置加副檔名
#     image_storage.append(filename)

#   #執行轉換連結
#   for img_path in image_storage:
#     CLIENT_ID = imgurdata['CLIENT_ID_data']
#     PATH = img_path #A Filepath to an image on your computer"
#     title = img_path
#     im = pyimgur.Imgur(CLIENT_ID)
#     uploaded_image = im.upload_image(PATH, title=title)
#     #image = uploaded_image.title + "連結：" + uploaded_image.link
#     imagetitle = uploaded_image.title
#     imagelink = uploaded_image.link
#     print( imagetitle + "連結：" + imagelink)
#     #delete_images()#刪除images檔案圖片
#   return {'imagetitle':imagetitle,'imagelink':imagelink}

# #-------------------取出未取名單---------------------------------
# def order_details():
#   OrderId = []
#   LineId = []
#   PhoneNumber = []
#   OrderTime = []
#   PickuptTime = []
#   amount = []
#   count = 0
#   #讀取訂單資料(所有)
#   implement = databasetest()
#   conn = implement['conn']
#   cursor = implement['cursor']
#   query = "SELECT * FROM Order_information;"
#   cursor.execute(query)
#   result = cursor.fetchall()
#   if result is not None:
#     testmsg = "願望清單讀取內容：\n"
#     for row in result:
#       if row[5] == "未取":
#         # 透過欄位名稱獲取資料
#         OrderId.append(row[0])#'訂單編號'
#         LineId.append(row[1])#'LineId'
#         PhoneNumber.append(row[2])#電話
#         OrderTime.append(row[3])#'下定時間'
#         PickuptTime.append(row[4])#'取貨完成時間'
#         amount.append(row[10])#'總額'
#         # 在這裡進行資料處理或其他操作
#         testmsg += ('共%s筆未取訂單\n---\n' %(count))
#   else:
#     testmsg = "找不到符合條件的資料。"
#   # 關閉游標與連線
#   testmsg += "(end)"
#   cursor.close()
#   conn.close()
#   return testmsg

# def test_manufacturers():
#     query = "SELECT * FROM Manufacturer_Information;"
#     category = 'select' #重試類別 select/notselect
#     result = retry(category,query)
#     return result

# def single_imagetolink():
#   id = lineboterp.user_id
#   storageimg = lineboterp.storage
#   imgurdata = imgurinfo()
#   # 取得圖片路徑
#   image_files = f"{storageimg[id+'img']}" #例：images/FXR0.jpg
#   #執行轉換連結
#   CLIENT_ID = imgurdata['CLIENT_ID_data']
#   PATH = image_files
#   title = image_files[:-4]
#   im = pyimgur.Imgur(CLIENT_ID)
#   uploaded_image = im.upload_image(PATH, title=title)
#   imagelink = uploaded_image.link
#   storageimg[id+'imagelink'] = imagelink #儲存圖片連結
#   #執行資料夾中此圖片刪除
#   if os.path.isfile(image_files):
#       os.remove(image_files)
def getPhoneNumberByPhoneNumberLastThreeYard(phoneNumber):
    query = f"SELECT distinct 電話 FROM Order_information WHERE 電話 LIKE '%{phoneNumber}' and 訂單狀態未取已取 like '%未取';"
    result = retry('select',query)
    send = []
    if result is not None:
        for row in result:
            send.append(row[0])       
    # 關閉游標與連線
    return send
def getOrderByPhoneNumber(phoneNumber):
    query = f"SELECT 訂單編號 FROM Order_information WHERE 電話 = '{phoneNumber}' and 訂單狀態未取已取 like '%未取';"
    # cursor.execute(query)
    result = retry('select',query)
    # result = cursor.fetchall() 
    send = []
    if result is not None:
        for row in result:
            send.append(row[0])       
    # 關閉游標與連線
    return send

def getOrderDetailByPhoneNumber(phoneNumber):
    query = f"SELECT o.訂單編號,p.商品名稱 ,o.訂購數量,o.商品小計 FROM Product_information as p inner join order_details as o on o.商品ID =p.商品ID  WHERE o.訂單編號 in( select 訂單編號 from Order_information where 電話 = '{phoneNumber}' and 訂單狀態未取已取 like '%未取' );"
    result = retry('select', query)
    test =''
    send = []
    a=[]
    for i in result:
        if i[0] == test:
          a.append(i)
        else :
          test = i[0]  
          send.append(a)
          a =[]
          a.append(i)
    send.append(a)
    send.pop(0)
    return send
def getOrderDetailByOrder(order):
    query = f"SELECT o.訂單編號,p.商品名稱,o.訂購數量,o.商品小計 FROM Product_information as p inner join order_details as o on o.商品ID =p.商品ID  WHERE o.訂單編號 = '{order}';"
    result = retry('select', query)
    send=[]    
    send.append(result)
    # 關閉游標與連線
    return send
def getTotalByOrder(order):
    query = f"SELECT 總額 FROM Order_information WHERE 訂單編號 = '{order}';"
    result = retry('select', query)
    return result[0][0]
def createProduct(id):
  storage = manager.global_Storage
  pname = storage[id+'pname']
  category= storage[id+'category']
  unit= storage[id+'unit']
  introduction= storage[id+'introduction']
  unitPrice= storage[id+'unitPrice']
  unitPrice2= storage[id+'unitPrice2']
  picture= storage[id+'picture']
  returnProduct= storage[id+'returnProduct']
  # query = f"SELECT 總額 FROM Order_information WHERE 訂單編號 = '{order}';"
  # result = retry('notselect', query)
  # return result
def updateOrder(id):
  storage = manager.global_Storage
  if storage[id+'order'][:1] == '0':
    query = f"UPDATE Order_information SET 訂單狀態未取已取 = CASE WHEN 訂單狀態未取已取 = '現購未取' THEN '現購已取' WHEN 訂單狀態未取已取 = '預購未取' THEN '預購已取' ELSE 訂單狀態未取已取 END , 取貨完成時間 = now() WHERE 電話 = '{storage[id+'order']}' and 訂單狀態未取已取 like '%未取' ;"
    result = retry('notselect', query)
  else : 
    query = f"UPDATE Order_information SET 訂單狀態未取已取 = CASE WHEN 訂單狀態未取已取 = '現購未取' THEN '現購已取' WHEN 訂單狀態未取已取 = '預購未取' THEN '預購已取' ELSE 訂單狀態未取已取 END , 取貨完成時間 = now()  WHERE 訂單編號 = '{storage[id+'order']}' and 訂單狀態未取已取 like '%未取';"
    # query = f"UPDATE Order_information SET 訂單狀態未取已取 = ''  WHERE 訂單編號 = '{storage[id+'order']} and 訂單狀態未取已取 like '%未取'';"
    result = retry('notselect', query)
  return result
