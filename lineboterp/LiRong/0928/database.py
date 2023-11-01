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
  formatted_datetime2 = modified_datetime.strftime('%Y-%m-%dT%H:%M')# 給日期選擇器的
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
        if category == 'select':
          result = []
        else:
          result = 'no'
        result2 = 'no'
  return result
#-------------所有廠商名稱列出---------------
def db_manufacturers():
  query = "SELECT * FROM Manufacturer_Information;"
  category = 'select' #重試類別 select/notselect
  result = retry(category,query)
  return result
#--------------此廠商所有商品----------------
def db_products_manufacturers(manufacturer_id,choose):
  if choose != 'stop':
    test1 = f"廠商編號 = '{manufacturer_id}' and 現預購商品 <> '現購停售'and 現預購商品 <> '預購截止'"
  else:
    test1 = f"現預購商品 = '現購停售' or 現預購商品 = '預購截止'"
  query = f"SELECT 商品ID,商品名稱,商品圖片,庫存數量,商品單位,進貨單價,售出單價,現預購商品 FROM Product_information NATURAL JOIN Purchase_Information WHERE {test1}"
  category = 'select'  # 重試類別 select/notselect
  result = retry(category, query)
  return result
#-------------分類下所有商品列表------------
def db_categoryate(selected_category):
  query = f"SELECT 商品ID,商品名稱,商品圖片,庫存數量,商品單位,進貨單價,售出單價,現預購商品 FROM Product_information NATURAL JOIN Purchase_Information WHERE 商品ID LIKE '{selected_category}%' and 現預購商品 <> '現購停售'and 現預購商品 <> '預購截止'"
  category = 'select' #重試類別 select/notselect
  result = retry(category,query)
  return result
# ---------------修改商品系列-----------------
def MP_information_modify(field_to_modify, new_value, pid):
    if field_to_modify in ["商品名稱", "商品簡介", "售出單價", "售出單價2", "預購數量限制_倍數","預購截止時間","商品圖片"]:
        query = f"UPDATE Product_information SET {field_to_modify} = '{new_value}' WHERE 商品ID = '{pid}'"
        category = 'notselect' # 重試類別 select/notselect
        result = retry(category, query) # 成功回傳 ok
        return result
    else:
        return "無效欄位名稱"    
#--------------辨識商品狀態進而選擇FM------------
def Product_status():
  user_id = manager.user_id
  pid = manager.product[user_id + 'Product_Modification_Product_id']
  query = f"SELECT 現預購商品,商品名稱,商品ID FROM Product_information WHERE 商品ID = '{pid}'"
  category = 'select'  # 重試類別 select/notselect
  result = retry(category, query)
  if result != []:
    product_status = result[0][0]
  else:
    product_status = '查無'
  return product_status    
#--------------現購FM函數------------------------
def Now_Product(id):
  query = f"SELECT 商品名稱, 商品簡介, 售出單價, 售出單價2,商品圖片 FROM Product_information natural join Purchase_Information WHERE 商品ID = '{id}'"
  category = 'select'  # 重試類別 select/notselect
  result = retry(category, query)
  return result                        

#--------------預購FM函數------------------------
def Per_Product(id):
  query = f"SELECT 商品名稱, 商品簡介, 售出單價, 售出單價2,商品圖片,預購數量限制_倍數,預購截止時間 FROM Product_information natural join Purchase_Information WHERE 商品ID = '{id}'"
  category = 'select'  # 重試類別 select/notselect
  result = retry(category, query)
  return result                 

#---------------停售-----------------------------
def stop_time(pid):
  query = f"UPDATE Product_information SET 現預購商品 = '現購停售' WHERE 商品ID = '{pid}'"
  category = 'notselect'  # 重試類別 select/notselect
  result = retry(category, query)
  return result