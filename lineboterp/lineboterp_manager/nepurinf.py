from linebot.models import TextSendMessage,FlexSendMessage
from datetime import datetime
import manager
import pytz
from database import newtopur_inf,newingtopur_inf,manufacturer,Manufacturer_infochange,MP_information_modify,gettime,db_infotmation
from FMtestpur import Purchase_fillin_and_check_screen,Purchase_establishment_screen
###廠商管理---
from relevant_information import bank,Citytalk#廠商建立用，未來拔掉
from manufacturerFM import Manufacturer_fillin_and_check_screen,Manufacturer_establishment_screen,Manufacturer_edit_screen #廠商建立用，未來拔掉
from vendor_management import Manufacturer_edit,Manufacturer_list#廠商建立用，未來拔掉
#-------蓉所需-
from FM import Now_Product_Modification_FM,Pre_Product_Modification_FM
import database,FM
from linebot.models import *
message_storage = {}


def purchase_check():
    id = manager.user_id
    state = manager.user_state
    if state[id] == 'pre_purchase_ck':
        check_texts = newing_purchaseinf()
    elif 'Product_Modification' in state[id]:#商品修改-蓉
        check_texts = product_modification()
    elif 'createNowProduct' in state[id]:
        check_texts = createNowProduct()
    elif state[id] in 'createPreOrder':
        check_texts = createPreOrder()
    elif state[id] in 'preAndNowSelect':
        check_texts = preAndNowSelect()
    elif state[id] in 'searchingOrderByPhoneNumber':
        check_texts = searchingOrderByPhoneNumber()
    #-------------------廠商管理-新增廠商----------------------
    elif state[id] in ['manufacturer_name','other_manufacturer_add','manufacturer_principal',
                       'manufacturer_localcalls','manufacturer_phonenum','manufacturer_Payment',
                       'manufacturer_bank','manufacturer_bankaccount','manufacturer_end']:#新增廠商
        check_texts = new_manufacturer()#single_manufacturer_num單獨建立；other_manufacturer新商品新廠商過來的
    elif state[id] == 'manufacturereditall':
        check_texts = Manufacturereditall_check()
    elif 'manufacturer_edit_' in state[id]:
        check_texts = manufacturer_editinfo()
    #-----1111測試----------------------------
    elif 'purchase_newinfo_' in state[id]:
        check_texts = newing_purchaseinf()
    #-----------------------------------------
    return check_texts

def purchase_info(is_ingnepurchase=False):
    id = manager.user_id
    state = manager.user_state
    state1 = manager.user_state1
    message = manager.msg
    message_storage = manager.storage
    
    if message == '取消':
        state[id] = 'normal'
        state1[id] = 'NAN'
        check_text = TextSendMessage(text=f"取消新增{'現購' if is_ingnepurchase else '預購'}商品！")
    elif state1[id] == 'num':
        message_storage[id + 'purchase_num'] = int(message)
        message_storage[id + 'purchase_all'] = f'\n您輸入的進貨數量： {message}'
        check_text = f"{message_storage[id + 'purchase_all']}\n=>請接著輸入「進貨單價」"
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'cost'
    elif state1[id] == 'cost':
        message_storage[id + 'purchase_cost'] = int(message)
        purchase_num = message_storage[id + 'purchase_num']
        purchase_cost = message_storage[id + 'purchase_cost']
        payment_amount = purchase_num * purchase_cost
        message_storage[id + 'give_money'] = payment_amount
        message_storage[id + 'purchase_all'] += f'\n您輸入的進貨單價： {message}'
        message_storage[id + 'purchase_all'] += f'\n您輸入的匯款金額： {payment_amount}'  
        taiwan_timezone = pytz.timezone('Asia/Taipei')
        current_time_taiwan = datetime.now(taiwan_timezone)
        current_time_str = current_time_taiwan.strftime("%Y-%m-%d %H:%M:%S")
        message_storage[id + 'purchase_time'] = current_time_str  
        message_storage[id + 'purchase_all'] += f'\n您輸入的進貨時間： {current_time_str}'
        if message_storage[id + 'manu_payment'] != '現金':
            template_message = FlexSendMessage(
                                alt_text='匯款時間選擇',
                                contents={
                                    "type": "carousel",
                                    "contents": [{
                                    "type": "bubble",
                                    "body": {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "選擇日期時間",
                                            "weight": "bold",
                                            "size": "xl"
                                        },
                                        {
                                            "type": "text",
                                            "text": f"{message_storage[id+'purchase_all']}\n=>請接著輸入「匯款時間」",
                                            "wrap": True
                                        }
                                        ]
                                    },
                                    "footer": {
                                        "type": "box",
                                        "layout": "vertical",
                                        "spacing": "sm",
                                        "contents": [
                                        {
                                            "type": "button",
                                            "style": "link",
                                            "height": "sm",
                                            "action": {
                                            "type": "datetimepicker",
                                            "label": "點擊選擇日期與時間",
                                            "data": f"新增{'現購' if is_ingnepurchase else '預購'}商品匯款時間",
                                            "mode": "datetime"
                                            }
                                        }
                                        ],
                                        "flex": 0
                                    }
                                    }]   
                                    } 
                                )
            check_text = template_message
            state1[id] = 'mtime'
        else:
            message_storage[id + 'money_time'] = 'NULL'
            check_text = TextSendMessage(text=f"{message_storage[id+'purchase_all']}\n確認後請輸入OK")
            state1[id] = 'end'
    elif state1[id] == 'mtime':
        check_text = f"{message_storage[id+'purchase_all']}\n確認後請輸入OK"
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'end'
    elif state1[id] == 'end':
        if message in ['ok','Ok','oK','OK']:
            if is_ingnepurchase:
                result = newingtopur_inf(
                    message_storage[id + 'purchase_pid'],
                    message_storage[id + 'purchase_num'],
                    message_storage[id + 'purchase_cost'],
                    message_storage[id + 'purchase_unit'],
                    message_storage[id + 'purchase_time'],
                    message_storage[id + 'give_money'],
                    message_storage[id + 'money_time']
                )
            else:
                result = newtopur_inf(
                    message_storage[id + 'purchase_pid'],
                    message_storage[id + 'purchase_num'],
                    message_storage[id + 'purchase_cost'],
                    message_storage[id + 'purchase_unit'],
                    message_storage[id + 'purchase_time'],
                    message_storage[id + 'give_money'],
                    message_storage[id + 'money_time']
                )
            if result == 'ok':
                check_text = f'進貨{"現購" if is_ingnepurchase else "預購"}商品成功！'
                check_text = TextSendMessage(text=check_text)
            else:
                check_text = f'進貨{"現購" if is_ingnepurchase else "預購"}商品失敗！稍後再試' 
                check_text = TextSendMessage(text=check_text)
            state[id] = 'normal'
            state1[id] = 'NAN'
    return check_text

#---------------二次進貨-預購---------------------
def renepurchase_info():
    id = manager.user_id
    state = manager.user_state
    state1 = manager.user_state1
    message = manager.msg
    message_storage = manager.storage
    if message == '取消':
        state[id] = 'normal'
        state1[id] = 'NAN'
        check_text = TextSendMessage(text="取消快速進貨預購商品！")
    elif state1[id] == 'num':
        message_storage[id + 'purchase_num'] = int(message)
        message_storage[id + 'purchase_all'] = f'\n您輸入的進貨數量： {message}'
        check_text = f"{message_storage[id + 'purchase_all']}\n=>請接著輸入「進貨單價」"
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'cost'
    elif state1[id] == 'cost':
        message_storage[id + 'purchase_cost'] = int(message)
        purchase_num = message_storage[id + 'purchase_num']
        purchase_cost = message_storage[id + 'purchase_cost']
        payment_amount = purchase_num * purchase_cost
        message_storage[id + 'give_money'] = payment_amount
        message_storage[id + 'purchase_all'] += f'\n您輸入的進貨單價： {message}'
        message_storage[id + 'purchase_all'] += f'\n您輸入的匯款金額： {payment_amount}'  
        taiwan_timezone = pytz.timezone('Asia/Taipei')
        current_time_taiwan = datetime.now(taiwan_timezone)
        current_time_str = current_time_taiwan.strftime("%Y-%m-%d %H:%M:%S")
        message_storage[id + 'purchase_time'] = current_time_str  
        message_storage[id + 'purchase_all'] += f'\n您輸入的進貨時間： {current_time_str}'
        if message_storage[id + 'manu_payment'] != '現金':
            template_message = FlexSendMessage(
                                alt_text='匯款時間選擇',
                                contents={
                                    "type": "carousel",
                                    "contents": [{
                                    "type": "bubble",
                                    "body": {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "選擇日期時間",
                                            "weight": "bold",
                                            "size": "xl"
                                        },
                                        {
                                            "type": "text",
                                            "text": f"{message_storage[id+'purchase_all']}\n=>請接著輸入「匯款時間」",
                                            "wrap": True
                                        }
                                        ]
                                    },
                                    "footer": {
                                        "type": "box",
                                        "layout": "vertical",
                                        "spacing": "sm",
                                        "contents": [
                                        {
                                            "type": "button",
                                            "style": "link",
                                            "height": "sm",
                                            "action": {
                                            "type": "datetimepicker",
                                            "label": "點擊選擇日期與時間",
                                            "data": "快速進貨商品匯款時間",
                                            "mode": "datetime"
                                            }
                                        }
                                        ],
                                        "flex": 0
                                    }
                                    }]   
                                    } 
                                )
            check_text = template_message
            state1[id] = 'mtime'
        else:
            message_storage[id + 'money_time'] = 'NULL'
            check_text = TextSendMessage(text=f"{message_storage[id+'purchase_all']}\n確認後請輸入OK")
            state1[id] = 'end'
    elif state1[id] == 'mtime':
        check_text = f"{message_storage[id+'purchase_all']}\n確認後請輸入OK"
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'end'
    elif state1[id] == 'end':
        if message in ['ok','Ok','oK','OK']:
            result = newtopur_inf(
            message_storage[id + 'purchase_pid'],
            message_storage[id + 'purchase_num'],
            message_storage[id + 'purchase_cost'],
            message_storage[id + 'purchase_unit'],
            message_storage[id + 'purchase_time'],
            message_storage[id + 'give_money'],
            message_storage[id + 'money_time']
        )
        if result == 'ok':
            check_text = '快速進貨預購商品成功！'
            check_text = TextSendMessage(text=check_text)
        else:
            check_text = '快速進貨預購商品失敗！稍後再試' 
            check_text = TextSendMessage(text=check_text)
        state[id] = 'normal'
        state1[id] = 'NAN'
    return check_text

#---------------進貨-現購---------------------
def quick_now_purchase():
    id = manager.user_id
    state = manager.user_state
    state1 = manager.user_state1
    message = manager.msg
    message_storage = manager.storage
    
    if message == '取消':
        state[id] = 'normal'
        state1[id] = 'NAN'
        check_text = TextSendMessage(text="取消快速進貨現購商品！")
    elif state1[id] == 'num':
        message_storage[id + 'purchase_num'] = int(message)
        message_storage[id + 'purchase_all'] = f'\n您輸入的進貨數量： {message}'
        check_text = f"{message_storage[id + 'purchase_all']}\n=>請接著輸入「進貨單價」"
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'cost'
    elif state1[id] == 'cost':
        message_storage[id + 'purchase_cost'] = int(message)
        purchase_num = message_storage[id + 'purchase_num']
        purchase_cost = message_storage[id + 'purchase_cost']
        payment_amount = purchase_num * purchase_cost
        message_storage[id + 'give_money'] = payment_amount
        message_storage[id + 'purchase_all'] += f'\n您輸入的進貨單價： {message}'
        message_storage[id + 'purchase_all'] += f'\n您輸入的匯款金額： {payment_amount}'  
        taiwan_timezone = pytz.timezone('Asia/Taipei')
        current_time_taiwan = datetime.now(taiwan_timezone)
        current_time_str = current_time_taiwan.strftime("%Y-%m-%d %H:%M:%S")
        message_storage[id + 'purchase_time'] = current_time_str  
        message_storage[id + 'purchase_all'] += f'\n您輸入的進貨時間： {current_time_str}'
        message_storage[id + 'money_time'] = 'NULL'
        check_text = TextSendMessage(text=f"{message_storage[id+'purchase_all']}\n確認後請輸入OK")
        state1[id] = 'end'
    elif state1[id] == 'end':
        if message in ['ok','Ok','oK','OK']:
            result = newingtopur_inf(
            message_storage[id + 'purchase_pid'],
            message_storage[id + 'purchase_num'],
            message_storage[id + 'purchase_cost'],
            message_storage[id + 'purchase_unit'],
            message_storage[id + 'purchase_time'],
            message_storage[id + 'give_money'],
            message_storage[id + 'money_time']
        )
        if result == 'ok':
            check_text = '快速進貨現購商品成功！'
            check_text = TextSendMessage(text=check_text)
        else:
            check_text = '快速進貨現購商品失敗！稍後再試' 
            check_text = TextSendMessage(text=check_text)
        state[id] = 'normal'
        state1[id] = 'NAN'
    return check_text
def format_time(selected_time):
    # 这里需要根据实际情况来解析和格式化时间
    # 下面的示例只是一个基本的示例
    # 请根据实际需求进行适当修改
    formatted_time = selected_time  # 假设 selected_time 已经是 "yyyy-mm-dd HH:MM:SS" 格式
    return formatted_time
#######廠商管理開始
#-------------------廠商管理-新增廠商----------------------
def new_manufacturer():
    id = manager.user_id
    state = manager.user_state
    message = manager.msg
    message_storage = manager.storage
    global_Storage = manager.global_Storage
    if state[id] == 'other_manufacturer_add':
        message_storage[id+'addtype'] = 'other'#最後判斷是否狀態回給新商品建立下一步狀態
        state[id] = 'manufacturer_name'
        message_storage[id+'Manufacturer_edit_step'] = 0
        check_text = Manufacturer_fillin_and_check_screen('')
    elif message in ['取消','重新填寫']:
        message_storage[id+'manufacturer_name'] = 'NAN'
        message_storage[id+'manufacturer_principal'] = 'NAN'
        message_storage[id+'manufacturer_localcalls'] = 'NAN'
        message_storage[id+'manufacturer_phonenum'] = 'NAN'
        message_storage[id+'manufacturer_Payment'] = 'NAN'
        message_storage[id+'manufacturer_bankid'] = 'NAN'
        message_storage[id+'manufacturer_bankname'] = 'NAN'
        message_storage[id+'manufacturer_bankaccount'] = 'NAN'
        message_storage[id+'manufacturer_localcalls_code'] = 'NAN'
        message_storage[id+'manufacturer_localcalls_num'] = 'NAN'
        if message == '取消':
            state[id] = 'normal'
            check_text = TextSendMessage(text="取消新增廠商流程囉！")
        else:
            state[id] = 'manufacturer_name'
            message_storage[id+'Manufacturer_edit_step'] = 0
            check_text = Manufacturer_fillin_and_check_screen('')
    elif state[id] == 'manufacturer_name':
        textmsg,check_step = check_manufacturer_name()#廠商名稱檢查
        if check_step == 'ok':
            state[id] = 'manufacturer_principal' #狀態負責人
            message_storage[id+'Manufacturer_edit_step'] = 1
            check_text = Manufacturer_fillin_and_check_screen('')
        else:
            check_text = Manufacturer_fillin_and_check_screen(textmsg)
    elif state[id] == 'manufacturer_principal':
        textmsg,check_step = check_manufacturer_principal()#廠商負責人或對接人檢查
        if check_step == 'ok':
            state[id] = 'manufacturer_localcalls' #狀態市話
            message_storage[id+'Manufacturer_edit_step'] = 2
            check_text = Manufacturer_fillin_and_check_screen('')
        else:
            check_text = Manufacturer_fillin_and_check_screen(textmsg)
    elif state[id] == 'manufacturer_localcalls':
        textmsg,check_step = check_manufacturer_localcalls()#廠商市話檢查
        if check_step == 'ok':
            state[id] = 'manufacturer_phonenum' #狀態電話
            message_storage[id+'Manufacturer_edit_step'] = 3
            check_text = Manufacturer_fillin_and_check_screen('')
        else:
            check_text = Manufacturer_fillin_and_check_screen(textmsg)
    elif state[id] == 'manufacturer_phonenum':
        textmsg,check_step = check_manufacturer_phonenum()#廠商電話檢查
        if check_step == 'ok':
            state[id] = 'manufacturer_Payment' #狀態付款方式
            message_storage[id+'Manufacturer_edit_step'] = 4
            check_text = Manufacturer_fillin_and_check_screen('')
        else:
            check_text = Manufacturer_fillin_and_check_screen(textmsg)
    elif state[id] == 'manufacturer_Payment':
        textmsg,check_step = check_manufacturer_Payment()#廠商付款方式檢查
        if check_step == 'ok':
            state[id] = 'manufacturer_bank' #狀態行庫
            message_storage[id+'Manufacturer_edit_step'] = 5
            check_text = Manufacturer_fillin_and_check_screen('')
        elif check_step == 'okend':
            state[id] = 'manufacturer_end' #狀態確認
            message_storage[id+'Manufacturer_edit_step'] = 8
            check_text = Manufacturer_fillin_and_check_screen('')
        else:
            check_text = Manufacturer_fillin_and_check_screen(textmsg)
    elif state[id] == 'manufacturer_bank':
        textmsg,check_step = check_manufacturer_bank()#行庫/行庫代號檢查
        if check_step == 'ok':
            state[id] = 'manufacturer_bankaccount' #狀態行庫帳號
            message_storage[id+'Manufacturer_edit_step'] = 6
            check_text = Manufacturer_fillin_and_check_screen('')
        else:
            check_text = Manufacturer_fillin_and_check_screen(textmsg)
    elif state[id] == 'manufacturer_bankaccount':
        textmsg,check_step = check_manufacturer_bankaccount()#廠商付款帳號確認
        check_text = TextSendMessage(text=textmsg)
        if check_step == 'ok':
            state[id] = 'manufacturer_end' #狀態新增確認
            message_storage[id+'Manufacturer_edit_step'] = 8
            check_text = Manufacturer_fillin_and_check_screen('')
        else:
            check_text = Manufacturer_fillin_and_check_screen(textmsg)
    elif state[id] == 'manufacturer_end':
        if message.isdigit():
            if message in ['1','2']:
                if message == '1':
                    citycall = f"({message_storage[id+'manufacturer_localcalls_code']}){message_storage[id+'manufacturer_localcalls_num']}"
                    check,info = manufacturer(message_storage[id+'manufacturer_name'],message_storage[id+'manufacturer_principal'],
                                              citycall,message_storage[id+'manufacturer_phonenum'],
                                              message_storage[id+'manufacturer_Payment'],message_storage[id+'manufacturer_bankid'],
                                              message_storage[id+'manufacturer_bankname'],message_storage[id+'manufacturer_bankaccount'])
                    if check == 'ok':
                        #廠商編號, 廠商名, 負責或對接人, 市話, 電話, 付款方式, 行庫名, 行庫代號, 匯款帳號
                        check_text = Manufacturer_establishment_screen(info[0][0],info[0][1],info[0][2],info[0][3],info[0][4],info[0][5],
                                                                       info[0][6],info[0][7],info[0][8])
                    else:
                        check_text = TextSendMessage(text=f"{info}廠商建立流程失敗！")
                    #check_text = TextSendMessage(text=f"廠商建立成功！")
                elif message == '2':
                    check_text = TextSendMessage(text="取消新增廠商流程囉！")
                if message_storage[id+'addtype'] == 'other':
                    global_Storage[id+'manufacturerId'] = info[0][0]#廠商id
                    state[id] = 'preAndNowSelect'#下一步的狀態
                    selectMessage = TextSendMessage(text='請點選新增類別',quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="現購", text="現購")),
                        QuickReplyButton(action=MessageAction(label="預購", text="預購")),
                    ]))
                    check_text = [check_text,selectMessage]
                else:
                    state[id] = 'normal'
                message_storage[id+'manufacturer_name'] = 'NAN'
                message_storage[id+'manufacturer_principal'] = 'NAN'
                message_storage[id+'manufacturer_localcalls'] = 'NAN'
                message_storage[id+'manufacturer_phonenum'] = 'NAN'
                message_storage[id+'manufacturer_Payment'] = 'NAN'
                message_storage[id+'manufacturer_bankid'] = 'NAN'
                message_storage[id+'manufacturer_bankname'] = 'NAN'
                message_storage[id+'manufacturer_bankaccount'] = 'NAN'
                message_storage[id+'manufacturer_localcalls_code'] = 'NAN'
                message_storage[id+'manufacturer_localcalls_num'] = 'NAN'
            else:
                message_storage[id+'Manufacturer_edit_step'] = 8
                check_text = Manufacturer_fillin_and_check_screen(f"「{message}」不是此流程的內容喔！")
        else:
            message_storage[id+'Manufacturer_edit_step'] = 8
            check_text = Manufacturer_fillin_and_check_screen(f"「{message}」不是此流程的內容喔！")
    return check_text
#-------------------廠商管理-修改廠商資料分類----------------------
def Manufacturereditall_check():
    user_id = manager.user_id
    user_state = manager.user_state
    msg = manager.msg
    storage = manager.storage
    list_page = manager.list_page
    if '【廠商列表下一頁】' in msg:
        original_string = msg
        # 找到"【廠商列表下一頁】"的位置
        start_index = original_string.find("【廠商列表下一頁】")
        if start_index != -1:
            # 從"【廠商列表下一頁】"後面開始切割字串
            substr = original_string[start_index + len("【廠商列表下一頁】"):]
            # 切割取得前後文字
            min = int(substr.split("～")[0].strip()) # 取出～前面的字並去除空白字元
            max = int(substr.split("～")[1].strip()) # 取出～後面的字並去除空白字元
        if (min - 1) < 0:
            min = 0
        else:
            min = min - 1
        list_page[user_id+'廠商列表min'] = min
        list_page[user_id+'廠商列表max'] = max
        user_state[user_id] = 'normal'
        Manufacturerlistpage = Manufacturer_list()
        if 'TextSendMessage' in Manufacturerlistpage:
            show = Manufacturerlistpage
        else:
            show = FlexSendMessage(
            alt_text='【管理廠商】廠商列表',
            contents={
                "type": "carousel",
                "contents": Manufacturerlistpage      
                } 
            )
    elif '【廠商修改】廠商' in msg:
        if storage[user_id+'manufacturer_list_id'] != None:
            check = msg[8:]
            if check == '名稱':
                user_state[user_id] = 'manufacturer_edit_name'
                show = Manufacturer_edit_screen(1,'',storage[user_id+'manufacturer_list_name'])#edittype,errormsg,before
            elif check == '負責人或對接人':
                user_state[user_id] = 'manufacturer_edit_principal'
                show = Manufacturer_edit_screen(2,'',storage[user_id+'manufacturer_list_principal'])#edittype,errormsg,before
            elif check == '市話':
                user_state[user_id] = 'manufacturer_edit_localcalls'
                show = Manufacturer_edit_screen(3,'',storage[user_id+'manufacturer_list_localcalls'])#edittype,errormsg,before
            elif check == '行動電話':
                user_state[user_id] = 'manufacturer_edit_phonenum'
                show = Manufacturer_edit_screen(4,'',storage[user_id+'manufacturer_list_phone'])#edittype,errormsg,before
            elif check == '付款方式':
                user_state[user_id] = 'manufacturer_edit_payment'
                show = Manufacturer_edit_screen(5,'',storage[user_id+'manufacturer_list_payment'])#edittype,errormsg,before
            elif check == '行庫/行庫代號':
                user_state[user_id] = 'manufacturer_edit_bank'
                before = [str(storage[user_id+'manufacturer_list_bankid']),storage[user_id+'manufacturer_list_bankname']]
                show = Manufacturer_edit_screen(6,'',before)#edittype,errormsg,before
            elif check == '付款帳號':
                user_state[user_id] = 'manufacturer_edit_bankaccount'
                show = Manufacturer_edit_screen(7,'',storage[user_id+'manufacturer_list_bankaccount'])#edittype,errormsg,before
            else:
                user_state[user_id] = 'manufacturereditall'
                show = [TextSendMessage(text=f"輸入的「{msg}」不是修改廠商資料流程中的指令！"),Manufacturer_edit()]
        else:
            show = [TextSendMessage(text='非正常流程進入修改喔！'),Manufacturer_edit()]
    else:
        show = [TextSendMessage(text=f"輸入的「{msg}」不是修改廠商資料流程中的指令！"),Manufacturer_edit()]
    return show
#-------------------廠商管理-修改廠商資料----------------------
def manufacturer_editinfo():
    id = manager.user_id
    state = manager.user_state
    message = manager.msg
    message_storage = manager.storage
    #editfield=廠商名, 負責或對接人, 市話, 電話, 付款方式, 行庫名, 行庫代號, 匯款帳號
    show = [Manufacturer_edit()]#退回修改清單頁
    if message == '取消':
        state[id] = 'manufacturereditall'
        message_storage[id+'manufacturer_name'] = 'NAN'
        message_storage[id+'manufacturer_principal'] = 'NAN'
        message_storage[id+'manufacturer_localcalls'] = 'NAN'
        message_storage[id+'manufacturer_phonenum'] = 'NAN'
        message_storage[id+'manufacturer_Payment'] = 'NAN'
        message_storage[id+'manufacturer_bankid'] = 'NAN'
        message_storage[id+'manufacturer_bankname'] = 'NAN'
        message_storage[id+'manufacturer_bankaccount'] = 'NAN'
        message_storage[id+'manufacturer_localcalls_code'] = 'NAN'
        message_storage[id+'manufacturer_localcalls_num'] = 'NAN'
        check_text = Manufacturer_edit()
    elif state[id] == 'manufacturer_edit_name':
        if message_storage[id+'manufacturer_list_name'] == message:#判斷有沒有修改
            state[id] = 'manufacturereditall'
            check_text = Manufacturer_edit()
        else:
            textmsg,check_step = check_manufacturer_name()#廠商名稱檢查
            if check_step == 'ok':
                #發送修改資料庫
                changedb =  Manufacturer_infochange('廠商名',message)#ok/no
                if changedb == 'ok':
                    check_text = Manufacturer_edit()
                else:
                    show.append(TextSendMessage(text='廠商名稱修改失敗！請稍後在試。'))
                    check_text = Manufacturer_edit()#退回修改清單頁
                state[id] = 'manufacturereditall'
            else:
                check_text = Manufacturer_edit_screen(1,textmsg,message_storage[id+'manufacturer_list_name'])#edittype,errormsg,before..名稱
    elif state[id] == 'manufacturer_edit_principal':
        if message_storage[id+'manufacturer_list_principal'] == message:#判斷有沒有修改
            state[id] = 'manufacturereditall'
            check_text = Manufacturer_edit()
        else:
            textmsg,check_step = check_manufacturer_principal()#廠商負責人或對接人檢查
            if check_step == 'ok':
                #發送修改資料庫
                changedb =  Manufacturer_infochange('負責或對接人',message)#ok/no
                if changedb == 'ok':
                    check_text = Manufacturer_edit()
                else:
                    show.append(TextSendMessage(text='廠商負責或對接人修改失敗！請稍後在試。'))
                    check_text = Manufacturer_edit()#退回修改清單頁
                state[id] = 'manufacturereditall'
            else:
                check_text = Manufacturer_edit_screen(2,textmsg,message_storage[id+'manufacturer_list_principal'])#edittype,errormsg,before..負責人
    elif state[id] == 'manufacturer_edit_localcalls':
        if message_storage[id+'manufacturer_list_localcalls'] == message:#判斷有沒有修改
            state[id] = 'manufacturereditall'
            check_text = Manufacturer_edit()
        else:
            textmsg,check_step = check_manufacturer_localcalls()#廠商市話檢查
            if check_step == 'ok':
                #發送修改資料庫
                citycall = f"({message_storage[id+'manufacturer_localcalls_code']}){message_storage[id+'manufacturer_localcalls_num']}"
                changedb =  Manufacturer_infochange('市話',citycall)#ok/no
                if changedb == 'ok':
                    check_text = Manufacturer_edit()
                else:
                    show.append(TextSendMessage(text='廠商市話修改失敗！請稍後在試。'))
                    check_text = Manufacturer_edit()#退回修改清單頁
                state[id] = 'manufacturereditall'
            else:
                check_text = Manufacturer_edit_screen(3,textmsg,message_storage[id+'manufacturer_list_localcalls'])#edittype,errormsg,before..市話
    elif state[id] == 'manufacturer_edit_phonenum':
        if message_storage[id+'manufacturer_list_phone'] == message:#判斷有沒有修改
            state[id] = 'manufacturereditall'
            check_text = Manufacturer_edit()
        else:
            textmsg,check_step = check_manufacturer_phonenum()#廠商電話檢查
            if check_step == 'ok':
                #發送修改資料庫
                changedb =  Manufacturer_infochange('電話',message)#ok/no
                if changedb == 'ok':
                    check_text = Manufacturer_edit()
                else:
                    show.append(TextSendMessage(text='廠商電話修改失敗！請稍後在試。'))
                    check_text = Manufacturer_edit()#退回修改清單頁
                state[id] = 'manufacturereditall'
            else:
                check_text = Manufacturer_edit_screen(4,textmsg,message_storage[id+'manufacturer_list_phone'])#edittype,errormsg,before..電話
    elif state[id] == 'manufacturer_edit_payment':
        if message_storage[id+'manufacturer_list_payment'] == message:#判斷有沒有修改
            state[id] = 'manufacturereditall'
            check_text = Manufacturer_edit()
        else:
            textmsg,check_step = check_manufacturer_Payment()#廠商付款方式檢查
            if check_step in ['ok','okend'] :
                #發送修改資料庫
                changedb =  Manufacturer_infochange('付款方式',message)#ok/no
                if message == '現金':
                    changedb1 =  Manufacturer_infochange('行庫代號','略過')#ok/no
                    changedb2 =  Manufacturer_infochange('行庫名','略過')#ok/no
                    changedb3 =  Manufacturer_infochange('匯款帳號','略過')#ok/no
                else:
                    changedb1 =  'ok'
                    changedb2 =  'ok'
                    changedb3 =  'ok'

                if (changedb == 'ok') and (changedb1 == 'ok') and (changedb2 == 'ok') and (changedb3 == 'ok'):
                    if (message == '匯款') and (message_storage[id+'manufacturer_list_bankid'] == '略過'):#判斷有沒有匯款資料
                        state[id] = 'manufacturer_edit_bank'#接續完成行庫代號/名稱及帳號
                        before = [str(message_storage[id+'manufacturer_list_bankid']),message_storage[id+'manufacturer_list_bankname']]
                        check_text = Manufacturer_edit_screen(6,textmsg,before)#edittype,errormsg,before..行庫/代號
                    else:
                        state[id] = 'manufacturereditall'
                        check_text = Manufacturer_edit()
                else:
                    show.append(TextSendMessage(text='付款方式修改失敗！請稍後在試。'))
                    check_text = Manufacturer_edit()#退回修改清單頁
                    state[id] = 'manufacturereditall'
            else:
                check_text = Manufacturer_edit_screen(5,textmsg,message_storage[id+'manufacturer_list_payment'])#edittype,errormsg,before..付款方式
    elif state[id] == 'manufacturer_edit_bank':
        textmsg,check_step = check_manufacturer_bank()#行庫/行庫代號檢查
        if check_step == 'ok':
            #發送修改資料庫
            bankid = message_storage[id+'manufacturer_bankid']
            bankname = message_storage[id+'manufacturer_bankname']
            changedb1 =  Manufacturer_infochange('行庫代號',bankid)#ok/no
            changedb2 =  Manufacturer_infochange('行庫名',bankname)#ok/no
            if changedb1 == 'ok' and changedb2 == 'ok':
                if message_storage[id+'manufacturer_list_bankaccount'] == '略過':
                    state[id] = 'manufacturer_edit_bankaccount'#接續完成帳號
                    check_text = Manufacturer_edit_screen(7,textmsg,message_storage[id+'manufacturer_list_bankaccount'])#edittype,errormsg,before..行庫/代號
                else:
                    state[id] = 'manufacturereditall'
                    check_text = Manufacturer_edit()
            else:
                failinfo = ''
                if changedb1 == 'no':
                    failinfo += '行庫代號'
                elif changedb2 == 'no':
                    failinfo += '行庫名稱'
                if len(failinfo) > 4:
                    failinfo = '行庫代號及行庫名稱'
                show.append(TextSendMessage(text=f"{failinfo}修改失敗！請稍後在試。"))
                check_text = Manufacturer_edit()#退回修改清單頁
                state[id] = 'manufacturereditall'
        else:
            before = [str(message_storage[id+'manufacturer_list_bankid']),message_storage[id+'manufacturer_list_bankname']]
            check_text = Manufacturer_edit_screen(6,textmsg,before)#edittype,errormsg,before..行庫/代號
    elif state[id] == 'manufacturer_edit_bankaccount':
        if message_storage[id+'manufacturer_list_bankaccount'] == message:#判斷有沒有修改
            state[id] = 'manufacturereditall'
            check_text = Manufacturer_edit()
        else:
            textmsg,check_step = check_manufacturer_bankaccount()#廠商付款帳號確認
            bankaccount = message_storage[id+'manufacturer_bankaccount']
            if check_step == 'ok':
                #發送修改資料庫
                changedb =  Manufacturer_infochange('匯款帳號',bankaccount)#ok/no
                if changedb == 'ok':
                    check_text = Manufacturer_edit()
                else:
                    show.append(TextSendMessage(text='匯款帳號修改失敗！請稍後在試。'))
                    check_text = Manufacturer_edit()#退回修改清單頁
                state[id] = 'manufacturereditall'
            else:
                check_text = Manufacturer_edit_screen(7,textmsg,message_storage[id+'manufacturer_list_bankaccount'])#edittype,errormsg,before..行庫帳號
    else:
        state[id] = 'manufacturereditall'
        check_text = [TextSendMessage(text=f"「{message}」不是廠商修改資料的項目。"),Manufacturer_edit()]
    message_storage[id+'manufacturer_name'] = 'NAN'
    message_storage[id+'manufacturer_principal'] = 'NAN'
    message_storage[id+'manufacturer_localcalls'] = 'NAN'
    message_storage[id+'manufacturer_phonenum'] = 'NAN'
    message_storage[id+'manufacturer_Payment'] = 'NAN'
    message_storage[id+'manufacturer_bankid'] = 'NAN'
    message_storage[id+'manufacturer_bankname'] = 'NAN'
    message_storage[id+'manufacturer_bankaccount'] = 'NAN'
    message_storage[id+'manufacturer_localcalls_code'] = 'NAN'
    message_storage[id+'manufacturer_localcalls_num'] = 'NAN'
    return check_text

###-------------------廠商名稱檢查----------------------
def check_manufacturer_name():
    id = manager.user_id
    message = manager.msg
    message_storage = manager.storage
    if len(message) <= 20:
        message_storage[id+'manufacturer_name'] = message #廠商名暫存
        check_step = 'ok'
        check_text = ''
    else:
        check_step = ''
        check_text = f"輸入的「{message}」名稱大於20字喔！"
    return check_text,check_step
###-------------------廠商負責人或對接人檢查----------------------
def check_manufacturer_principal():
    id = manager.user_id
    message = manager.msg
    message_storage = manager.storage
    if len(message) <= 10:
        message_storage[id+'manufacturer_principal'] = message #負責人暫存
        check_step = 'ok'
        check_text = ''
    else:
        check_step = ''
        check_text = f"輸入的「{message}」名稱大於10字喔！"
    return check_text,check_step
###-------------------廠商市話檢查----------------------
def check_manufacturer_localcalls():
    id = manager.user_id
    message = manager.msg
    message_storage = manager.storage
    citytalkinfo = Citytalk()#市話所有資訊
    if message.isdigit():
        check_areacode = 'no'
        if len(message) in [9,10]:
            for info in citytalkinfo:
                for i in range(4, 0, -1):#從前4,3,2,1倒數切割
                    if message[:(i)] == info['code']:#從區碼清單中比對是否存在
                        check_areacode = 'ok'
                        if message[i:][0] in info['starting_number']:
                            if len(message[i:]) in info['back_code_length']:
                                message_storage[id+'manufacturer_localcalls'] = message #市話暫存
                                message_storage[id+'manufacturer_localcalls_code'] = info['code'] #區碼
                                message_storage[id+'manufacturer_localcalls_num'] = message[i:] #市話
                                check_step = 'ok'
                                check_text = ''
                            else:
                                lengthmsg = ''
                                for length in info['back_code_length']:
                                    lengthmsg += str(length)+'或'
                                check_step = ''
                                check_text = f"區碼「{info['code']}」與市話開頭「{message[i:][0]}」正確，扣除區碼之市話長度不是「{lengthmsg[:-1]}」！"
                        else:
                            check_step = ''
                            check_text = f"「{info['code']}」區碼正確，市話號碼開頭錯誤！"
                        break
                if check_areacode == 'ok':
                    break#提早尋找到
            if check_areacode == 'no':
                check_step = ''
                check_text = f"輸入的「{message}」其中的區碼不在臺灣所規定的'固定通信網路服務'中，請再重新查核！"
        else:
            check_step = ''
            check_text = f"輸入的「{message}」不是區碼加市話的9或10碼，請再重新查核！"
    else:
        if message == '略過':
            check_step = 'ok'
            message_storage[id+'manufacturer_localcalls'] = message #市話暫存
            message_storage[id+'manufacturer_localcalls_code'] = '無' #區碼
            message_storage[id+'manufacturer_localcalls_num'] = '略過' #市話
            check_text = ''
        else:
            check_step = ''
            check_text = f"輸入的「{message}」不是市話的規則喔！"
    return check_text,check_step
###-------------------廠商電話檢查----------------------
def check_manufacturer_phonenum():
    id = manager.user_id
    message = manager.msg
    message_storage = manager.storage
    if message.isdigit():
        if(len(message) < 10):
            check_step = ''
            check_text =  f"輸入電話格式錯誤！(10碼)\n請重新打字輸入正確的電話號碼。"
        elif (len(message) > 10):
            check_step = ''
            check_text =  f"輸入電話格式錯誤！(10碼)\n請重新打字輸入正確的電話號碼。"
        elif(message[:2] != '09'):  
            check_step = ''         
            check_text =  f"輸入電話格式錯誤！(09開頭)\n請重新打字輸入正確的電話號碼。"
        else:
            message_storage[id+'manufacturer_phonenum'] = message #行動電話暫存
            check_step = 'ok'
            check_text = ''
    else:
        if message == '略過':
            check_step = 'ok'
            message_storage[id+'manufacturer_phonenum'] = message #行動電話暫存
            check_text = ''
        else:
            check_step = ''
            check_text = f"輸入的「{message}」不是行動電話的規則喔！"
    return check_text,check_step
###-------------------廠商付款方式檢查----------------------
def check_manufacturer_Payment():
    id = manager.user_id
    message = manager.msg
    message_storage = manager.storage
    if message in ['現金','匯款']:
        message_storage[id+'manufacturer_Payment'] = message #付款方式暫存
        if message == '匯款':
            check_step = 'ok'
            check_text = ''
        else:
            check_step = 'okend'
            message_storage[id+'manufacturer_bankid'] = "略過"
            message_storage[id+'manufacturer_bankname'] = "略過"
            message_storage[id+'manufacturer_bankaccount'] = "略過"
            check_text = ''
    else:
        check_step = ''
        check_text = f"輸入的「{message}」不是現金或匯款喔！"
    return check_text,check_step
###-------------------行庫/行庫代號檢查----------------------
def check_manufacturer_bank():
    id = manager.user_id
    message = manager.msg
    message_storage = manager.storage
    bankdata = bank()
    checkbank = 'no'
    if message.isdigit():
        if len(message) <= 3:
            for bankcheck in bankdata:
                if message == bankcheck['code']:
                    message_storage[id+'manufacturer_bankid'] = message #行庫代號暫存
                    message_storage[id+'manufacturer_bankname'] = bankcheck['name'] #行庫名稱暫存
                    checkbank = 'yes'
                    break
            if checkbank == 'yes':
                check_step = 'ok'
                check_text = ''
            else:
                check_step = ''
                check_text = f"輸入的代號「{message}」查無銀行！"  
        else:
            check_step = ''
            check_text = f"輸入的「{message}」不是銀行代號數字3碼！"
    else:       
        if len(message) <= 30:
            for bankcheck in bankdata:
                if message in bankcheck['name']:
                    message_storage[id+'manufacturer_bankid'] = bankcheck['code'] #行庫代號暫存
                    message_storage[id+'manufacturer_bankname'] = bankcheck['name'] #行庫名稱暫存
                    checkbank = 'yes'
                    break
            if checkbank == 'yes':
                check_step = 'ok'
                check_text = ''
            else:
                check_step = ''
                check_text = f"輸入的行庫名「{message}」查無銀行！"    
        else:
            check_step = ''
            check_text = f"輸入的「{message}」銀行行庫名大於30字！"
    return check_text,check_step
###-------------------廠商付款帳號檢查----------------------
def check_manufacturer_bankaccount():
    id = manager.user_id
    message = manager.msg
    message_storage = manager.storage
    if message.isdigit():
        if len(message) <= 14:
            if len(message) < 14:
                while len(message) < 14:
                    message = '0'+ message
            message_storage[id+'manufacturer_bankaccount'] = message #行庫帳號暫存
            check_step = 'ok'
            check_text = ''
        else:
            check_step = ''
            check_text = f"輸入的「{message}」不是數字3碼！"
    else:
        check_step = ''
        check_text = f"輸入的「{message}」不是數字3碼！"
    return check_text,check_step
#---------------------廠商管理結束--------------------
#---------------------商品管理-蓉---------------------
def product_modification():
    id = manager.user_id
    state = manager.user_state
    message = manager.msg
    product = manager.product
    product_status = product[id + 'Product_Modification_Product_status']#現預購狀態
    product_id = product.get(id + 'Product_Modification_Product_id')
    flex_message = None
    storage= manager.storage
    before_all = db_infotmation(product_id)
    
    if state[id] == 'Product_Modification_Product':#這邊是按鈕按下去後的流程
        info = message[8:]
        if '商品名稱' == info:
            state[id] = 'Product_Modification_Product_Pname'
            flex_message = TextSendMessage(text='(◍•ᴗ•◍)請輸入想修改的商品名稱:')
        elif '商品簡介' == info:
            state[id] = 'Product_Modification_Pintroduction'
            flex_message = TextSendMessage(text='(◍•ᴗ•◍)請輸入想修改的商品簡介:')
        elif '商品售出單價' == info:
            state[id] = 'Product_Modification_Punit_price_sold'
            flex_message = TextSendMessage(text='(◍•ᴗ•◍)請輸入想修改的商品售出單價:')
        elif '商品售出單價2'== info:
            state[id] = 'Product_Modification_Punit_price_sold2'
            flex_message = TextSendMessage(text='(◍•ᴗ•◍)請輸入想修改的商品售出單價2:')
        elif '預購倍數' == info:
            state[id] = 'Product_Modification_order_multiple'
            flex_message = TextSendMessage(text='(◍•ᴗ•◍)請輸入想修改的預購倍數:')
        elif '預購截止時間' == info:
            timeget = gettime()
            datetime = timeget['formatted_datetime2']#2023-10-18T21:00 用於LINE的格式
            state[id] = 'Product_Modification_order_deadline'
            template_message = FlexSendMessage(
                            alt_text='預購截止時間選擇',
                            contents={
                                "type": "carousel",
                                "contents": [{
                                "type": "bubble",
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "選擇日期時間",
                                        "weight": "bold",
                                        "size": "xl"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"(◍•ᴗ•◍)請輸入想修改的預購截止時間:",
                                        "wrap": True,
                                    }
                                    ]
                                },
                                "footer": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                    {
                                        "type": "button",
                                        "style": "link",
                                        "height": "sm",
                                        "action": {
                                        "type": "datetimepicker",
                                        "label": "點擊選擇日期與時間",
                                        "data": "預購截止時間",
                                        "mode": "datetime",
                                        "min": f"{datetime}"
                                        }
                                    }
                                    ],
                                    "flex": 0
                                }
                                }]   
                                } 
                            )
            flex_message = template_message
        elif '更換商品圖片' == info:
            state[id] = 'Product_Modification_Photo'
            flex_message = TextSendMessage(text='(◍•ᴗ•◍)請輸入新的商品圖片連結:')
        elif message == '取消':
            state[id] = 'normal'
            flex_message = TextSendMessage(text='已經取消囉！')
        else:
            flex_message = TextSendMessage(text=f'「{message}」錯誤內容指令')


        if message == '退出修改':
            state[id] = 'normal'
            flex_message = TextSendMessage(text='已經取消囉！')
        
    elif state[id] in ['Product_Modification_Product_Pname', 'Product_Modification_Pintroduction', 'Product_Modification_Punit_price_sold', 
                       'Product_Modification_Punit_price_sold2','Product_Modification_order_multiple','Product_Modification_order_deadline',
                       'Product_Modification_Photo']:
        #商品名稱,商品簡介,售出單價,售出單價2,預購數量限制_倍數,預購截止時間,商品圖片
        field_to_modify = None
        if state[id] == 'Product_Modification_Product_Pname':
            if before_all[0][0] == message:
                checkbefore = 'no'#不做資料庫
            else:
                field_to_modify = '商品名稱'
                checkbefore = 'ok'
        elif state[id] == 'Product_Modification_Pintroduction':
            if before_all[0][1] == message:
                checkbefore = 'no'#不做資料庫
            else:
                field_to_modify = '商品簡介'
                checkbefore = 'ok'
        elif state[id] == 'Product_Modification_Punit_price_sold':
            if before_all[0][2] == message:
                checkbefore = 'no'#不做資料庫
            else:
                field_to_modify = '售出單價'
                checkbefore = 'ok'
        elif state[id] == 'Product_Modification_Punit_price_sold2':
            if before_all[0][3] == message:
                checkbefore = 'no'#不做資料庫
            else:
                field_to_modify = '售出單價2'
                checkbefore = 'ok'
        elif state[id] == 'Product_Modification_order_multiple':
            if before_all[0][4] == message:
                checkbefore = 'no'#不做資料庫
            else:
                field_to_modify = '預購數量限制_倍數'
                checkbefore = 'ok'
        elif state[id] == 'Product_Modification_order_deadline':
            if before_all[0][5] == message:
                checkbefore = 'no'#不做資料庫
            else:
                field_to_modify = '預購截止時間'
                checkbefore = 'ok'
        elif state[id] == 'Product_Modification_Photo':
            if before_all[0][6] == message:
                checkbefore = 'no'#不做資料庫
            else:
                field_to_modify = '商品圖片'
                checkbefore = 'ok'

        if message != '取消':
            if checkbefore == 'ok':
                result = MP_information_modify(field_to_modify, message, product_id)
                if result == 'ok':
                    # flex_message = TextSendMessage(text=f'{field_to_modify} 修改成功！')
                    flex_message = get_product_modification_flex_message(product_status, product_id)
                else:
                    flex_message = TextSendMessage(text=f'{field_to_modify} 修改失敗，请稍后再试')
        else:
            flex_message = get_product_modification_flex_message(product_status, product_id)
        state[id] = 'Product_Modification_Product'
    return flex_message

def get_product_modification_flex_message(product_status, product_id):
    if product_status == '現購':
        return Now_Product_Modification_FM(product_id)
    elif product_status == '預購':
        return Pre_Product_Modification_FM(product_id)
    elif product_status == '預購進貨':
        return Pre_Product_Modification_FM(product_id)
    elif product_status == '預購未取':
        return Pre_Product_Modification_FM(product_id)
    elif product_status == '預購截止':
        return Pre_Product_Modification_FM(product_id)
    elif product_status == '查無':
        return TextSendMessage(text='商品有誤！')




#-------------------測試1111輸入進貨資訊-------------------
#-------------------廠商管理-新增廠商----------------------
def newing_purchaseinf():
    id = manager.user_id
    state = manager.user_state
    state1 = manager.user_state1
    message = manager.msg
    message_storage = manager.storage
    if message in ['取消','重新填寫']:
        message_storage[id + 'purchase_pid']= 'NAN'
        message_storage[id + 'purchase_num']= 'NAN'
        message_storage[id + 'purchase_cost']= 'NAN'
        message_storage[id + 'purchase_unit']= 'NAN'
        message_storage[id + 'purchase_time']= 'NAN'
        message_storage[id + 'give_money']= 'NAN'
        message_storage[id + 'money_time']= 'NAN'
        if message == '取消':
            state[id] = 'normal'
            check_text = TextSendMessage(text="取消輸入進貨資訊流程囉！")
        else:
            state1[id] = 'Purchase_num'#進貨數量
            message_storage[id+'Purchase_edit_step'] = 0
            check_text = Purchase_fillin_and_check_screen('')
    elif state1[id] == 'Purchase_num':
        textmsg,check_step = check_Purchase_num()#進貨數量檢查
        state1[id] = 'Purchase_cost' #進貨單價
        if check_step == 'ok':
            state1[id] = 'Purchase_cost' #進貨單價
            message_storage[id+'Purchase_edit_step'] = 1
            check_text = Purchase_fillin_and_check_screen('')
        else:
            check_text = Purchase_fillin_and_check_screen(textmsg)
    elif state1[id] == 'Purchase_cost':
        textmsg,check_step = check_Purchase_cost()#進貨單價檢查
        if check_step == 'ok':
            state1[id] = 'Purchase_end' #匯款金額0*1
            if message_storage[id + 'manu_payment'] != '現金':
                message_storage[id+'Purchase_edit_step'] = 2
                template_message = FlexSendMessage(
                                    alt_text='匯款時間選擇',
                                    contents={
                                        "type": "carousel",
                                        "contents": [{
                                        "type": "bubble",
                                        "body": {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": "選擇日期時間",
                                                "weight": "bold",
                                                "size": "xl"
                                            },
                                            {
                                                "type": "text",
                                                "text": f"{message_storage[id+'purchase_all']}\n=>請接著輸入「匯款時間」",
                                                "wrap": True,
                                                "color": "#3b5a5f",
                                                "weight": "bold"
                                            }
                                            ]
                                        },
                                        "footer": {
                                            "type": "box",
                                            "layout": "vertical",
                                            "spacing": "sm",
                                            "contents": [
                                            {
                                                "type": "button",
                                                "style": "link",
                                                "height": "sm",
                                                "action": {
                                                "type": "datetimepicker",
                                                "label": "點擊選擇日期與時間",
                                                "data": "新增進貨預購商品匯款時間",
                                                "mode": "datetime"
                                                }
                                            }
                                            ],
                                            "flex": 0
                                        }
                                        }]   
                                        } 
                                    )
                check_text = [Purchase_fillin_and_check_screen(''),template_message]
            else:
                message_storage[id+'Purchase_edit_step'] = 3
                message_storage[id+'money_time'] = 'NAN'
                check_text = Purchase_fillin_and_check_screen('')
        else:
            check_text = Purchase_fillin_and_check_screen(textmsg)
    elif state1[id] == 'Purchase_end':
        if message.isdigit():##
            if message in ['1','2']:
                if message == '1':
                    check = newingtopur_inf (message_storage[id+'purchase_pid'],
                                    message_storage[id+'purchase_num'],
                                    message_storage[id+'purchase_cost'],
                                    message_storage[id+'purchase_unit'],
                                    message_storage[id+'purchase_time'],
                                    message_storage[id+'give_money'],
                                    message_storage[id+'money_time'])
                    if check == 'ok':
                        check_text = Purchase_establishment_screen(message_storage[id+'purchase_pid'],
                                                                    message_storage[id+'purchase_num'],
                                                                    message_storage[id+'purchase_cost'],
                                                                    message_storage[id+'purchase_unit'],
                                                                    message_storage[id+'money_time'],
                                                                    message_storage[id+'give_money'],
                                                                    message_storage[id+'purchase_time'])
                    else:
                        check_text = TextSendMessage(text=f"進貨資訊流程失敗！")
                elif message == '2':
                    check_text = TextSendMessage(text="取消輸入進貨資訊流程囉！")
                state[id] = 'normal'
                message_storage[id + 'purchase_pid']= 'NAN'
                message_storage[id + 'purchase_num']= 'NAN'
                message_storage[id + 'purchase_cost']= 'NAN'
                message_storage[id + 'purchase_unit']= 'NAN'
                message_storage[id + 'purchase_time']= 'NAN'
                message_storage[id + 'give_money']= 'NAN'
                message_storage[id + 'money_time']= 'NAN'
            else:
                message_storage[id+'Purchase_edit_step'] = 5
                check_text = Purchase_fillin_and_check_screen(f"「{message}」不是此流程的內容喔！")
        else:
            message_storage[id+'Purchase_edit_step'] = 5
            check_text = Purchase_fillin_and_check_screen(f"「{message}」不是此流程的內容喔！")
    return check_text





#--------------檢查格式區--------------------------
###-------------------進貨數量檢查----------------------
def check_Purchase_num():
    id = manager.user_id
    message = manager.msg
    message_storage = manager.storage
    if message.isdigit() is not True or int(message) <= 0:
        check_step = ''
        check_text = f"輸入的「{message}」不是正確的格式或不是大於0的正整數！"
    else:
        message_storage[id+'purchase_num'] = int(message) #進貨數量暫存
        check_step = 'ok'
        check_text = ''
    return check_text,check_step
def check_Purchase_cost():
    id = manager.user_id
    message = manager.msg
    message_storage = manager.storage
    if message.isdigit() is not True or int(message) <= 0:
        check_step = ''
        check_text = f"輸入的「{message}」不是正確的格式或不是大於0的正整數！"
    else:
        message_storage[id+'purchase_cost'] = int(message) #進貨單價暫存
        check_step = 'ok'
        check_text = ''
    return check_text,check_step

def searchingOrderByPhoneNumber():
     # 若使用者已經在等待回覆狀態，則根據回覆進行處理
    id = manager.user_id
    message = manager.msg
    state = manager.user_state
    state1 = manager.user_state1
    global_Storage = manager.global_Storage
    
    if state1[id] =='first':
        global_Storage[id+'base'] = 0
        actions = []
        global_Storage[id+'orders'] = database.getPhoneNumberByPhoneNumberLastThreeYard(message)
        # global_Storage[id+'orders'] = a
        if global_Storage[id+'orders'] == []:
            check_text = TextSendMessage(text='找不到符合條件的資料')
            state[id] = 'normal'
        else:            
            for option in global_Storage[id+'orders'][global_Storage[id+'base']:global_Storage[id+'base']+10]:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            if len(global_Storage[id+'orders'])>global_Storage[id+'base']+10:
                actions.append(QuickReplyButton(action=MessageAction(label='下一頁', text='下一頁')))
            check_text=TextSendMessage(text='請選擇電話', quick_reply=QuickReply(items=actions))
            state1[id] = 'second'
    elif state1[id] == 'second':
        if message == '下一頁':
            actions = []
            global_Storage[id+'base']+=10
            for option in global_Storage[id+'orders'][global_Storage[id+'base']:global_Storage[id+'base']+10]:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            if len(global_Storage[id+'orders'])>global_Storage[id+'base']+10:
                actions.append(QuickReplyButton(action=MessageAction(label='下一頁', text='下一頁')))
            check_text=TextSendMessage(text='請選擇電話', quick_reply=QuickReply(items=actions))
        else:
            global_Storage[id+'base'] = 0
            check_text = TemplateSendMessage(
                    alt_text='取貨選擇',
                    template=ConfirmTemplate(
                        text='請選擇取貨方式：\n【全部領取】或是【分開領】',
                        actions=[
                            MessageAction(
                                label='【全部領取】',
                                text='全部領取'+message,
                            ),
                            MessageAction(
                                label='【分開領】',
                                text='分開領'+message
                            )
                        ]
                    )
                )
            state1[id]='third'
    elif state1[id] == 'third':
        if message[:3] == '分開領':
            actions = []
            global_Storage[id+'orders'] = database.getOrderByPhoneNumber(message[3:])
            for option in global_Storage[id+'orders'][global_Storage[id+'base']:global_Storage[id+'base']+10]:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            if len(global_Storage[id+'orders'])>global_Storage[id+'base']+10:
                actions.append(QuickReplyButton(action=MessageAction(label='下一頁', text='下一頁')))
            check_text=TextSendMessage(text='請選擇訂單', quick_reply=QuickReply(items=actions))

        else:
            if message == '下一頁':
                actions = []
                global_Storage[id+'base']+=10
                for option in global_Storage[id+'orders'][global_Storage[id+'base']:global_Storage[id+'base']+10]:
                    actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
                if len(global_Storage[id+'orders'])>global_Storage[id+'base']+10:
                    actions.append(QuickReplyButton(action=MessageAction(label='下一頁', text='下一頁')))
                return TextSendMessage(text='請選擇訂單', quick_reply=QuickReply(items=actions))
            elif message[:4]== '全部領取':
                
                global_Storage[id+'orders'] = database.getOrderDetailByPhoneNumber(message[4:])
                global_Storage[id+'order'] = message[4:]
            else:
                global_Storage[id+'base']=0
                global_Storage[id+'orders'] = database.getOrderDetailByOrder(message)
                global_Storage[id+'order'] = message
            check_text = FM.showOrder()
            state1[id] = 'end'
    elif state1[id] == 'end':
        if message == '下一頁':
            global_Storage[id+'base']+=10
            check_text = FM.showOrder()
            return check_text
        elif '【確認】' in message:
            database.updateOrder(id)
            check_text = TextSendMessage(text='取貨成功')
        else:
            check_text = TextSendMessage(text='取貨取消')
        state[id] = 'normal'
        global_Storage[id+'base'] = 0
    return check_text

def createNowProduct():
    id = manager.user_id
    state = manager.user_state
    state1 = manager.user_state1
    message = manager.msg
    global_Storage = manager.global_Storage
    options = ['frozen', 'dailyuse', 'dessert', 'local', 'staplefood', 'generally', 'beauty', 'snack', 'healthy', 'drinks','test']
    units=['個','包','盒','桶','公克','公斤','組','箱','帶']
    returnoptions = ['可退','可換','退換','空白']
    if state1[id] == 'first':
        if len(message) > 50:
            check_text = ('您輸入的品名超過50字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text
        global_Storage[id+'pname'] = '品名：'+ message
        check_text = ('您輸入的品名： %s' %(message))
        check_text += '\n=>請接著輸入「商品類別」'
        
        actions=[]
        for option in options:
           actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
        check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
        state1[id] = 'one'
    elif state1[id] == 'one':
        if message not in options:
            check_text = ('您輸入的類別錯誤，請重新輸入')
            actions=[]
            for option in options:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
            return check_text
        global_Storage[id+'category'] = '商品類別:' + message
        check_text = ('%s\n %s' %(global_Storage[id+'pname'],global_Storage[id+'category']))
        check_text += '\n=>請接著選擇「商品單位'
        actions=[]
        for option in units:
           actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
        check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
        state1[id] = 'two'
    elif state1[id] == 'two':
        if message not in units :
            check_text = ('您輸入的單位錯誤，請重新輸入')
            actions=[]
            for option in units:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
            return check_text
        global_Storage[id+'unit'] = '商品單位：' + message
        check_text = ('%s\n%s\n%s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit']))
        check_text += '\n=>請接著輸入「商品簡介」(小於150字)'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'three'
    elif state1[id] == 'three':
        if len(message) > 150:
            check_text = ('您輸入的商品簡介超過50字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text
        global_Storage[id+'introduction'] = '商品簡介：' + message
        check_text = ('%s\n%s\n%s\n %s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction']))
        check_text += '\n=>請接著輸入「商品售出單價」'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'four'
    elif state1[id] == 'four':
        if not message.isdigit():
            check_text = ('您輸入的商品售出單價不是數字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text
        global_Storage[id+'unitPrice'] = '商品售出單價：' + message
        check_text = ('%s\n%s\n%s\n%s\n%s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction'],global_Storage[id+'unitPrice']))
        check_text += '\n=>請接著輸入「商品售出單價2」'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'five'
    elif state1[id] == 'five':
        if not message.isdigit():
            check_text = ('您輸入的商品售出單價2不是數字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text        
        global_Storage[id+'unitPrice2'] = '商品售出單價2：' + message
        check_text = ('%s\n%s\n%s\n%s\n%s\n %s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction'],global_Storage[id+'unitPrice'],global_Storage[id+'unitPrice2']))
        check_text += '\n=>請接著輸入「商品圖片」'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'six'
    elif state1[id] == 'six':
        global_Storage[id+'picture'] = '商品圖片：' + message
        check_text = ('%s\n%s\n%s\n%s\n%s\n%s\n%s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction'],global_Storage[id+'unitPrice'],global_Storage[id+'unitPrice2'],global_Storage[id+'picture']))
        check_text += '\n=>請接著選擇「可否退換貨」'
        actions=[]
        for option in returnoptions:
           actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
        check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
        state1[id] = 'seven'
    elif state1[id] == 'seven':
        if message not in returnoptions:
            check_text = ('您輸入的可否退換貨錯誤，請重新輸入')
            actions=[]
            for option in returnoptions:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
            return check_text
        global_Storage[id+'returnProduct'] = '可否退換貨：' + message
        check_text = ('%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction'],global_Storage[id+'unitPrice'],global_Storage[id+'unitPrice2'],global_Storage[id+'picture'],global_Storage[id+'returnProduct']))
        state1[id] = 'ShowFM'
    elif state1[id] == 'changePname':
        if len(message) > 50:
            check_text = ('您輸入的品名超過50字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text
        state1[id] = 'ShowFM' 
        global_Storage[id+'pname'] ='品名:'+ message

    elif state1[id] == 'changeCategory':
         if message not in options:
            check_text = ('您輸入的類別錯誤，請重新輸入')
            actions=[]
            for option in options:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
            return check_text
         state1[id] = 'ShowFM'
         global_Storage[id+'category'] ='商品類別:'+ message        
    elif state1[id] == 'changeUnit':
        if message not in units :
            check_text = ('您輸入的單位錯誤，請重新輸入')
            actions=[]
            for option in units:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
            return check_text
        state1[id] = 'ShowFM'
        global_Storage[id+'unit'] ='商品單位:'+ message
    elif state1[id] == 'changeIntroduction':
        if len(message) > 150:
            check_text = ('您輸入的商品簡介超過50字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text
        state1[id] = 'ShowFM'
        global_Storage[id+'introduction'] ='商品簡介:'+ message
    elif state1[id] == 'changeUnitPrice':
        if not message.isdigit():
            check_text = ('您輸入的商品售出單價不是數字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text
        state1[id] = 'ShowFM'
        global_Storage[id+'unitPrice'] = '商品售出單價:'+message
    elif state1[id] == 'changeUnitPrice2':
        if not message.isdigit():
            check_text = ('您輸入的商品售出單價2不是數字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text  
        state1[id] = 'ShowFM'
        global_Storage[id+'unitPrice2'] = '商品售出單價2:'+message
    elif state1[id] == 'changePicture':
        state1[id] = 'ShowFM'
        global_Storage[id+'picture'] = '商品圖片'+message
    elif state1[id] == 'changeReturnProduct':
        if message not in returnoptions:
            check_text = ('您輸入的可否退換貨錯誤，請重新輸入')
            actions=[]
            for option in returnoptions:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
            return check_text
        state1[id] = 'ShowFM'
        global_Storage[id+'returnProduct'] = '可否退換貨:'+message
    if state1[id] == 'ShowFM':
        if(message=='修改品名'):
            check_text = '請輸入品名(少於50字)'
            state1[id] = 'changePname'
            check_text = TextSendMessage(text=check_text)
        if(message=='修改商品類別'):
            check_text = '請選擇商品類別'
            actions=[]
            for option in options:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
            state1[id] = 'changeCategory'
        if(message=='修改商品單位'):
            check_text = '請選擇商品單位'
            state1[id] = 'changeUnit'
            actions=[]
            for option in units:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
        if(message=='修改商品簡介'):
            check_text = '請輸入商品簡介(少於150字)'
            state1[id] = 'changeIntroduction'
            check_text = TextSendMessage(text=check_text)
        if(message=='修改商品售出單價'):
            check_text = '請輸入商品售出單價'
            state1[id] = 'changeUnitPrice'
            check_text = TextSendMessage(text=check_text)
        if(message=='修改商品售出單價2'):
            check_text = '請輸入商品售出單價2'
            state1[id] = 'changeUnitPrice2'
            check_text = TextSendMessage(text=check_text)
        if(message=='修改商品圖片'):
            check_text = '請輸入商品圖片'
            state1[id] = 'changePicture'
            check_text = TextSendMessage(text=check_text)
        if(message=='修改可否退換貨'):
            check_text = '請選擇可否退換貨'
            state1[id] = 'changeReturnProduct'
            check_text = ('您輸入的單位錯誤，請重新輸入')
            actions=[]
            for option in returnoptions:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
            return check_text
        if(message == '建立商品'):
            global_Storage[id+'createType'] = 'now'
            database.createProduct(id)
            check_text = TextSendMessage(text='商品建立成功')
            state[id]= 'normal'
        elif(state1[id] == 'ShowFM'):
            check_text = FM.create_now_purchase_product(id)
        
    

    return check_text
def createPreOrder():
    id = manager.user_id    
    state = manager.user_state
    state1 = manager.user_state1
    message = manager.msg
    global_Storage = manager.global_Storage
    options = ['frozen', 'dailyuse', 'dessert', 'local', 'staplefood', 'generally', 'beauty', 'snack', 'healthy', 'drinks','test']
    units=['個','包','盒','桶','公克','公斤','組','箱','帶']
    if state1[id] == 'first':
        if len(message) > 50:
            check_text = ('您輸入的品名超過50字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text
        global_Storage[id+'pname'] = '品名：'+ message
        check_text = ('您輸入的品名： %s' %(message))
        check_text += '\n=>請接著選擇「商品類別」'
        
        actions=[]
        for option in options:
           actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
        check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
        state1[id] = 'one'
    elif state1[id] == 'one':
        if message not in options:
            check_text = ('您輸入的類別錯誤，請重新輸入')
            actions=[]
            for option in options:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
            return check_text
        global_Storage[id+'category'] = '商品類別:' + message
        check_text = ('%s\n %s' %(global_Storage[id+'pname'],global_Storage[id+'category']))
        check_text += '\n=>請接著選擇「商品單位」'
        actions=[]
        for option in units:
           actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
        check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
        state1[id] = 'two'
    elif state1[id] == 'two':
        if message not in units :
            check_text = ('您輸入的單位錯誤，請重新輸入')
            actions=[]
            for option in units:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
            return check_text
        global_Storage[id+'unit'] = '商品單位：' + message
        check_text = ('%s\n%s\n%s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit']))
        check_text += '\n=>請接著輸入「商品簡介」(少於150字)'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'three'
    elif state1[id] == 'three':
        if len(message) > 150:
            check_text = ('您輸入的商品簡介超過50字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text
        global_Storage[id+'introduction'] = '商品簡介：' + message
        check_text = ('%s\n%s\n%s\n %s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction']))
        check_text += '\n=>請接著輸入「商品售出單價」'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'four'
    elif state1[id] == 'four':
        if not message.isdigit():
            check_text = ('您輸入的商品售出單價不是數字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text
        global_Storage[id+'unitPrice'] = '商品售出單價：' + message
        check_text = ('%s\n%s\n%s\n%s\n%s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction'],global_Storage[id+'unitPrice']))
        check_text += '\n=>請接著輸入「商品售出單價2」'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'five'
    elif state1[id] == 'five':
        if not message.isdigit():
            check_text = ('您輸入的商品售出單價2不是數字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text
        global_Storage[id+'unitPrice2'] = '商品售出單價2：' + message
        check_text = ('%s\n%s\n%s\n%s\n%s\n %s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction'],global_Storage[id+'unitPrice'],global_Storage[id+'unitPrice2']))
        check_text += '\n=>請接著輸入「商品圖片」'
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'six'
        global_Storage[id+'check'] = 0
    elif state1[id] == 'six':
        if(global_Storage[id+'check'] == 1):
            global_Storage[id+'picture'] = '商品圖片：' + message
            check_text = ('%s\n%s\n%s\n%s\n%s\n%s\n%s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction'],global_Storage[id+'unitPrice'],global_Storage[id+'unitPrice2'],global_Storage[id+'picture']))
            check_text += '\n=>請接著輸入「商品預購截止時間」'
            timeget = gettime()
            datetime = timeget['formatted_datetime2']#2023-10-18T21:00 用於LINE的格式
            check_text = [TextSendMessage(text='輸入錯誤'),FM.template_message(check_text,datetime)]
        else:
            global_Storage[id+'picture'] = '商品圖片：' + message
            check_text = ('%s\n%s\n%s\n%s\n%s\n%s\n%s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction'],global_Storage[id+'unitPrice'],global_Storage[id+'unitPrice2'],global_Storage[id+'picture']))
            check_text += '\n=>請接著輸入「商品預購截止時間」'
            timeget = gettime()
            datetime = timeget['formatted_datetime2']#2023-10-18T21:00 用於LINE的格式
            check_text = [FM.template_message(check_text,datetime)]
            global_Storage[id+'check'] = 1
        # state1[id] = 'seven'
    elif state1[id] == 'seven':
        # 加上判斷
        global_Storage[id+'deadline'] = '商品預購截止時間：' + message
        check_text = ('%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction'],global_Storage[id+'unitPrice'],global_Storage[id+'unitPrice2'],global_Storage[id+'picture'],global_Storage[id+'deadline']))
        check_text += '\n=>請接著輸入「商品預購倍數」'
        check_text = TextSendMessage(text=check_text)
        
        state1[id] = 'eight'
    elif state1[id] == 'eight':
        if not message.isdigit():
            check_text = ('您輸入的商品預購倍數不是數字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text
        global_Storage[id+'multiple'] = '商品預購倍數：' + message
        check_text = ('%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' %(global_Storage[id+'pname'],global_Storage[id+'category'],global_Storage[id+'unit'],global_Storage[id+'introduction'],global_Storage[id+'unitPrice'],global_Storage[id+'unitPrice2'],global_Storage[id+'picture'],global_Storage[id+'deadline'],global_Storage[id+'multiple']))
        check_text = TextSendMessage(text=check_text)
        global_Storage[id+'tag'] = 'nil'
        state1[id] = 'ShowFM'
    elif state1[id] == 'changePname':
        if len(message) > 50:
            check_text = ('您輸入的品名超過50字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text
        state1[id] = 'ShowFM' 
        global_Storage[id+'pname'] ='品名:'+ message
    elif state1[id] == 'changeCategory':
         if message not in options:
            check_text = ('您輸入的類別錯誤，請重新輸入')
            actions=[]
            for option in options:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
            return check_text
         state1[id] = 'ShowFM'
         global_Storage[id+'category'] ='商品類別:'+ message        
    elif state1[id] == 'changeUnit':
        if message not in units :
            check_text = ('您輸入的單位錯誤，請重新輸入')
            actions=[]
            for option in units:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
            return check_text
        state1[id] = 'ShowFM'
        global_Storage[id+'unit'] ='商品單位:'+ message
    elif state1[id] == 'changeIntroduction':
        if len(message) > 150:
            check_text = ('您輸入的商品簡介超過50字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text
        state1[id] = 'ShowFM'
        global_Storage[id+'introduction'] ='商品簡介:'+ message
    elif state1[id] == 'changeUnitPrice':
        if not message.isdigit():
            check_text = ('您輸入的商品售出單價不是數字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text
        state1[id] = 'ShowFM'
        global_Storage[id+'unitPrice'] = '商品售出單價:'+message
    elif state1[id] == 'changeUnitPrice2':
        if not message.isdigit():
            check_text = ('您輸入的商品售出單價2不是數字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text
        state1[id] = 'ShowFM'
        global_Storage[id+'unitPrice2'] = '商品售出單價2:'+message
    elif state1[id] == 'changePicture':
        state1[id] = 'ShowFM'
        global_Storage[id+'picture'] = '商品圖片'+message
    elif state1[id] == 'changeDeadline':
        # state1[id] = 'ShowFM'
        global_Storage[id+'deadline'] = '商品預購截止時間:'+message
    elif state1[id] == 'changeMultiple':
        if not message.isdigit():
            check_text = ('您輸入的商品預購倍數不是數字，請重新輸入')
            check_text = TextSendMessage(text=check_text)
            return check_text
        state1[id] = 'ShowFM'
        global_Storage[id+'multiple'] = '商品預購倍數:'+message
    if state1[id] == 'ShowFM':
        if(message=='修改品名'):
            check_text = '請輸入品名(少於50字)'
            state1[id] = 'changePname'
            check_text = TextSendMessage(text=check_text)
        if(message=='修改商品類別'):
            check_text = '請選擇商品類別'
            actions=[]
            for option in options:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
            state1[id] = 'changeCategory'
        if(message=='修改商品單位'):
            check_text = '請選擇商品單位'
            state1[id] = 'changeUnit'
            actions=[]
            for option in units:
                actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
            check_text=TextSendMessage(text=check_text, quick_reply=QuickReply(items=actions))
        if(message=='修改商品簡介'):
            check_text = '請輸入商品簡介(少於150字)'
            state1[id] = 'changeIntroduction'
            check_text = TextSendMessage(text=check_text)
        if(message=='修改商品售出單價'):
            check_text = '請輸入商品售出單價'
            state1[id] = 'changeUnitPrice'
            check_text = TextSendMessage(text=check_text)
        if(message=='修改商品售出單價2'):
            check_text = '請輸入商品售出單價2'
            state1[id] = 'changeUnitPrice2'
            check_text = TextSendMessage(text=check_text)
        if(message=='修改商品圖片'):
            check_text = '請輸入商品圖片'
            state1[id] = 'changePicture'
            check_text = TextSendMessage(text=check_text)
        if(message=='修改商品預購截止時間'):
            check_text = '請輸入商品預購截止時間'
            state1[id] = 'changeDeadline'
            timeget = gettime()
            datetime = timeget['formatted_datetime2']#2023-10-18T21:00 用於LINE的格式
            check_text = FM.template_message(check_text,datetime)
        if(message=='修改商品預購倍數'):
            check_text = '請輸入商品預購倍數'
            state1[id] = 'changeMultiple'
            check_text = TextSendMessage(text=check_text)
        if(message == '建立商品'):
            global_Storage[id+'createType'] = 'pre'
            database.createProduct(id)
            check_text = TextSendMessage(text='商品建立成功')
            state[id]= 'normal'
        elif(state1[id] == 'ShowFM'):
            check_text = FM.create_preorder(id)

    return check_text

def preAndNowSelect():
    user_state = manager.user_state
    user_state1 = manager.user_state1
    user_id = manager.user_id
    msg = manager.msg
    if msg == '現購':
        user_state[user_id] = 'createNowProduct'
        user_state1[user_id] = 'first'
        check_text = TextSendMessage(text='請輸入商品名稱(低於50字)')
    elif msg =='預購':
        user_state[user_id] = 'createPreOrder'
        user_state1[user_id] = 'first'
        check_text = TextSendMessage(text='請輸入商品名稱(低於50字)')
    return check_text