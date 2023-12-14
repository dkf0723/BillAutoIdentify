from database import year_report_list
import matplotlib as mpl
import matplotlib.pyplot as plt
from linebot.models import TextSendMessage
import matplotlib.font_manager as FM
import random
import string
import os, pyimgur, glob
font_path = "Noto_Sans_TC/NotoSansTC-VariableFont_wght.ttf"
font = FM.FontProperties(fname=font_path, size=14)
#-------------------------------
# current_datetime = datetime.now()# 取得當前的日期和時間
# modified_datetime = current_datetime + timedelta(hours=8)#時區轉換+8
# modified_year = formatted_datetime_obj.year
# # order_date = modified_datetime.strftime('%Y')#格式化日期，清除
# # order_month_1 = order_date+'-01'
# # order_month_12 = order_date+'-12'
# # print(order_month_1,order_month_12)
# #-------------------------------
# # 建立連接字串
# conn_str = {
#     'host': '140.131.114.242',
#     'user': '112405',
#     'password': '!mdEe24@5',
#     'database': '112-112405'
# }

# try:
#     # 建立連接
#     cnxn = mysql.connector.connect(**conn_str)

#     # 連接成功
#     print("連線成功！")

# except pyodbc.Error as err:
#     # 連接失敗
#     print(f"連線失敗：{err}")
# cursor = cnxn.cursor()
# #---------------對的query，但沒有圖(嗎?)--------------------------------
# query = f"""
#     SELECT 年月,月成本_值, 月利潤_值
#     FROM Statistical_Product
#     WHERE 年月 like '{modified_year}%' AND 年月 != '2023-99';
#     """
# #-------------------------------------------------------------------

# cursor.execute(query)
# result = cursor.fetchall()
# cursor.close()
# cnxn.close()
# print(result)
#-------------------------------
def manager_year_report():
  return #下面解風刪除53、54行
'''def manager_year_report():
  db_report = year_report_list()
  if db_report=="找不到符合條件的資料。":
    show = TextSendMessage(text=db_report)
  else:
    month = []
    month_cost = [] #年成本
    month_profit = [] #年成本
    arr_len = 0
    for i in range(len(db_report)):
      month.append(db_report[i][0])
      month_cost.append(db_report[i][1])
      month_profit.append(db_report[i][2])
    arr_len = len(month)
    arr_ran = range(arr_len)
    check_month = []
    year_cost = []
    year_profit = []
    for i in range(12):
      if i<9:
        check_month.append(f'{order_date}-0{i+1}')
      else:
        check_month.append(f'{order_date}-{i+1}')
    test = 1
    i = 0

    while(len(month)>=test):
      if check_month[i] == month[test-1] :
        year_cost.append(month_cost[test-1])
        year_profit.append(month_profit[test-1])
        test += 1
      else :
        year_cost.append(0)
        year_profit.append(0)
      i += 1
    remaining_month = 12 - len(year_cost)
    for i in range(remaining_month):
        year_cost.append(0)
        year_profit.append(0)
  print(year_cost,year_profit)

#-----------------------------------------------------------
def imgurinfo():
    imgurdata = {
        'CLIENT_ID_data':'ebcfa98f6d190dc'
    }
    return imgurdata
#------------------------處理圖片路徑-----------------------
def handle_image_message():
    image_name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(4))#為圖片隨機命名
    image_name = image_name.upper()+'.jpg'#轉換大寫並加入副檔名
    path='images/'+image_name #儲存資料夾路徑
    return path
    #line_bot_api.push_message(event.reply_token, imagetolink(path))
#-------------------images資料夾中圖片轉連結----------------------
def imagetolink(link):
  imgurdata = imgurinfo()
  #執行轉換連結
  CLIENT_ID = imgurdata['CLIENT_ID_data']
  #title = image_files[:-4] #選擇的關鍵字(報表類型)
  title = '測試' #選擇的關鍵字(報表類型)
  im = pyimgur.Imgur(CLIENT_ID)
  uploaded_image = im.upload_image(link, title=title)
  imagelink = uploaded_image.link
  #執行資料夾中此圖片刪除
  if os.path.isfile(link):
      os.remove(link)
  return imagelink
link = handle_image_message()
#-----------------------------年成本折線圖----------------------------
plt.title('年成本')
plt.plot(year_cost,'ro--', linewidth=2, markersize=6)  # 簡化後的程式碼
x = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
plt.xticks([0,1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],fontsize=20)

plt.savefig(f'{link}', #存path
            transparent=False,
            bbox_inches='tight',
            pad_inches=1)
cost_line_database_link = imagetolink(link)
plt.show()
#-----------------------------年利潤折線圖----------------------------
plt.title('年利潤')
plt.plot(year_profit,'ro--', linewidth=2, markersize=6)  # 簡化後的程式碼
plt.xticks([0,1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],fontsize=20)
# for a,b in zip(x,year_profit):
#   plt.text(a,b,b, ha= 'center', va='bottom',fontsize=14)
plt.savefig(f'{link}', #存path
            transparent=False,
            bbox_inches='tight',
            pad_inches=1)
profit_line_database_link = imagetolink(link)
plt.show()
#-------------------------------
upload_year_report(cost_line_database_link,profit_line_database_link)'''
#建立連接字串
# conn_str = {
#     'host': '140.131.114.242',
#     'user': '112405',
#     'password': '!mdEe24@5',
#     'database': '112-112405'
# }

# try:
#     # 建立連接
#     cnxn = mysql.connector.connect(**conn_str)

#     # 連接成功
#     print("連線成功！")

# except pyodbc.Error as err:
#     # 連接失敗
#     print(f"連線失敗：{err}")
# cursor = cnxn.cursor()

# query = f"""
#     INSERT INTO Statistical_Product (年月,年成本_圖,年利潤_圖)
#     VALUES ( '2023-99','{cost_line_database_link}','{profit_line_database_link}');
#     """

# cursor.execute(query)
# cnxn.commit()
# cursor.close()
# cnxn.close()