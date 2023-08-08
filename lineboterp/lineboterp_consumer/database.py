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
import lineboterp
#安裝 Python 的 MySQL 連接器及其相依性>pip install mysql-connector-python
#安裝Python 的 pyimgur套件> pip install pyimgur
# Obtain connection string information from the portal

#-------------------取得現在時間----------------------
def time():
  current_datetime = datetime.now()# 取得當前的日期和時間
  modified_datetime = current_datetime + timedelta(hours=8)#時區轉換+8
  formatted_datetime = modified_datetime.strftime('%Y-%m-%d %H:%M:%S')# 格式化日期和時間，不包含毫秒部分
  formatted_date = modified_datetime.strftime('%Y-%m-%d')#格式化日期
  order_date = modified_datetime.strftime('%Y%m%d')#格式化日期，清除-
  return {'formatted_datetime':formatted_datetime,'formatted_date':formatted_date,'order_date':order_date}
#-------------------資料庫連線----------------------
def databasetest():
  db = lineboterp.db
  #取得資料庫資訊
  dbdata = dbinfo()  
  config = {
  'host': dbdata['host'],
  'user': dbdata['user'],
  'password': dbdata['password'],
  'database': dbdata['database']
  }
  #錯誤重新執行最大3次
  max_retries = 3  # 最大重試次數
  retry_count = 0  # 初始化重試計數
  while retry_count<max_retries:
    try:
      conn = mysql.connector.connect(**config)
      databasetest_msg = '資料庫連接成功'
      break
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        databasetest_msg = '使用者或密碼有錯'
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        databasetest_msg = '資料庫不存在或其他錯誤'
      else:
        databasetest_msg = err
  db['databasetest_msg'] = databasetest_msg
  cursor = conn.cursor()
  db['conn'] = conn
  db['cursor'] = cursor
#-------------------檢查userid是否在資料庫即是否有購物車基本資料----------------------
def member_profile(userid):
  member = lineboterp.member
  conn = lineboterp.db['conn']
  cursor = lineboterp.db['cursor']
  timeget = time()
  formatted_datetimeget = timeget['formatted_datetime']
  order_dateget = timeget['order_date']
  query = """SELECT 會員_LINE_ID FROM member_profile;""" #會員資料檢查
  #錯誤重新執行最大3次
  max_retries = 3  # 最大重試次數
  retry_count = 0  # 初始化重試計數
  while retry_count<max_retries:
    try:
      cursor.execute(query)
      member_result = cursor.fetchall()
      break
    except mysql.connector.Error as e:
      retry_count += 1 #重試次數累加

  query1 = f"""
          SELECT 訂單編號, 會員_LINE_ID ,訂單成立時間
          FROM Order_information 
          WHERE 訂單編號 like'cart%' and 訂單成立時間 <= '{formatted_datetimeget}'
          ORDER BY 訂單成立時間 DESC,訂單編號 DESC;
          """#購物車資料檢查(DESC遞減取得最新)
  cursor.execute(query1)
  cart_result = cursor.fetchall()
  storagememberlist = []#存放查詢到的所有會員列表
  storagecartlist = []#存放查詢到的所有購物車會員列表

  if member_result == []:
    query3 = f"""
        INSERT INTO member_profile (會員_LINE_ID,會員信賴度_取貨率退貨率,加入時間,身分別)
        VALUES ( '{userid}','0.80', '{formatted_datetimeget}','消費者');
        """
    cursor.execute(query3)
    conn.commit()
  else:
    for row in member_result:
      memberlist = row[0]
      storagememberlist.append(memberlist)
    if userid not in storagememberlist:
      query3 = f"""
        INSERT INTO member_profile (會員_LINE_ID,會員信賴度_取貨率退貨率,加入時間,身分別)
        VALUES ( '{userid}','0.80', '{formatted_datetimeget}','消費者');
        """
      cursor.execute(query3)
      conn.commit()

  if cart_result == []:
    serial_number = '000001'
    query4 = f"""
          INSERT INTO Order_information (訂單編號,會員_LINE_ID,電話,訂單狀態未取已取,訂單成立時間)
          VALUES ( 'cart{order_dateget}{str(serial_number)}','{userid}','add','dd' ,'{formatted_datetimeget}');
          """
    cursor.execute(query4)
    conn.commit()
  else:
    checkaddtime = cart_result[0][0]#取得最新一筆購物車序號
    for row1 in cart_result:
      cartlist = row1[1]
      storagecartlist.append(cartlist)
    if userid not in storagecartlist:#最新一筆購物車序號
      if checkaddtime[4:12] == f"{str(order_dateget)}":
        serial_number = int(checkaddtime[12:])+1
        serial_number = '00000'+str(serial_number)
        if len(serial_number) != 6:
          serial_number = serial_number[-6:]
      else:
        serial_number = '000001'
      query4 = f"""
        INSERT INTO Order_information (訂單編號,會員_LINE_ID,電話,訂單狀態未取已取,訂單成立時間)
        VALUES ( 'cart{order_dateget}{serial_number}','{userid}','add','dd' ,'{formatted_datetimeget}');
        """
      cursor.execute(query4)
      conn.commit()
  member[userid] = 'yy'


#-------------------查詢預購商品列表----------------------
def preorder_list():
  conn = lineboterp.db['conn']
  cursor = lineboterp.db['cursor']
  query = """
          SELECT 商品ID, 商品名稱, 現預購商品, 商品圖片, 商品簡介, 
                商品單位, 售出單價, 售出單價2, 預購數量限制_倍數, 
                預購截止時間 
          FROM Product_information 
          WHERE 現預購商品='預購';"""
  
  #錯誤重新執行最大3次
  max_retries = 3  # 最大重試次數
  retry_count = 0  # 初始化重試計數
  while retry_count<max_retries:
    try:
      cursor.execute(query)
      result = cursor.fetchall()
      break
    except mysql.connector.Error as e:
      retry_count += 1 #重試次數累加

  if result != []:
    listbuynow = result
  else:
    listbuynow = "找不到符合條件的資料。"
  return listbuynow
#-------------------查詢現購商品列表----------------------
def buynow_list():
  conn = lineboterp.db['conn']
  cursor = lineboterp.db['cursor']
  query = """
          SELECT 商品ID,商品名稱,現預購商品,商品圖片,商品簡介,
                  商品單位,售出單價,售出單價2,庫存數量 
          FROM Product_information 
          WHERE 現預購商品='現購' and 庫存數量>0;"""
  #錯誤重新執行最大3次
  max_retries = 3  # 最大重試次數
  retry_count = 0  # 初始化重試計數
  while retry_count<max_retries:
    try:
      cursor.execute(query)
      result = cursor.fetchall()
      break
    except mysql.connector.Error as e:
      retry_count += 1 #重試次數累加

  if result != []:
    listpreorder = result
  else:
    listpreorder = "找不到符合條件的資料。"
  return listpreorder

#查詢資料SELECT
def test_datasearch():
  #測試讀取資料庫願望清單(所有)
  conn = lineboterp.db['conn']
  cursor = lineboterp.db['cursor']
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
  testmsg += "(end)"
  return testmsg
#-------------------訂單成立----------------------
def order_create():
  userid = lineboterp.user_id
  orderall = lineboterp.orderall[userid]
  phonenum = lineboterp.storage[userid+'phonenum']
  conn = lineboterp.db['conn']
  cursor = lineboterp.db['cursor']
  timeget = time()
  formatted_datetimeget = timeget['formatted_datetime']
  order_dateget = timeget['order_date']
  establishment_message = '' #訂單檢查回傳訊息

  query2 = f"""
          SELECT 訂單編號, 會員_LINE_ID ,訂單成立時間
          FROM Order_information 
          WHERE 訂單編號 like'order%' and 訂單成立時間 <= '{formatted_datetimeget}'
          ORDER BY 訂單成立時間 DESC , 訂單編號 DESC;""" #訂單資料檢查
  cursor.execute(query2)
  order_result = cursor.fetchall()

  if order_result == []:
    serial_number = '00001'
    order_details,establishmentget = order_detail(serial_number,conn,cursor)
    establishment_message = establishmentget
    query3_1 = f"""
          INSERT INTO Order_information (訂單編號,會員_LINE_ID,電話,訂單成立時間,訂單狀態未取已取)
          VALUES ('order{order_dateget}{serial_number}','{userid}','{phonenum}', '{formatted_datetimeget}','未取');
          """
    cursor.execute(query3_1)
    conn.commit()
    query3_2 = f"""
          INSERT INTO order_details (訂單編號,商品ID,訂購數量,商品小計)
          VALUES {order_details};
          """
    cursor.execute(query3_2)
    conn.commit()
    query3_3 = f"""
          UPDATE Order_information
          SET 總額 = (
              SELECT SUM(商品小計) AS 小計
              FROM order_details
              WHERE 訂單編號 = 'order{order_dateget}{serial_number}'
          )
          WHERE 訂單編號 = 'order{order_dateget}{serial_number}';
          """
    cursor.execute(query3_3)
    conn.commit()
    establishment_message = 'ok'
    query4_1 = f"""
              SELECT 訂單編號,商品名稱,現預購商品, 訂購數量, 商品小計, 商品單位  
              FROM order_details Natural Join Product_information 
              Where 訂單編號 = 'order{order_dateget}{serial_number}';""" #回傳資訊
    cursor.execute(query4_1)
    orderinfo = cursor.fetchall()
  else:
    checkaddtime = order_result[0][0]#取得最新一筆訂單序號
    if checkaddtime[5:13] == f"{str(order_dateget)}":
      serial_number = int(checkaddtime[13:])+1
      serial_number = '0000'+str(serial_number)
      if len(serial_number) != 5:
        serial_number = serial_number[-5:]
    else:
      serial_number = '00001'
    order_details, establishmentget = order_detail(serial_number,conn,cursor)
    establishment_message = establishmentget
    addorder = f"""
          INSERT INTO Order_information (訂單編號,會員_LINE_ID,電話,訂單成立時間,訂單狀態未取已取)
          VALUES ('order{order_dateget}{serial_number}','{userid}','{phonenum}', '{formatted_datetimeget}','未取');
          """
    cursor.execute(addorder)
    conn.commit()
    addorderdetails = f"""
          INSERT INTO order_details (訂單編號,商品ID,訂購數量,商品小計)
          VALUES {order_details};
          """
    cursor.execute(addorderdetails)
    conn.commit()
    addtotalcost = f"""
          UPDATE Order_information
          SET 總額 = (
              SELECT SUM(商品小計) AS 小計
              FROM order_details
              WHERE 訂單編號 = 'order{order_dateget}{serial_number}'
          )
          WHERE 訂單編號 = 'order{order_dateget}{serial_number}';
          """
    cursor.execute(addtotalcost)
    conn.commit()
    establishment_message = 'ok'
    query4_2 = f"""
              SELECT 訂單編號,商品名稱,現預購商品, 訂購數量, 商品小計, 商品單位  
              FROM order_details Natural Join Product_information 
              Where 訂單編號 = 'order{order_dateget}{serial_number}';""" #回傳資訊
    cursor.execute(query4_2)
    orderinfo = cursor.fetchall()
  return orderinfo, establishment_message

#檢查庫存等動作(單筆)
def order_detail(serial_number,conn,cursor):
  userid = lineboterp.user_id
  orderall = lineboterp.orderall[userid]
  timeget = time()
  order_dateget = timeget['order_date']
  order_details = ''
  establishment_message = ''
  
  query = f"select 現預購商品,庫存數量,售出單價2 from Product_information where 商品ID = '{orderall[0]}'"
  cursor.execute(query)
  inventory_result = cursor.fetchall()
  if inventory_result != []:
    for row in inventory_result:
      sort = row[0] #現預購商品
      inventory = row[1] #庫存數量
      price2 = row[2] #售出單價2
      if sort != '預購':
        if int(orderall[1])<= int(inventory):#庫存檢查
          if int(orderall[1]) >= 2:
            if price2 is not None:
              order_details += f"('order{order_dateget}{serial_number}','{orderall[0]}','{str(orderall[1])}', (select 售出單價2 from Product_information where 商品ID = '{orderall[0]}')*{orderall[1]})"
            else:
              order_details += f"('order{order_dateget}{serial_number}','{orderall[0]}','{str(orderall[1])}', (select 售出單價 from Product_information where 商品ID = '{orderall[0]}')*{orderall[1]})"
          else:
            order_details += f"('order{order_dateget}{serial_number}','{orderall[0]}','{str(orderall[1])}', (select 售出單價 from Product_information where 商品ID = '{orderall[0]}')*{orderall[1]})"
        else:
          establishment_message = f"商品id：{orderall[0]},訂購數量：{str(orderall[1])},庫存剩餘數量不足！"
        query1 =f"""
                UPDATE Product_information
                SET 庫存數量 = '{str(int(inventory)-int(orderall[1]))}'
                WHERE 商品ID = '{orderall[0]}'
                """
        cursor.execute(query1)
        conn.commit()
      else:
        if int(orderall[1]) >= 2:
          if price2 is not None:
            order_details += f"('order{order_dateget}{serial_number}','{orderall[0]}','{str(orderall[1])}', (select 售出單價2 from Product_information where 商品ID = '{orderall[0]}')*{orderall[1]})"
          else:
            order_details += f"('order{order_dateget}{serial_number}','{orderall[0]}','{str(orderall[1])}', (select 售出單價 from Product_information where 商品ID = '{orderall[0]}')*{orderall[1]})"
        else: 
          order_details += f"('order{order_dateget}{serial_number}','{orderall[0]}','{str(orderall[1])}', (select 售出單價 from Product_information where 商品ID = '{orderall[0]}')*{orderall[1]})"
  else:
    establishment_message = '資料庫查無此商品資料'
  return order_details,establishment_message

#預購倍數查詢
def multiplesearch(product_id):
  cursor = lineboterp.db['cursor']
  query = f"""
    select 預購數量限制_倍數 
    from Product_information 
    where 現預購商品 = '預購' and 商品ID = '{product_id}'
    """
  cursor.execute(query)
  result = cursor.fetchall()
  if result == []:
    multiple = 1 #預設倍數
  else:
    for i in result:
      multiple = int(i[0]) #查詢倍數
  return multiple

#商品單位查詢
def unitsearch(product_id):
  cursor = lineboterp.db['cursor']
  query = f"""
    select 商品單位 
    from Product_information 
    where 商品ID = '{product_id}'
    """
  cursor.execute(query)
  result = cursor.fetchall()
  if result == []:
    unit = '無'
  else:
    for i in result:
      unit = i[0] #單位
  return unit

#單獨庫存查詢
def stock(pid,num):
  cursor = lineboterp.db['cursor']
  query = f"select 庫存數量 from Product_information where 商品ID = '{pid}'"
  cursor.execute(query)
  inventory_result = cursor.fetchall()
  if inventory_result != []:
    inventory = inventory_result[0][0] #庫存數量
    if inventory > 0:
      if num <=inventory:
        checkstock = 'ok'
        renum = num
        order = 'ok'#購物車訂單建立用
      else:
        checkstock = 'ok'
        renum = inventory
        order = 'no'
    else:
      checkstock = 'no'
      renum = 0
      order = 'no'
  return checkstock,renum,order
#-------------------未取訂單查詢(100筆)----------------------
def ordertoplist():
  userid = lineboterp.user_id
  conn = lineboterp.db['conn']
  cursor = lineboterp.db['cursor']
  query = f"""
    select 訂單編號,總額,訂單成立時間
    from `Order_information` 
    where 會員_LINE_ID = '{userid}' and 訂單狀態未取已取 = '未取'
    order by 訂單成立時間 desc
    limit 100 offset 0
    """#下一頁加100改offset(目前暫無考慮)
  cursor.execute(query)
  result = cursor.fetchall()
  if result == []:
    result = '找不到符合條件的資料。'
  return result
#-------------------歷史訂單查詢(100筆)----------------------
def ordertopalllist():
  userid = lineboterp.user_id
  conn = lineboterp.db['conn']
  cursor = lineboterp.db['cursor']
  query = f"""
        select 訂單編號,總額,訂單成立時間,訂單狀態未取已取,取貨完成時間
        from `Order_information`
        where 會員_LINE_ID = '{userid}' and 訂單狀態未取已取 <> '未取' and 訂單編號 not like 'cart%'
        order by 訂單成立時間 desc
        limit 100 offset 0
        """#下一頁加100改offset(目前暫無考慮)
  cursor.execute(query)
  result = cursor.fetchall()
  if result == []:
    result = '找不到符合條件的資料。'
  return result
#-------------------訂單詳細資料------------------------
def orderdt():
  userid = lineboterp.user_id
  ordersearch = lineboterp.orderall[userid+'dt']
  conn = lineboterp.db['conn']
  cursor = lineboterp.db['cursor']
  query = f"""
          SELECT
            Order_information.訂單編號,
            Order_information.電話,
            Order_information.訂單狀態未取已取,
            Product_information.商品ID,
            Product_information.商品名稱,
            Product_information.商品單位,
            order_details.訂購數量,
            order_details.商品小計,
            Order_information.總額,
            Order_information.訂單成立時間,
            Order_information.取貨完成時間
          FROM
            Order_information
          JOIN
            order_details ON Order_information.訂單編號 = order_details.訂單編號
          JOIN
            Product_information ON order_details.商品ID = Product_information.商品ID
          WHERE Order_information.訂單編號 = '{ordersearch}' ;
          """
  cursor.execute(query)
  result = cursor.fetchall()
  if result == []:
    result = '找不到符合條件的資料。'
  return result
#-------------------購物車資料查詢----------------------
def cartsearch():
  userid = lineboterp.user_id
  cursor = lineboterp.db['cursor']
  query = f"""
    select 訂單編號, 商品ID, 商品名稱, 訂購數量, 商品單位, 商品小計
    from order_details natural join Product_information
    where 訂單編號 = (
    select 訂單編號
    from Order_information
    where 會員_LINE_ID = '{userid}' and 訂單編號 like 'cart%')
    """
  cursor.execute(query)
  result = cursor.fetchall()
  if result == []:
    result = '資料庫搜尋不到'
  return result
#-------------------購物車單一商品小計查詢----------------------
def cartsubtotal(pid):
  userid = lineboterp.user_id
  cursor = lineboterp.db['cursor']
  query = f"""
    select 商品小計
    from order_details
    where 訂單編號 = (
    select 訂單編號
    from Order_information
    where 會員_LINE_ID = '{userid}' and 訂單編號 like 'cart%') and 商品ID = '{pid}'
    """
  cursor.execute(query)
  result = cursor.fetchall()
  result = result[0][0]
  return result
#-------------------購物車資料新增----------------------
def cartadd(id,product_id,num):
  try:
    conn = lineboterp.db['conn']
    cursor = lineboterp.db['cursor']
    query = f"select 現預購商品,庫存數量,售出單價2 from Product_information where 商品ID = '{product_id}'"
    cursor.execute(query)
    inventory_result = cursor.fetchall()
    if inventory_result != []:
      if inventory_result[0][2] is not None:
        if num >= 2 :
          query1 =f"""
                  INSERT INTO order_details (訂單編號,商品ID,訂購數量,商品小計)
                  VALUES ((select 訂單編號 from Order_information where 會員_LINE_ID = '{id}' and 訂單編號 like 'cart%'),
                  '{product_id}','{num}',(select 售出單價2 from Product_information where 商品ID = '{product_id}')*{num});
                  """
        else:
          query1 =f"""
                  INSERT INTO order_details (訂單編號,商品ID,訂購數量,商品小計)
                  VALUES ((select 訂單編號 from Order_information where 會員_LINE_ID = '{id}' and 訂單編號 like 'cart%'),
                  '{product_id}','{num}',(select 售出單價 from Product_information where 商品ID = '{product_id}')*{num});
                  """
      else:
        query1 =f"""
                  INSERT INTO order_details (訂單編號,商品ID,訂購數量,商品小計)
                  VALUES ((select 訂單編號 from Order_information where 會員_LINE_ID = '{id}' and 訂單編號 like 'cart%'),
                  '{product_id}','{num}',(select 售出單價 from Product_information where 商品ID = '{product_id}')*{num});
                  """
      cursor.execute(query1)
      conn.commit()
      text = 'ok'
    else:
      text = 'Null'
  except Exception as e: #例外處理
      conn.rollback()  # 撤銷操作恢復到操作前的狀態
      #text = f'Commit failed: {str(e)}'
      text = 'no'
      state = lineboterp.user_state
      state[id] = 'normal' #結束流程將user_state轉換預設狀態
  return text
#-------------------購物車單商品數量修改----------------------
def revise(id,product_id,num):
  try:
    conn = lineboterp.db['conn']
    cursor = lineboterp.db['cursor']
    query = f"select 現預購商品,庫存數量,售出單價2 from Product_information where 商品ID = '{product_id}'"
    cursor.execute(query)
    inventory_result = cursor.fetchall()
    if inventory_result != []:
      if inventory_result[0][2] is not None:
        if num >= 2 :
          query1 = f"""
              UPDATE order_details
              SET 訂購數量 = '{num}', 商品小計 = (select 售出單價2 from Product_information where 商品ID = '{product_id}')*{num}
              WHERE 訂單編號 = (
              select 訂單編號
              from Order_information
              where 會員_LINE_ID = '{id}' and 訂單編號 like 'cart%') and 商品ID = '{product_id}';
              """
        else:
          query1 = f"""
              UPDATE order_details
              SET 訂購數量 = '{num}', 商品小計 = (select 售出單價 from Product_information where 商品ID = '{product_id}')*{num}
              WHERE 訂單編號 = (
              select 訂單編號
              from Order_information
              where 會員_LINE_ID = '{id}' and 訂單編號 like 'cart%') and 商品ID = '{product_id}';
              """
      else:
        query1 = f"""
              UPDATE order_details
              SET 訂購數量 = '{num}', 商品小計 = (select 售出單價 from Product_information where 商品ID = '{product_id}')*{num}
              WHERE 訂單編號 = (
              select 訂單編號
              from Order_information
              where 會員_LINE_ID = '{id}' and 訂單編號 like 'cart%') and 商品ID = '{product_id}';
              """
      cursor.execute(query1)
      conn.commit()
      text = 'ok'
    else:
      text = 'Null'
  except Exception as e: #例外處理
      conn.rollback()  # 撤銷操作恢復到操作前的狀態
      #text = f'Commit failed: {str(e)}'
      text = 'no'
  return text
#-------------------修改購物車清單----------------------
def removecart(user_id, product_id):
    try:
      conn = lineboterp.db['conn']
      cursor = lineboterp.db['cursor']
      query = f"""
              DELETE FROM order_details 
              WHERE 訂單編號 = (
              select 訂單編號
              from Order_information
              where 會員_LINE_ID = '{user_id}' and 訂單編號 like 'cart%') and 商品ID = '{product_id}'
              """
      cursor.execute(query)
      conn.commit()
      text = 'ok'
    except Exception as e: #例外處理
      conn.rollback()  # 撤銷操作恢復到操作前的狀態
      #text = f'Commit failed: {str(e)}'
      text = 'no'
    return text
#-------------------購物車訂單建立----------------------
def cartordergo(phonenum):
  userid = lineboterp.user_id
  conn = lineboterp.db['conn']
  cursor = lineboterp.db['cursor']
  timeget = time()
  formatted_datetimeget = timeget['formatted_datetime']
  order_dateget = timeget['order_date']
  stockcheck = 'ok'#預設庫存檢查無誤
  establishment_message = '' #訂單檢查回傳訊息
  
  dblistcart = cartsearch()#購物車所有查詢(訂單編號, 商品ID, 商品名稱, 訂購數量, 商品單位, 商品小計)
  for totallist in dblistcart:
    pid = totallist[1]#商品ID
    num = totallist[3]#訂購數量
    checkstock,renum,order = stock(pid,num) #使用order即可=='ok'
    if order != 'ok':
      stockcheck = 'no'#庫存檢查錯誤
      establishment_message += f"商品名稱：{totallist[3]}，訂單建立庫存檢查不足！\n"

  if stockcheck == 'ok':#庫存無誤執行建立訂單流程
    query2 = f"""
            SELECT 訂單編號, 會員_LINE_ID ,訂單成立時間
            FROM Order_information 
            WHERE 訂單編號 like'order%' and 訂單成立時間 <= '{formatted_datetimeget}'
            ORDER BY 訂單成立時間 DESC , 訂單編號 DESC;""" #訂單資料檢查
    cursor.execute(query2)
    order_result = cursor.fetchall()

    if order_result == []:
      serial_number = '00001'
      query3_1 = f"""
            INSERT INTO Order_information (訂單編號,會員_LINE_ID,電話,訂單成立時間,訂單狀態未取已取)
            VALUES ('order{order_dateget}{serial_number}','{userid}','{phonenum}', '{formatted_datetimeget}','未取');
            """
      cursor.execute(query3_1)
      conn.commit()#建立訂單資訊

      query3_2 = f"""
            UPDATE order_details
            SET 訂單編號 = 'order{order_dateget}{serial_number}'
            WHERE 訂單編號 = (
            select 訂單編號 
            from Order_information 
            where 會員_LINE_ID = '{userid}' and 訂單編號 like 'cart%');
            """#將購物車編號轉換訂單編號
      cursor.execute(query3_2)
      conn.commit()
      query3_3 = f"""
            UPDATE Order_information
            SET 總額 = (
                SELECT SUM(商品小計) AS 小計
                FROM order_details
                WHERE 訂單編號 = 'order{order_dateget}{serial_number}'
            )
            WHERE 訂單編號 = 'order{order_dateget}{serial_number}';
            """#訂單資訊總額計算
      cursor.execute(query3_3)
      conn.commit()
      establishment_message = 'ok'
      query4_1 = f"""
                SELECT 訂單編號,商品名稱,現預購商品, 訂購數量, 商品小計, 商品單位  
                FROM order_details Natural Join Product_information 
                Where 訂單編號 = 'order{order_dateget}{serial_number}';""" #回傳資訊
      cursor.execute(query4_1)
      orderinfo = cursor.fetchall()
    else:
      checkaddtime = order_result[0][0]#取得最新一筆訂單序號
      if checkaddtime[5:13] == f"{str(order_dateget)}":
        serial_number = int(checkaddtime[13:])+1
        serial_number = '0000'+str(serial_number)
        if len(serial_number) != 5:
          serial_number = serial_number[-5:]
      else:
        serial_number = '00001'
      addorder = f"""
            INSERT INTO Order_information (訂單編號,會員_LINE_ID,電話,訂單成立時間,訂單狀態未取已取)
            VALUES ('order{order_dateget}{serial_number}','{userid}','{phonenum}', '{formatted_datetimeget}','未取');
            """
      cursor.execute(addorder)
      conn.commit()
      addorderdetails = f"""
            UPDATE order_details
            SET 訂單編號 = 'order{order_dateget}{serial_number}'
            WHERE 訂單編號 = (
            select 訂單編號 
            from Order_information 
            where 會員_LINE_ID = '{userid}' and 訂單編號 like 'cart%');
            """#將購物車編號轉換訂單編號
      cursor.execute(addorderdetails)
      conn.commit()
      addtotalcost = f"""
            UPDATE Order_information
            SET 總額 = (
                SELECT SUM(商品小計) AS 小計
                FROM order_details
                WHERE 訂單編號 = 'order{order_dateget}{serial_number}'
            )
            WHERE 訂單編號 = 'order{order_dateget}{serial_number}';
            """
      cursor.execute(addtotalcost)
      conn.commit()
      establishment_message = 'ok'
      query4_2 = f"""
                SELECT 訂單編號,商品名稱,現預購商品, 訂購數量, 商品小計, 商品單位  
                FROM order_details Natural Join Product_information 
                Where 訂單編號 = 'order{order_dateget}{serial_number}';""" #回傳資訊
      cursor.execute(query4_2)
      orderinfo = cursor.fetchall()
  return orderinfo, establishment_message

#-------------------修改資料UPDATE----------------------
def test_dataUPDATE():
  return 

#-------------------圖片取得並發送----------------------
def imagesent():
    conn = lineboterp.db['conn']
    cursor = lineboterp.db['cursor']
    img = []
    send = []
    #query = "SELECT 商品名稱, 商品圖片 FROM Product_information LIMIT 1 OFFSET 0;"#0開始1筆
    query = "SELECT 商品名稱, 商品圖片 FROM Product_information LIMIT 2 OFFSET 0;"
    cursor.execute(query)
    result = cursor.fetchall()
    
    if result != []:
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

