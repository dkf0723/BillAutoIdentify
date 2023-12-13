from databse import month_report_list
import matplotlib as mpl
import matplotlib.pyplot as plt

import matplotlib.font_manager as fm
font_path = "Noto_Sans_TC/NotoSansTC-VariableFont_wght.ttf"
font = fm.FontProperties(fname=font_path, size=14)
# #-------------------------------
# current_datetime = datetime.now()# 取得當前的日期和時間
# modified_datetime = current_datetime + timedelta(hours=8)#時區轉換+8
# order_date = modified_datetime.strftime('%Y-%m')#格式化日期，清除
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
# query = """
#     SELECT 商品名稱, 訂購數量, 進貨單價, 商品小計
#     FROM Statistics_Data
#     WHERE 年月='2023-08'
#     Order by 商品ID;
#     """

# cursor.execute(query)
# result = cursor.fetchall()
# cursor.close()
# cnxn.close()
def manager_month_report():
    db_report = month_report_list()
#---------------------------------

    if db_report=="找不到符合條件的資料。":
        show = TextSendMessage(text=db_report)
    else:
        database_product_name = [] #存資料庫商品名
        database_purchase_cost = [] #存資料庫成本
        database_profit = [] #存資料庫利潤
        database_saled_figure = [] #存資料庫售出數量
        product_name = [] #去重複商品名
        purchase_cost = [] #去重複成本
        profit = [] #去重複利潤
        saled_figure = [] #去重複售出數量
        month_total_cost = 0 #月成本
        month_total_profit = 0 #月利潤
        for i in range(len(db_report)):
            if db_report[i][0] in database_product_name:
                loc = database_product_name.index(db_report[i][0])
                database_purchase_cost[loc] += db_report[i][1]*db_report[i][2]
                database_profit[loc] += db_report[i][3]-db_report[i][1]*db_report[i][2]
                database_saled_figure[loc] += db_report[i][1]
            else:
                database_product_name.append(db_report[i][0]) #商品名
                database_purchase_cost.append(db_report[i][1]*db_report[i][2]) #成本
                database_profit.append(db_report[i][3]-db_report[i][1]*db_report[i][2]) #利潤
                database_saled_figure.append(db_report[i][1]) #售出數量     
            month_total_cost += database_purchase_cost[i]
            month_total_profit += database_profit[i]
        #圓餅圖只適合顯示到5個扇面
        if len(product_name) > 4:
            arr_len = len(product_name)-4
        else:
            arr_len = 0
        #長條圖只適合顯示到7個
        if len(product_name) > 6:
            bar_len = len(product_name)-6
        else:
            bar_len = 0
        #------------------------成本排序---------------------------
        list_cost = list(zip(purchase_cost, product_name)) #用zip將成本與名稱壓縮
        list_cost.sort() #再用sort排序
        heapsort_purchase_cost_tuple, heapsort_purchase_cost_product_name_tuple = zip(*list_cost) #解壓縮
        heapsort_purchase_cost = [*heapsort_purchase_cost_tuple] #將tuple轉回list
        heapsort_purchase_cost_product_name = [*heapsort_purchase_cost_product_name_tuple]
        #------------------------利潤排序---------------------------
        list_profit = list(zip(profit, product_name))
        list_profit.sort()
        heapsort_profit_tuple, heapsort_profit_product_name_tuple = zip(*list_profit)
        heapsort_profit = [*heapsort_profit_tuple]
        heapsort_profit_product_name = [*heapsort_profit_product_name_tuple]
        #------------------------熱門商品排序---------------------------
        list_saled_figure = list(zip(saled_figure, product_name))
        list_saled_figure.sort()
        heapsort_saled_figure_tuple, heapsort_saled_figure_product_name_tuple = zip(*list_saled_figure)
        heapsort_saled_figure = [*heapsort_saled_figure_tuple]
        heapsort_saled_figure_product_name = [*heapsort_saled_figure_product_name_tuple]
        #---------------------------圓餅圖只適合顯示到5個扇面--------------------------------
        heapsort_purchase_cost_product_name_limited = heapsort_purchase_cost_product_name[arr_len:] #取前四成本的商品名稱
        heapsort_purchase_cost_limited = heapsort_purchase_cost[arr_len:] #取前四成本的值
        #---------------------------圓餅圖只適合顯示到5個扇面--------------------------------
        heapsort_profit_product_name_limited = heapsort_profit_product_name[arr_len:] #取前四利潤的商品名稱
        heapsort_profit_limited = heapsort_profit[arr_len:] #取前四利潤的值
        #---------------------------長條圖只適合顯示到7個--------------------------------
        heapsort_saled_figure_product_name_limited = heapsort_saled_figure_product_name[bar_len:] #取前六熱門的商品名稱
        heapsort_saled_figure_limited = heapsort_saled_figure[bar_len:] #取前六熱門商品的值

        remaining_total_cost = 0 #取剩餘的成本
        remaining_total_profit = 0 #取剩餘的成本
        remaining_total_saled_figure = 0 #取剩餘的成本
        if arr_len > 0:
        for i in range(arr_len):
            remaining_total_cost +=  int(heapsort_purchase_cost[i])
            remaining_total_profit +=  int(heapsort_profit[i])
        heapsort_purchase_cost_product_name_limited.insert(0, '其他')
        heapsort_purchase_cost_limited.insert(0,remaining_total_cost)
        heapsort_profit_product_name_limited.insert(0, '其他')
        heapsort_profit_limited.insert(0,remaining_total_profit)
        if bar_len > 0:
        for i in range(bar_len):
            remaining_total_saled_figure += int(heapsort_saled_figure[i])
        heapsort_saled_figure_product_name_limited.insert(0, '其他')
        heapsort_saled_figure_limited.insert(0,remaining_total_saled_figure)

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
        #--------------------------透過百分比反推原本的數值---------------------------------------
        def func(s,d):
        t = int(round(s/100.*sum(d)))
        return f'{s:.1f}%\n( {t}元 )'
        #--------------------------月成本圓餅圖---------------------------------------
        plt.title('月成本',x=0.5,y=1.2)
        plt.pie(heapsort_purchase_cost_limited,
                radius=1.5,
                textprops={'weight':'bold', 'size':16},
                labels=heapsort_purchase_cost_product_name_limited,
                autopct=lambda i: func(i,purchase_cost), #lamda 匿名, 呼叫函式
                pctdistance=0.8,
                counterclock = True,
                wedgeprops={'linewidth':3,'edgecolor':'w'}) # 繪製每個扇形的外框
        link = handle_image_message()
        plt.savefig(f'{link}', #存path
                    transparent=False,
                    bbox_inches='tight',
                    pad_inches=1)
        cost_pie_database_link = imagetolink(link)
        plt.show()
        #--------------------------月利潤圓餅圖---------------------------------------
        plt.title('月利潤',x=0.5,y=1.2)
        plt.pie(heapsort_profit_limited,
                radius=1.5,
                textprops={'weight':'bold', 'size':16},
                labels=heapsort_profit_product_name_limited,
                autopct=lambda i: func(i,profit), #lamda 匿名, 呼叫函式
                pctdistance=0.8,
                wedgeprops={'linewidth':3,'edgecolor':'w'}) # 繪製每個扇形的外框

        plt.savefig(f'{link}', #存path
                    transparent=False,
                    bbox_inches='tight',
                    pad_inches=1)
        profit_pie_database_link = imagetolink(link)
        plt.show()
        #--------------------------熱門商品長條圖-------------------------------------
        plt.title('月熱門商品')
        x = range(len(heapsort_saled_figure_product_name_limited))
        h = heapsort_saled_figure_limited
        label = heapsort_saled_figure_product_name_limited   # 標籤數據
        plt.xticks(ticks=x,
                labels=label,
                fontsize=16,
                rotation=30)
        plt.bar(x,h,tick_label=label, width=0.5)  # 加入顏色、標籤和寬度參數
        plt.savefig(f'{link}', #存path
                    transparent=False,
                    bbox_inches='tight',
                    pad_inches=1)
        saled_figure_chart_database_link = imagetolink(link)
        plt.show()
#-------------------------------
# #建立連接字串
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
#     INSERT INTO Statistical_Product (年月,月成本_圖,月利潤_圖,月熱門商品_圖,月成本_值,月利潤_值)
#     VALUES ( '2023-08','{cost_pie_database_link}','{profit_pie_database_link}','{saled_figure_chart_database_link}','{month_total_cost}','{month_total_profit}');
#     """


# cursor.execute(query)
# cnxn.commit()
# cursor.close()
# cnxn.close()