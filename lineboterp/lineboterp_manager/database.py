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
  query = "SELECT * FROM member_profile;"
  cursor.execute(query)
  result = cursor.fetchall()
  testmsg = "會員資料讀取內容：\n"
  num = 0
  for row in result:
    # 透過欄位名稱獲取資料
    member = row[0]#'會員_LINE_ID'
    #'會員信賴度'
    time = row[2]#'加入時間'
    member_type = row[3]#'身分別'
    # 在這裡進行資料處理或其他操作
    num += 1
    testmsg += ('第%s筆\n會員LINE_ID:\n%s\n身分別：\n%s\n加入時間：\n%s\n---\n' %(num,member,member_type,time))
  # 關閉游標與連線
  testmsg += "(end)"
  cursor.close()
  conn.close()
  return testmsg