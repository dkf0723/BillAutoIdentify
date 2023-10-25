from linebot.models import *
from linebot.models import TextSendMessage
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import TemplateSendMessage, ButtonsTemplate, MessageAction,DatetimePickerAction
from linebot.models import *
from datetime import datetime, timedelta
import manager
import pytz
from database import *
from flexmsg import *
###廠商管理---
from relevant_information import bank,Citytalk#廠商建立用，未來拔掉
from manufacturerFM import Manufacturer_fillin_and_check_screen,Manufacturer_establishment_screen,Manufacturer_edit_screen #廠商建立用，未來拔掉
from vendor_management import Manufacturer_edit,Manufacturer_list#廠商建立用，未來拔掉
#----


message_storage = {}


def purchase_check():
    id = manager.user_id
    state = manager.user_state
    if state[id] == 'pre_purchase_ck':
        check_texts = nepurchase_info()
    elif state[id] == 'purchasing_ck':
        check_texts = ingnepurchase_info()
    elif state[id] == 'repurchase_ck':
        check_texts = renepurchase_info()
    #-------------------廠商管理-新增廠商----------------------
    elif state[id] in ['manufacturer_name','other_manufacturer_add','manufacturer_principal',
                       'manufacturer_localcalls','manufacturer_phonenum','manufacturer_Payment',
                       'manufacturer_bank','manufacturer_bankaccount','manufacturer_end']:#新增廠商
        check_texts = new_manufacturer()#single_manufacturer_num單獨建立；other_manufacturer新商品新廠商過來的
    elif state[id] == 'manufacturereditall':
        check_texts = Manufacturereditall_check()
    elif 'manufacturer_edit_' in state[id]:
        check_texts = manufacturer_editinfo()
    #-----------------------------------------
    return check_texts

#新增預購進貨
def nepurchase_info():
    id = manager.user_id
    state = manager.user_state
    state1 = manager.user_state1
    message = manager.msg
    message_storage = manager.storage
    
    if message == '取消':
        state[id] = 'normal'
        state1[id] = 'NAN'
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
                                            "data": "匯款時間",
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
            check_text = '進貨預購商品成功！'
            check_text = TextSendMessage(text=check_text)
        else:
            check_text = '進貨預購商品失敗！稍後再試' 
            check_text = TextSendMessage(text=check_text)
        state[id] = 'normal'
        state1[id] = 'NAN'
    return check_text

















###########新增現購
def ingnepurchase_info():
    id = manager.user_id
    state = manager.user_state
    state1 = manager.user_state1
    message = manager.msg
    message_storage = manager.storage
    #if message.isdigit():
    if message == '取消':
        state[id] = 'normal'
        state1[id] = 'NAN'
    elif state1[id] == 'num':
        message_storage[id + 'purchase_num'] = int(message)
        message_storage[id+'purchase_all'] = f'\n您輸入的進貨數量： {message}'
        check_text = f"{message_storage[id+'purchase_all']}\n=>請接著輸入「進貨單價」"
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'cost'
    elif state1[id] == 'cost':
        message_storage[id + 'purchase_cost'] = int(message)
        message_storage[id+'purchase_all'] += f'\n您輸入的進貨單價： {message}'
        if message_storage[id + 'dbmanuinf'] == 'ok':
            #商品ID, 現預購商品, 付款方式, 行庫名, 行庫代號, 匯款帳號
            '''
            message_storage[id + 'dbmanuinf'][0][1]
            message_storage[id + 'dbmanuinf'][0][2]
            message_storage[id + 'dbmanuinf'][0][3]
            message_storage[id + 'dbmanuinf'][0][4]
            message_storage[id + 'dbmanuinf'][0][5]'''
            #if message_storage[id + 'dbmanuinf'][0][2] == '現金':
            template_message = FlexSendMessage(
                                alt_text='進貨時間選擇',
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
                                            "text": f"{message_storage[id+'purchase_all']}\n=>請接著輸入「進貨時間」",
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
                                            "data": "進貨時間",
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
            state1[id] = 'ptime'
        else:
            check_text = TextSendMessage(text='商品出現問題，請稍後再試！')
    elif state1[id] == 'ptime':
        check_text = f"{message_storage[id+'purchase_all']}\n=>請接著輸入「匯款金額」"
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'mmoney'
    elif state1[id] == 'mmoney':
        message_storage[id + 'give_money'] = int(message)
        message_storage[id+'purchase_all'] += f'\n您輸入的匯款金額： {message}'
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
                                        "data": "匯款時間",
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
    elif state1[id] == 'mtime':
        message_storage[id + 'money_time'] = message
        message_storage[id+'purchase_all'] += f'\n您輸入的匯款時間： {message}\n確認後請輸入OK'
        check_text = f"{message_storage[id+'purchase_all']}"
        check_text = TextSendMessage(text=check_text)
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
            purchase_pid = message_storage[id + "purchase_pid"]
            check_text = check_okok(purchase_pid)
        else:
            check_text = '進貨現購商品失敗！稍後再試'
            check_text = TextSendMessage(text=check_text)
        state[id] = 'normal'
        state1[id] = 'NAN'
    return check_text

def renepurchase_info():
    id = manager.user_id
    state = manager.user_state
    state1 = manager.user_state1
    message = manager.msg
    message_storage = manager.storage
    #if message.isdigit():
    if message == '取消':
        state[id] = 'normal'
        state1[id] = 'NAN'
    elif state1[id] == 'num':
        message_storage[id + 'purchase_num'] = int(message)
        message_storage[id+'purchase_all'] = f'\n您輸入的進貨數量： {message}'
        check_text = f"{message_storage[id+'purchase_all']}\n=>請接著輸入「進貨單價」"
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'cost'
    elif state1[id] == 'cost':
        message_storage[id + 'purchase_cost'] = int(message)
        purchase_num = message_storage[id + 'purchase_num']
        purchase_cost = message_storage[id + 'purchase_cost']
        payment_amount = purchase_num * purchase_cost
        message_storage[id + 'give_money'] = payment_amount
        message_storage[id + 'purchase_all'] += f'\n您輸入的進貨單價： {message}'
        message_storage[id + 'purchase_all'] += f'\n您輸入的匯款金額： {payment_amount}'  # 這裡顯示計算出的支付金額
        template_message = FlexSendMessage(
                            alt_text='進貨時間選擇',
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
                                        "text": f"{message_storage[id+'purchase_all']}\n=>請接著輸入「進貨時間」",
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
                                        "data": "進貨時間",
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
        state1[id] = 'ptime'
    elif state1[id] == 'ptime':
        check_text = f"{message_storage[id+'purchase_all']}\n=>請接著輸入「匯款金額」"
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'mmoney'
    elif state1[id] == 'mmoney':
        message_storage[id + 'give_money'] = int(message)
        message_storage[id+'purchase_all'] += f'\n您輸入的匯款金額： {message}'
        check_text = f"{message_storage[id+'purchase_all']}\n=>請接著輸入「匯款時間」"
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'mtime'
    elif state1[id] == 'mtime':
        message_storage[id + 'money_time'] = message
        message_storage[id+'purchase_all'] += f'\n您輸入的匯款時間： {message}\n確認後請輸入OK'
        check_text = f"{message_storage[id+'purchase_all']}"
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'end'
    elif state1[id] == 'end':
        if message in ['ok','Ok','oK','OK']:
            result = quick_pur_inf(
            message_storage[id + 'purchase_pid'],
            message_storage[id + 'purchase_num'],
            message_storage[id + 'purchase_cost'],
            message_storage[id + 'purchase_unit'],
            message_storage[id + 'purchase_time'],
            message_storage[id + 'give_money'],
            message_storage[id + 'money_time']
        )
        if result == 'ok':
            purchase_pid = message_storage[id + "purchase_pid"]
            check_text = checkquick_ok(purchase_pid)
        else:
            check_text = '快速進貨失敗！稍後再試'
            check_text = TextSendMessage(text=check_text)
        state[id] = 'normal'
        state1[id] = 'NAN'
    return check_text

##快速進貨

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
    addtype = 'single'
    if state[id] == 'other_manufacturer_add':
        addtype = 'other'#最後判斷是否狀態回給新商品建立下一步狀態
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


