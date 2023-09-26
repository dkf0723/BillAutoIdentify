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
  formatted_date = modified_datetime.strftime('%Y-%m-%d')#格式化日期
  order_date = modified_datetime.strftime('%Y%m%d')#格式化日期，清除-
  return {'formatted_datetime':formatted_datetime,'formatted_date':formatted_date,'order_date':order_date,'formatted_millisecond':formatted_millisecond}
#-------------------資料庫連線----------------------
#連線
def databasetest(db_pool, serial_number):
  db = manager.db
  timeget = gettime()
  formatted_datetime = timeget['formatted_datetime']
  #錯誤重新執行最大3次
  max_retries = 3  # 最大重試次數
  retry_count = 0  # 初始化重試計數
  while retry_count<max_retries:
    try:
      conn = db_pool.get_connection()
      databasetest_msg = '資料庫連接成功'
      break
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        databasetest_msg = '使用者或密碼有錯'
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        databasetest_msg = '資料庫不存在或其他錯誤'
      else:
        databasetest_msg = err
  
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
    db['conn'].close()
    db['databasetest_msg'] = databasetest_msg
    db['databaseup'] = formatted_datetime
    db['databasenext'] = new_formatted_datetime
    db['conn'] = conn
  elif serial_number == 4:
    new_formatted_datetime = next_conn_time(formatted_datetime, 4)#取得下次執行時間
    db['conn1'].close()
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
      except mysql.connector.Error as e:
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
          elif category == 'notselect':
            cursor.execute(query)
            conn.commit()
            cursor.close()#游標關閉
            result = 'ok'
          stepout = 1 #不進行第二輪
          break
        except mysql.connector.Error as e:
          conn.rollback()  # 撤銷操作恢復到操作前的狀態
          count += 1 #重試次數累加
          result = [] #錯誤回傳內容
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
  return result

#----------------新增-依廠商查詢所有廠商名稱--------------------
def alln_manufacturers_name():
  query = "SELECT 廠商編號,廠商名 FROM Manufacturer_Information;"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result
#-----------------新增->依廠商查詢所有商品的商品ID及商品名稱-----------------
def nm_pur_info(manufacturerR_id):
  query = f"SELECT 商品ID,商品名稱 FROM  Product_information natural join Manufacturer_Information where 廠商編號 ='{manufacturerR_id}'"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result
#-----------------新增->依分類查詢所有商品的商品ID及商品名稱-----------------
def nc_pur_info(selectedr_category):
  query = f"SELECT 商品ID,商品名稱 FROM  Product_information where 商品ID like'{selectedr_category}%'"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result




#----------------修改-依廠商查詢所有廠商名稱--------------------
def allr_manufacturers_name():
  query = "SELECT 廠商編號,廠商名 FROM Manufacturer_Information;"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result
#-----------------修改->依廠商查詢所有商品的商品ID及商品名稱-----------------
def revm_pur_info(manufacturerR_id):
  query = f"SELECT 商品ID,商品名稱 FROM  Product_information natural join Manufacturer_Information where 廠商編號 ='{manufacturerR_id}'"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result
#-----------------修改->依分類查詢所有商品的商品ID及商品名稱-----------------
def revc_pur_info(selectedr_category):
  query = f"SELECT 商品ID,商品名稱 FROM  Product_information where 商品ID like'{selectedr_category}%'"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result
#----------------庫存-查詢所有廠商編號及廠商名--------------------
def alls_manufacturers_name():
  query = "SELECT 廠商編號,廠商名 FROM Manufacturer_Information;"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result
#--------------依廠商->庫存資訊---------------
def stock_manufacturers(manufacturer_id):
  query = f"SELECT 商品ID,商品名稱,庫存數量,售出單價 FROM Product_information WHERE 廠商編號 = '{manufacturer_id}'"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result
#-----------------依分類->庫存資訊-----------------
def stock_categoryate(selected_category):
  query = f"SELECT 商品ID,商品名稱,庫存數量,售出單價 FROM  Product_information WHERE 商品ID LIKE '{selected_category}%'"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result
#-----------------依廠商->進貨資訊---------------
def purchase_manufacturers(manufacturerA_id):
  query = f"SELECT * FROM Manufacturer_Information NATURAL JOIN Purchase_Information NATURAL JOIN Product_information WHERE 廠商編號 = '{manufacturerA_id}'"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result
#-----------------依分類->進貨資訊-----------------
def purchase_categoryate(selectedA_category):
  query = f"SELECT * FROM Manufacturer_Information NATURAL JOIN Purchase_Information NATURAL JOIN Product_information WHERE 商品ID LIKE '{selectedA_category}%'"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result
#----------------進貨-查詢所有廠商編號及廠商名稱--------------------
def allp_manufacturers_name():
  query = "SELECT * FROM Manufacturer_Information;"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result
#-----------------新增->依分類查詢所有商品的廠商編號及商品ID-----------------
def new_pur_info(product_name):
  query = f"SELECT * FROM Product_information natural join Manufacturer_Information WHERE 商品名稱 LIKE '%{product_name}%'"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result
#-----------------抓取進貨中商品-----------------
def puring_pro():
  query = f"SELECT 商品ID,商品名稱,廠商編號,廠商名,進貨數量,進貨狀態,進貨時間 FROM Purchase_Information natural join Product_information natural join Manufacturer_Information WHERE 進貨狀態 ='進貨中'"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result
#-----------------抓取已到貨商品-----------------
def pured_pro():
  query = f"SELECT 商品ID,商品名稱,廠商編號,廠商名,進貨數量,進貨狀態,進貨時間 FROM Purchase_Information natural join Product_information natural join Manufacturer_Information WHERE 進貨狀態 ='已到貨'"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result
#------------------更改進貨中的商品狀態-----------
def puring_trastate(manufacturerV_id):
  query = f"UPDATE Purchase_Information SET 進貨狀態 = '已到貨' WHERE 商品ID = '{manufacturerV_id}'"
  category ='notselect' #重試類別select/notselect
  result = retry(category,query)
  return result
#-----------------抓取消費者訂單編號----------------
def order_inf():
  query = f"SELECT 商品ID,訂單編號,訂單狀態未取已取 FROM order_details natural join Order_information"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result
#-----------------抓取預購截止的商品---------------
def preorder_end():
  query = f"SELECT 商品ID,商品名稱,現預購商品 FROM Product_information WHERE 現預購商品 = '預購截止'"
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  return result
#-----------------修改現預購商品欄位為預購進貨---------------
def endtopur_upd(manufacturerP_id):
  query = f"UPDATE Product_information SET 現預購商品 = '預購進貨' WHERE 商品ID = '{manufacturerP_id}'"
  category ='notselect' #重試類別select/notselect
  result = retry(category,query)
  return result

#def AA_BB():
  #query = f"SELECT 訂單編號 from order_details where 商品ID = '{manufacturerP_id}'"
  #category ='select' #重試類別select/notselect
  #result = retry(category,query)
  #return result


"""
#-------------------圖片取得並發送----------------------
def imagesent():
    implement = databasetest()  # 定義 databasetest() 函式並返回相關物件 #要
    img = []
    send = []
    conn = implement['conn'] 
    cursor = implement['cursor'] 
    #query = "SELECT 商品名稱, 商品圖片 FROM Product_information LIMIT 1 OFFSET 0;"#0開始1筆
    query = "SELECT 商品名稱, 商品圖片 FROM Product_information LIMIT 2 OFFSET 0;" #要
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
  return {'imagetitle':imagetitle,'imagelink':imagelink}"""