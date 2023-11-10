#應該是報表
from linebot import LineBotApi, WebhookHandler
# 載入對應的函式庫
from linebot.models import *
line_bot_api = LineBotApi('')
# 剛剛 Flex Message 的 JSON 檔案就貼在下方
user_ids = ''
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta
import pyodbc
import matplotlib.pyplot as plt
import json
import time
import string #字符串處理相關的工具
import pyimgur, os
import random
#-------------------------------
# 建立連接字串
conn_str = {
}

try:
    # 建立連接
    cnxn = mysql.connector.connect(**conn_str)

    # 連接成功
    print("連線成功！")

except pyodbc.Error as err:
    # 連接失敗
    print(f"連線失敗：{err}")
cursor = cnxn.cursor()
query = """
    SELECT 商品名稱, 訂購數量, 進貨單價
    FROM Statistics_Data
    WHERE 年月='2023-07';
    """

cursor.execute(query)
result = cursor.fetchall()
cursor.close()
cnxn.close()

#-------------------------------
db_report = result
show = []
if db_report=="找不到符合條件的資料。":
  show = TextSendMessage(text=db_report)
else:
  title = '2023-07' #標題-年月
  product_name = [] #x軸-商品名
  purchase_cost = [] #y軸-成本

  for i in range(len(db_report)):
          product_name.append(db_report[i][0])
          purchase_cost.append(db_report[i][1]*db_report[i][2])
#--------------------------月成本圓餅圖---------------------------------------
def func(s,d):
  t = int(round(s/100.*sum(d)))     # 透過百分比反推原本的數值
  return f'{s:.1f}%\n( {t}元 )'

plt.pie(purchase_cost,
        radius=1.5,
        labels=product_name,
        autopct=lambda i: func(i,purchase_cost), #lamda 匿名, 呼叫函式
        pctdistance=0.8,
        wedgeprops={'linewidth':3,'edgecolor':'w'}) # 繪製每個扇形的外框
plt.savefig('/content/drive/MyDrive/Colab Notebooks/test.png', #存path
            transparent=False, #透明度:否
            bbox_inches='tight',
            pad_inches=1)
plt.show()
