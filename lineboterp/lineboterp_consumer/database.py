import mysql.connector
from mysql.connector import errorcode
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *

#安裝 Python 的 MySQL 連接器及其相依性>pip install mysql-connector-python
# Obtain connection string information from the portal

def databasetest():
  config = {
  'host':'140.131.114.242',
  'user':'112405',
  'password':'!mdEe24@5',
  'database':'112-112405',
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
  return {'databasetest_msg': databasetest_msg, 'conn':conn, 'cursor':cursor}

def test_datasearch():
  #測試讀取資料庫願望清單(所有)
  implement = databasetest()
  conn = implement['conn']
  cursor = implement['cursor']
  query = "SELECT * FROM wishlist;"
  cursor.execute(query)
  result = cursor.fetchall()
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
  # 關閉游標與連線
  testmsg += "(end)"
  cursor.close()
  conn.close()
  return testmsg