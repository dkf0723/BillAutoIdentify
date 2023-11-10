
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


current_datetime = datetime.now()# 取得當前的日期和時間
modified_datetime = current_datetime + timedelta(hours=8)#時區轉換+8
formatted_datetime = modified_datetime.strftime('%Y-%m-%d %H:%M:%S')# 格式化日期和時間，不包含毫秒部分
formatted_date = modified_datetime.strftime('%Y-%m-%d')#格式化日期
order_date = modified_datetime.strftime('%Y')#格式化日期，清除-

now_time = int(order_date)
report_year = []
year_list = [] #近10年的年份
for i in range(10):
    year_list.append(now_time-i)
for i in range(len(year_list)):
  report_year.append({
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": f"{year_list[i]}", #前面須加關鍵字才能呼叫選擇月份
          "text": f"{year_list[i]}"
        }
      }
    ]
  }
})

line_bot_api.push_message(user_ids, FlexSendMessage(
  alt_text='測試',contents={
                  "type": "carousel",
                  "contents": report_year
                  }
            ))