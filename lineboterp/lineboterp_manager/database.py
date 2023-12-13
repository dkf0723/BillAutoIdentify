import mysql.connector
from datetime import datetime, timedelta
from mysql.connector import errorcode
# 載入對應的函式庫
from linebot.models import TextSendMessage,ImageSendMessage
from relevant_information import imgurinfo
import os, pyimgur, glob
import manager
import time


#-------------------取得現在時間----------------------
def gettime():
  current_datetime = datetime.now()# 取得當前的日期和時間
  modified_datetime = current_datetime + timedelta(hours=8)#時區轉換+8
  formatted_millisecond = modified_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
  formatted_datetime = modified_datetime.strftime('%Y-%m-%d %H:%M:%S')# 格式化日期和時間，不包含毫秒部分
  formatted_date = modified_datetime.strftime('%Y-%m-%d')#格式化日期
  order_date = modified_datetime.strftime('%Y%m%d')#格式化日期，清除-
  formatted_datetime2 = modified_datetime.strftime('%Y-%m-%dT%H:%M')# 給日期選擇器的-蓉
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
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
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
      except:#except mysql.connector.Error as mysql_err:
        databasetest_msg = '主要1的重新連線(3分鐘)關閉連線錯誤！'
    db['databasetest_msg'] = databasetest_msg
    db['databaseup'] = formatted_datetime
    db['databasenext'] = new_formatted_datetime
    db['conn'] = conn
  elif serial_number == 4:
    new_formatted_datetime = next_conn_time(formatted_datetime, 4)#取得下次執行時間
    if db['conn1'] is not None:
      try:
        db['conn1'].close()
      except:#except mysql.connector.Error as mysql_err:
        databasetest_msg = '備用1的重新連線(5分鐘)關閉連線錯誤！'
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
    modified_add = next_time(check, check1, nowtime, addhours,'ok')#下次更新分鐘取得

  if serial_number in [2,4]:
    #check1 = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    check1 = [5, 10, 20, 25, 35, 40, 50, 55]
    addhours = []#小時進位分鐘
    for i in range(55,60):#55～59
      addhours.append(i)
    modified_add = next_time(check, check1, nowtime, addhours,'no')#下次更新分鐘取得
  new_formatted_datetime = modified_add.strftime('%Y-%m-%d %H:%M:%S')
  return new_formatted_datetime

#下次更新分鐘取得
def next_time(check, check1,nowtime, addhours,check2):
  if check in addhours:
    modified_add = nowtime + timedelta(hours=1)
    if check2 == 'ok':#3min
      modified_add = modified_add.replace(minute=0)
    else:
      modified_add = modified_add.replace(minute=5)
  else:
    next_minute = min([i for i in check1 if i > check])
    modified_add = nowtime.replace(minute=next_minute)
  return modified_add

#-------------------錯誤重試----------------------
def retry(category,query):#select/notselect
  #indb_pool = manager.db_pool
  block = 0#結束點是1
  stepout = 0 #離開標記
  step = 0 #預設起始
  while block == 0:
    max = 3  # 最大重試次數
    count = 0  # 初始化重試計數
    connobtain = 'ok' #檢查是否取得conn連線資料
    connobtain1 = 'ok'#檢查是否取得conn1連線資料
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
        if count != 2:
          count += 1 #重試次數累加
        else:
          if step == 0:
            connobtain = 'no'
          else:
            connobtain1 = 'no'
        
    count = 0  # 重試次數歸零，用於後面的步驟
    if connobtain == 'ok' or connobtain1 == 'ok':
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
        except:#except mysql.connector.Error as e:
          count += 1 #重試次數累加
          result = [] #錯誤回傳內容
          if count == 2 and step == 1:
            stepout = 1
          time.sleep(1)
      if stepout == 1:#成功取得資料後退出或兩輪都失敗退出迴圈
        cursor.close()#關閉第一輪游標的
        block = 1
    else:
      if stepout == 1 and step == 1:#兩輪都失敗退出迴圈
        cursor.close()#關閉第一輪游標的
        block = 1
        if category == 'select':
          result = []
        else:
          result = 'no'
      if connobtain == 'no' and connobtain1 == 'no':
        block = 1
        if category == 'select':
          result = []
        else:
          result = 'no'
      elif step == 0 and connobtain == 'no':
        step = 1 #conn沒取到進入切換conn1
      elif step == 1 and connobtain1 == 'no':
        step = 0
  return result
#-----------------抓取未有進貨資訊的預購商品列表---------------
def nopur_inf():
  query =f"""SELECT P.商品ID,P.商品名稱,P.商品單位,廠商名,付款方式 
            FROM Product_information AS P LEFT JOIN Purchase_Information AS PI ON P.商品ID = PI.商品ID natural join Manufacturer_Information
            WHERE PI.商品ID IS NULL AND P.現預購商品 = '預購';"""
  category ='select'
  result = retry(category,query)
  if result != [] and len(result) > 0:
    prolist = result
  else:
    prolist = "找不到符合條件的資料。"
  return prolist
############################################
#------------------抓取未有進貨資訊的現購商品列表------------------
def product_ing():
  query = f"""SELECT P.商品ID,P.商品名稱,P.商品單位,廠商名,付款方式 
            FROM Product_information AS P LEFT JOIN Purchase_Information AS PI ON P.商品ID = PI.商品ID natural join Manufacturer_Information
            WHERE PI.商品ID IS NULL AND P.現預購商品 = '現購';"""
  category ='select'
  result = retry(category,query)
  if result != [] and len(result) > 0:
    prolist2 = result
  else:
    prolist2 = "找不到符合條件的資料。"
  return prolist2
#------------------新增預購進貨資訊、狀態更新------------------------
def newtopur_inf(purchase_pid,purchase_num,purchase_cost,purchase_unit,purchase_time,give_money,money_time):
  if money_time != 'NULL':
    change_money_time = f"'{money_time}'"
  else:
    change_money_time = money_time
  query = f"""INSERT INTO Purchase_Information (商品ID,進貨數量, 進貨單價, 商品單位, 進貨狀態, 進貨時間, 匯款金額,匯款時間) 
            VALUES ('{purchase_pid}','{purchase_num}','{purchase_cost}','{purchase_unit}','進貨中','{purchase_time}','{give_money}',{change_money_time});"""
  category ='notselect'
  result1 = retry(category, query)

  query_one = f"UPDATE Product_information SET 現預購商品 = '預購進貨' WHERE 商品ID = '{purchase_pid}';"
  category_one = 'notselect'
  result1 = retry(category_one, query_one)

  order_numbers = []
  query_two = f"SELECT 訂單編號 FROM order_details WHERE 商品ID = '{purchase_pid}'"
  category_two = 'select'
  result = retry(category_two, query_two)

  for row in result:
    order_numbers.append(row[0])

  for order_num in order_numbers:
      query_three = f"UPDATE Order_information SET 訂單狀態未取已取 = '預購進貨' WHERE 訂單編號 = '{order_num}';"
      category_three = 'notselect'
      result1 = retry(category_three, query_three)

  return result1

#--------------------新增現購進貨資訊---------------------
def newingtopur_inf(purchase_pid,purchase_num,purchase_cost,purchase_unit,purchase_time,give_money,money_time):
  if money_time != 'NULL':
    change_money_time = f"'{money_time}'"
  else:
    change_money_time = money_time
  query = f"""INSERT INTO Purchase_Information (商品ID,進貨數量, 進貨單價, 商品單位, 進貨狀態, 進貨時間, 匯款金額,匯款時間) 
            VALUES ('{purchase_pid}','{purchase_num}','{purchase_cost}','{purchase_unit}','進貨中','{purchase_time}','{give_money}',{change_money_time});"""
  category ='notselect'
  result = retry(category, query)
  return result
#---------------------------快速進貨-依廠商查詢所有廠商名稱-------------------------------
def db_quick_purchase_manufacturers():
  query = "SELECT 廠商編號,廠商名 FROM Manufacturer_Information;"
  category ='select'
  result = retry(category,query)
  return result

#-----------------快速進貨->依廠商查詢所有商品的商品ID及商品名稱-----------------
def db_quickmanu_pro(manufacturerR_id):
  query = f"""SELECT Product_information.商品ID, Product_information.商品名稱, Purchase_Information.進貨時間,Product_information.現預購商品,Product_information.商品單位,Manufacturer_Information.付款方式
             FROM Product_information INNER JOIN Purchase_Information ON Product_information.商品ID = Purchase_Information.商品ID 
             INNER JOIN Manufacturer_Information ON Product_information.廠商編號 = Manufacturer_Information.廠商編號 
             WHERE Manufacturer_Information.廠商編號 LIKE '{manufacturerR_id}' AND Purchase_Information.進貨時間 IS NOT NULL;"""
  category ='select'
  result = retry(category,query)
  return result

#------------------快速進貨->依分類查詢所有商品的商品ID及商品名稱-------------------
def db_quick_catepro(selectedr_category):
  query = f"""SELECT Product_information.商品ID, Product_information.商品名稱, Purchase_Information.進貨時間,Product_information.現預購商品,Product_information.商品單位,Manufacturer_Information.付款方式 
              FROM Product_information INNER JOIN Purchase_Information ON Product_information.商品ID = Purchase_Information.商品ID natural join Manufacturer_Information
              WHERE Product_information.商品ID LIKE '{selectedr_category}%' AND Purchase_Information.進貨時間 IS NOT NULL;"""
  category ='select'
  result = retry(category,query)
  return result
#--------------------庫存-查詢所有廠商編號及廠商名-----------------------
def db_stock_manufacturers_name():
  query = "SELECT 廠商編號,廠商名 FROM Manufacturer_Information;"
  category ='select'
  result = retry(category,query)
  return result

#-------------------庫存->選擇此廠商的商品庫存資訊------------------------
def db_stock_manuinf(manufacturerZ_id):
  query = f"SELECT 商品ID,商品名稱,庫存數量,售出單價,售出單價2 FROM Product_information WHERE 廠商編號 = '{manufacturerZ_id}';"
  category ='select'
  result = retry(category,query)
  return result

#-------------------庫存->選擇此類別的商品庫存資訊------------------------
def db_stock_categoryinf(selectedD_category):
  query = f"SELECT 商品ID,商品名稱,庫存數量,售出單價,售出單價2 FROM  Product_information WHERE 商品ID LIKE '{selectedD_category}%';"
  category ='select'
  result = retry(category,query)
  return result

#-------------------進貨狀態-抓取進貨中商品------------------------
def db_puring_pro():
  query = f"SELECT 商品ID,商品名稱,進貨數量,進貨狀態,進貨時間,付款方式,現預購商品 FROM Purchase_Information natural join Product_information natural join Manufacturer_Information WHERE 進貨狀態 ='進貨中';"
  category ='select' 
  result = retry(category,query)
  return result

#-------------------進貨狀態-抓取已到貨商品-------------------------
def db_pured_pro():
  query = f"SELECT 商品ID,商品名稱,進貨數量,進貨狀態,進貨時間,付款方式 FROM Purchase_Information natural join Product_information natural join Manufacturer_Information WHERE 進貨狀態 ='已到貨';"
  category ='select'
  result = retry(category,query)
  return result

#------------------商品已到貨後的狀態改變及庫存數量更動-----------
def puring_trastate(manufacturerV_id,stapro):
  #取得進貨數量
  query_otwo = f"""SELECT 進貨數量 FROM Purchase_Information 
                WHERE 商品ID = '{manufacturerV_id}' and 進貨狀態= '進貨中' 
                order by 進貨時間 desc limit 1;
                """
  category_otwo = 'select'
  result8 = retry(category_otwo, query_otwo)
  if result8 != []:
    #取得庫存數量
    query_othree = f"SELECT 庫存數量 FROM Product_information WHERE 商品ID = '{manufacturerV_id}';"
    category_othree = 'select'
    result9 = retry(category_othree, query_othree)
    if result9 != []:
      if stapro == '現':
        query_oone = f"SELECT 訂單剩餘 FROM Product_information WHERE 商品ID = '{manufacturerV_id}';"
        category_oone = 'select'
        result7 = retry(category_oone, query_oone)
        if result7 != []:
          if result7 != [] and result8 != []:
            if result7[0][0] is None:#訂單剩餘
              sum = int(result8[0][0])#進貨數量
            else:
              sum = int(result7[0][0]) + int(result8[0][0])
            query_two = f"UPDATE Product_information SET 訂單剩餘 = {sum} WHERE 商品ID = '{manufacturerV_id}';"
            category_two = 'notselect' ##消費者
            result2 = retry(category_two, query_two)
            if result2 == 'ok':
              if result9[0][0] is None:#庫存數量
                sum1 = int(result8[0][0])#進貨數量
              else:
                sum1 = int(result9[0][0]) + int(result8[0][0])
              query_three = f"UPDATE Product_information SET 庫存數量 = {sum1} WHERE 商品ID = '{manufacturerV_id}';"
              category_three = 'notselect' ##管理者
              result3 = retry(category_three, query_three)
              if result3 == 'ok':
                result = 'ok'
              else:
                result = '修改庫存數量錯誤'
            else:
              result = '修改訂單剩餘錯誤'
          else:
            result = '提取進貨數量或庫存數量錯誤'
        else:
          result = '訂單剩餘取得有誤'
      ##
      elif stapro == '預':
        if result8 != []:#進貨數量
          queryfour = f"UPDATE Product_information SET 現預購商品 = '預購未取' WHERE 商品ID = '{manufacturerV_id}';"
          categoryfour ='notselect'
          result4 = retry(categoryfour,queryfour)
          if result4 == 'ok':
            if result9[0][0] is None:#庫存數量
              sum2 = int(result8[0][0])
            else:
              sum2 = int(result9[0][0]) + int(result8[0][0])
            query_five = f"UPDATE Product_information SET 庫存數量 = {sum2} WHERE 商品ID = '{manufacturerV_id}';"
            category_five = 'notselect' ##管理者
            result5 = retry(category_five, query_five)
            if result5 == 'ok':
              query_six = f"SELECT 訂單編號 FROM order_details WHERE 商品ID = '{manufacturerV_id}';"
              category_six = 'select'
              result6 = retry(category_six, query_six)
              if result6 != []:
                order_numbers = []
                for row in result6:
                  order_numbers.append(row[0])
                for order_num in order_numbers:
                  query_ten = f"UPDATE Order_information SET 訂單狀態未取已取 = '預購未取' WHERE 訂單編號 = '{order_num}';"
                  category_ten = 'notselect'
                  result10 = retry(category_ten, query_ten)
                if result10 == 'ok':
                  result = 'ok'
                else:
                  result = '修改訂單狀態<預購未取>失敗'
              else:
                result = 'ok'#修改詳細資訊前取得訂單編號錯誤
            else:
              result = '2庫存數量修改錯誤'
          else:
            result = '修改為<預購未取>錯誤'
        else:
          result = '沒有取得進貨數量'
      else:
        result = '找不到「現或預」字'
    else:
      result = '庫存數量取得錯誤'
  else:
    result = '進貨數量取得有誤'

  if result == 'ok':
    querypd = f"UPDATE Purchase_Information SET 進貨狀態 = '已到貨' WHERE 商品ID = '{manufacturerV_id}';"
    categorypd ='notselect' 
    resultpd = retry(categorypd,querypd)
    if resultpd == 'ok':
      resultinfo = 'ok'
    else:
      resultinfo = '修改為<已到貨>錯誤'
  else:
    resultinfo = result
  return resultinfo


def bankpay(manufacturerV_id):
  timeget = gettime()['formatted_datetime']
  queryfive = f"""
              UPDATE Purchase_Information
              SET 匯款時間 = '{timeget}' 
              WHERE 商品ID = '{manufacturerV_id}' AND 進貨狀態 = '進貨中';
              """
  categoryfive ='notselect'
  result = retry(categoryfive,queryfive)
  return result
  

#-----------------點擊要進貨時的商品及廠商資訊-----------------
def getmanuinf():
  id = manager.user_id
  pid = manager.storage[id + 'purchase_pid']
  message_storage = manager.storage
  query = f"""select 商品ID, 現預購商品, 付款方式, 行庫名, 行庫代號, 匯款帳號
              from Product_information natural join Manufacturer_Information
              where 商品ID = '{pid}';
              """
  category ='select'
  message_storage[id + 'dbmanuinf'] = retry(category,query)

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
  return {'imagetitle':imagetitle,'imagelink':imagelink}

#######廠商管理開始
#-------------------廠商管理建立----------------------
def manufacturer(name,principal,localcalls,phonenum,Payment,bankid,bankname,bankaccount):
  timeget = gettime()
  formatted_datetimeget = timeget['formatted_datetime']

  query = """SELECT 廠商編號 FROM Manufacturer_Information order by 建立時間 desc limit 1;"""
  category ='select' #重試類別select/notselect
  manufacturernum_result = retry(category,query)

  if manufacturernum_result == []:
    addnum = '000001'
  else:
    add = int(str(manufacturernum_result[0][0])[12:])+1
    addnum = '00000' + str(add)
  if len(addnum) != 6:
    addnum = addnum[-6:]

  query = f"""
        INSERT INTO Manufacturer_Information (廠商編號,廠商名,負責或對接人,市話,電話,付款方式,行庫代號,行庫名,匯款帳號,建立時間)
        VALUES ('manufacturer{addnum}','{name}','{principal}','{localcalls}','{phonenum}','{Payment}','{bankid}','{bankname}','{bankaccount}','{formatted_datetimeget}');
        """
  category ='notselect' #重試類別select/notselect
  result = retry(category,query)
  if result == 'ok':
    check = 'ok'
    result = Manufacturer_single(f"manufacturer{addnum}",0)
    info = result
  else:
    check = 'no'
    info = ''
  return check,info

#-------------------單獨查詢廠商----------------------
def Manufacturer_single(manufacturer_id,choose):
  id = manager.user_id
  message_storage = manager.storage
  query = f"""
        SELECT 廠商編號, 廠商名, 負責或對接人, 市話, 電話, 付款方式, 行庫名, 行庫代號, 匯款帳號
        FROM Manufacturer_Information
        where 廠商編號 = '{manufacturer_id}';
        """
  category ='select' #重試類別select/notselect
  result = retry(category,query)

  #修改廠商資訊進入做的暫存
  if choose == 1:
    if result != []:
      for storage in result:
        message_storage[id+'manufacturer_list_check'] = 'ok'
        message_storage[id+'manufacturer_list_name'] = storage[1]#廠商名
        message_storage[id+'manufacturer_list_principal'] = storage[2]#負責或對接人
        message_storage[id+'manufacturer_list_localcalls'] = storage[3]#市話
        message_storage[id+'manufacturer_list_phone'] = storage[4]#電話
        message_storage[id+'manufacturer_list_payment'] = storage[5]#付款方式
        message_storage[id+'manufacturer_list_bankname'] = storage[6]#行庫名
        message_storage[id+'manufacturer_list_bankid'] = storage[7]#行庫代號
        message_storage[id+'manufacturer_list_bankaccount'] = storage[8]#匯款帳號
    else:
      message_storage[id+'manufacturer_list_check'] = 'no'
  return result
#-------------------廠商列表----------------------
def Manufacturer():
  query = f"""
        SELECT 廠商編號, 廠商名, 負責或對接人, 市話, 電話, 付款方式, 行庫名, 行庫代號, 匯款帳號
        FROM Manufacturer_Information;
        """
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  if result != []:
    manufacturer_list = result
  else:
    manufacturer_list = 'no'
  return manufacturer_list

#-------------------修改廠商資料----------------------
def Manufacturer_infochange(editfield,changeinfo):
  #editfield=廠商編號, 廠商名, 負責或對接人, 市話, 電話, 付款方式, 行庫名, 行庫代號, 匯款帳號
  #changeinfo=修改的內容
  id = manager.user_id
  message_storage = manager.storage
  manufacturer_id = message_storage[id+'manufacturer_list_id']
  query = f"""
            UPDATE Manufacturer_Information
            SET {editfield} = '{changeinfo}'
            WHERE 廠商編號 = '{manufacturer_id}';
            """
  category ='notselect' #重試類別select/notselect
  result = retry(category,query)
  return result
#---------------------廠商管理結束--------------------
#-------------------取出預購名單---------------------------------海碧
def preorder_list():
  query = f"""
          SELECT 訂單編號, 會員_LINE_ID, 電話, 訂單成立時間, 總額
          FROM Order_information
			    WHERE 訂單狀態未取已取='預購';"""
  category ='select'
  result = retry(category,query)
  return result
 
#-------------------取出未取名單---------------------------------
def order_list():
  query = f"""
          SELECT 訂單編號, 會員_LINE_ID, 電話, 訂單成立時間, 總額
          FROM Order_information
			    WHERE 訂單狀態未取已取='預購未取' or 訂單狀態未取已取='現購未取'
          limit 100 offset 0;"""
  category ='select'
  result = retry(category,query)
  return result
#-------------------訂單詳細資料------------------------
def orderdt():
  userid = manager.user_id
  ordersearch = manager.orderall[userid+'dt'] #本是使用者的ID
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
  category ='select'
  result = retry(category,query)
  return result
#-------------------取出庫存---------------------------------
def inquiry_list():
  query = """
    SELECT 商品名稱, 商品ID, 庫存數量, 現預購商品, 商品單位, 付款方式
    FROM Product_information natural join Manufacturer_Information 
    WHERE 現預購商品='現購' AND 庫存數量 IS NOT NULL AND 庫存數量<=20
    order by 庫存數量 asc;"""
  category ='select'
  result = retry(category,query)
  return result
#-----------------------------------------------------海碧

#---------------蓉的資料庫語法--------------------------#
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
  query = f"""SELECT 商品ID,商品名稱,商品圖片,庫存數量,商品單位,進貨單價,售出單價,現預購商品 
              FROM Product_information NATURAL JOIN Purchase_Information 
              WHERE {test1} 
              order by 進貨時間 desc
              limit 1;"""
  category = 'select'  # 重試類別 select/notselect
  result = retry(category, query)
  return result
#-------------分類下所有商品列表------------
def db_categoryate(selected_category):
  query = f"""WITH LatestPurchase AS (
                SELECT
                  pi.商品ID,
                  MAX(pi.進貨時間) AS 最新進貨時間
                FROM
                  Purchase_Information pi
                GROUP BY
                  pi.商品ID
              )
              SELECT
                p.商品ID,p.商品名稱,p.商品圖片,p.庫存數量,p.商品單位,
                pi.進貨單價,p.售出單價,p.現預購商品
              FROM
                Product_information p
              INNER JOIN
                Purchase_Information pi ON p.商品ID = pi.商品ID
              INNER JOIN
                LatestPurchase lp ON pi.商品ID = lp.商品ID AND pi.進貨時間 = lp.最新進貨時間
              where p.商品ID LIKE '{selected_category}%' and p.現預購商品 <> '現購停售'and p.現預購商品 <> '預購截止'
              order by pi.進貨時間 desc;"""
  category = 'select' #重試類別 select/notselect
  result = retry(category,query)
  return result
#-----------抓取商品資訊----------------------
def db_infotmation(pid):
  query = f"""SELECT 商品名稱,商品簡介,售出單價,售出單價2,預購數量限制_倍數,預購截止時間,商品圖片 
              FROM Product_information 
              WHERE 商品ID = '{pid}';"""
  category = 'select' #重試類別 select/notselect
  result = retry(category,query)
  return result
# ---------------修改商品系列-----------------
def MP_information_modify(field_to_modify, new_value, pid):
    if field_to_modify in ["商品名稱", "商品簡介", "售出單價", "售出單價2", "預購數量限制_倍數","預購截止時間","商品圖片"]:
        query = f"UPDATE Product_information SET {field_to_modify} = '{new_value}' WHERE 商品ID = '{pid}';"
        category = 'notselect' # 重試類別 select/notselect
        result = retry(category, query) # 成功回傳 ok
        return result
    else:
        return "無效欄位名稱" 
#--------------辨識商品狀態進而選擇FM------------
def Product_status():
  user_id = manager.user_id
  pid = manager.product[user_id + 'Product_Modification_Product_id']
  query = f"SELECT 現預購商品,商品名稱,商品ID FROM Product_information WHERE 商品ID = '{pid}';"
  category = 'select'  # 重試類別 select/notselect
  result = retry(category, query)
  if result != []:
    product_status = result[0][0]
  else:
    product_status = '查無'
  return product_status  
#--------------現購FM函數------------------------
def Now_Product(id):
  query = f"""SELECT 商品名稱, 商品簡介, 售出單價, 售出單價2,商品圖片 
              FROM Product_information natural join Purchase_Information 
              WHERE 商品ID = '{id}';"""
  category = 'select'  # 重試類別 select/notselect
  result = retry(category, query)
  return result                        

#--------------預購FM函數------------------------
def Per_Product(id):
  query = f"""SELECT 商品名稱, 商品簡介, 售出單價, 售出單價2,商品圖片,預購數量限制_倍數,預購截止時間 
              FROM Product_information natural join Purchase_Information 
              WHERE 商品ID = '{id}';"""
  category = 'select'  # 重試類別 select/notselect
  result = retry(category, query)
  return result                 

#---------------停售-----------------------------
def stop_time(pid):
  query = f"UPDATE Product_information SET 現預購商品 = '現購停售' WHERE 商品ID = '{pid}';"
  category = 'notselect'  # 重試類別 select/notselect
  result = retry(category, query)
  return result

#-------------------許願清單----------------------
def wisheslistdb():
  query =f"""
          SELECT 商品圖片,商品名稱,會員_LINE_ID,推薦原因,願望建立時間,資料來源
          FROM wishlist
          order by 願望建立時間 desc;
            """
  category ='select' #重試類別select/notselect
  result = retry(category,query)
  if result == []:
    info = '找不到符合條件的資料。'
  else:
    info = result
  return info
#---------------蓉的資料庫語法--------------------------#
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
def updateOrder(id):
  storage = manager.global_Storage
  if storage[id+'order'][:1] == '0':
    query = f"UPDATE Order_information SET 訂單狀態未取已取 = CASE WHEN 訂單狀態未取已取 = '現購未取' THEN '現購已取' WHEN 訂單狀態未取已取 = '預購未取' THEN '預購已取' ELSE 訂單狀態未取已取 END , 取貨完成時間 = '{datetime.now() + timedelta(hours=8)}'  WHERE 電話 = '{storage[id+'order']}' and 訂單狀態未取已取 like '%未取' ;"
    result = retry('notselect', query)
  else : 
    query = f"UPDATE Order_information SET 訂單狀態未取已取 = CASE WHEN 訂單狀態未取已取 = '現購未取' THEN '現購已取' WHEN 訂單狀態未取已取 = '預購未取' THEN '預購已取' ELSE 訂單狀態未取已取 END , 取貨完成時間 = '{datetime.now() + timedelta(hours=8)}'   WHERE 訂單編號 = '{storage[id+'order']}' and 訂單狀態未取已取 like '%未取';"
    # query = f"UPDATE Order_information SET 訂單狀態未取已取 = ''  WHERE 訂單編號 = '{storage[id+'order']} and 訂單狀態未取已取 like '%未取'';"
    result = retry('notselect', query)
  return result

def createProduct(id):
  storage = manager.global_Storage
  if storage[id+'createType'] == 'now':
    pname = storage[id+'pname'][3:]
    category= storage[id+'category'][5:]
    unit= storage[id+'unit'][5:]
    introduction= storage[id+'introduction'][5:]
    unitPrice= storage[id+'unitPrice'][7:]
    unitPrice2= storage[id+'unitPrice2'][8:]
    picture= storage[id+'picture'][5:]
    returnProduct= storage[id+'returnProduct'][6:]
    manufacturerId = storage[id+'manufacturerId']
    num = count(category)
    query = f"INSERT INTO Product_information (商品ID,商品名稱,現預購商品,商品圖片,商品簡介,商品單位,售出單價,商品建立時間,商品可否退換貨,售出單價2,廠商編號) VALUES ('{category+num}','{pname}','現購','{picture}','{introduction}','{unit}','{unitPrice}','{datetime.now() + timedelta(hours=8)}' ,'{returnProduct}', '{unitPrice2}','{manufacturerId}');"
  else :
    pname = storage[id+'pname'][3:]
    category= storage[id+'category'][5:]
    unit= storage[id+'unit'][5:]
    introduction= storage[id+'introduction'][5:]
    unitPrice= storage[id+'unitPrice'][7:]
    unitPrice2= storage[id+'unitPrice2'][8:]
    picture= storage[id+'picture'][5:]
    deadline = storage[id+'deadline'][9:]
    multiple = storage[id+'multiple'][7:]
    manufacturerId = storage[id+'manufacturerId']
    num = count(category)
    query = f"INSERT INTO Product_information (商品ID,商品名稱,現預購商品,商品圖片,商品簡介,商品單位,售出單價,商品建立時間,售出單價2,預購數量限制_倍數,預購截止時間,廠商編號) VALUES ('{category+num}','{pname}','現購','{picture}','{introduction}','{unit}','{unitPrice}','{datetime.now() + timedelta(hours=8)}', '{unitPrice2}','{multiple}','{deadline}','{manufacturerId}');"
  result = retry('notselect', query)
  return result

def count(category):
    query = f"SELECT  商品ID  FROM Product_information   where 商品ID like '{category}%'  order by  商品ID DESC  limit 1;"
    result = retry('select', query)
    if result == []:
      number = 0
    else:
      number = int(result[0][0][-6:])+1
    result_string_formatted = '{:06}'.format(number)
    return result_string_formatted
#--------------------取出報表---------------------------------
def report_query_list(report_type, time_query):
  query = f"""
    SELECT {report_type}
    FROM Statistical_Product
    WHERE 年月 like '{time_query}%';
    """#成本月報表
  result = retry('select', query)
  if result != []:
    img_link = result[0][0]
    image_msg = ImageSendMessage(
                    original_content_url=img_link,  # 圖片原圖
                    preview_image_url=img_link  # 圖片縮圖
                )
  else:
    image_msg = TextSendMessage(text="找不到符合條件的資料。")
  return image_msg
#--------------------繪製月報表----------------------------------
def month_report_list():
  modified_year = formatted_datetime_obj.year # 取年份
  modified_month = formatted_datetime_obj.month #取月份
  int_modified_month = int(modified_month)-1
  query = f"""
    SELECT
            Product_information.商品名稱,
            order_details.訂購數量,
            Purchase_Information.進貨單價,
            order_details.商品小計
          FROM
            Order_information
          JOIN
            order_details ON Order_information.訂單編號 = order_details.訂單編號
          JOIN
            Product_information ON order_details.商品ID = Product_information.商品ID
		  JOIN
			Purchase_Information ON order_details.商品ID = Purchase_Information.商品ID
          WHERE (訂單狀態未取已取='現購已取' OR 訂單狀態未取已取='預購已取') AND 取貨完成時間 like {modified_year}-{int_modified_month}%';;
    """
  result = retry('select', query)
  if result == []:
    report_data = '找不到符合條件的資料。'
  else:
    report_data = result
  return report_data
#--------------------繪製年報表----------------------------------
def year_report_list():
  modified_year = formatted_datetime_obj.year # 取年份
  int_modified_year = int(modified_year)-1
  query = f"""
    SELECT 年月,月成本_值, 月利潤_值
    FROM Statistical_Product
    WHERE 年月 like '{int_modified_year}%' AND 年月 != '{int_modified_year}-99';
    """
  result = retry('select', query)
  if result == []:
    report_data = '找不到符合條件的資料。'
  else:
    report_data = result
  return report_data
#--------------------上傳月報表_圖-------------------------------
def upload_month_report(cost_pie_database_link,profit_pie_database_link,saled_figure_chart_database_link,month_total_cost,month_total_profit):
  modified_year = formatted_datetime_obj.year # 取年份
  modified_month = formatted_datetime_obj.month # 取月份
  year_month = modified_year+modified_month
  query = f"""
    INSERT INTO Statistical_Product (年月,月成本_圖,月利潤_圖,月熱門商品_圖,月成本_值,月利潤_值)
    VALUES ( '{year_month}','{cost_pie_database_link}','{profit_pie_database_link}','{saled_figure_chart_database_link}','{month_total_cost}','{month_total_profit}');
    """
  result = retry('notselect', query)
  if result == []:
    report_data = '找不到符合條件的資料。'
  else:
    report_data = result
  return report_data
#--------------------上傳年報表_圖-------------------------------
def upload_year_report(cost_line_database_link,profit_line_database_link):
  modified_year = formatted_datetime_obj.year # 取年份
  query = f"""
    INSERT INTO Statistical_Product (年月,年成本_圖,年利潤_圖)
    VALUES ( '{modified_year}-99','{cost_line_database_link}','{profit_line_database_link}');
    """
    result = retry('notselect', query)
  if result == []:
    report_data = '找不到符合條件的資料。'
  else:
    report_data = result
  return report_data