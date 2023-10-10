from linebot.models import *
from linebot.models import TextSendMessage
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import TemplateSendMessage, ButtonsTemplate, MessageAction,DatetimePickerAction
from linebot.models import *
from datetime import datetime, timedelta
import manager
from database import *
from flexmsg import *


message_storage = {}


def purchase_check():
    id = manager.user_id
    state = manager.user_state

    if state[id] == 'purchase_ck':
        check_texts = nepurchase_info()
    elif state[id] == 'repurchase_ck':
        check_texts = renepurchase_info()
    return check_texts

def nepurchase_info():
    id = manager.user_id
    state = manager.user_state
    state1 = manager.user_state1
    message = manager.msg

    #if message.isdigit():
    if message == '取消':
        state[id] = 'normal'
        state1[id] = 'NAN'
    elif state1[id] == 'num':
        message_storage[id + 'purchase_num'] = int(message)
        message_storage[id+'purchase_all'] += f'\n您輸入的進貨數量： {message}'
        check_text = f"{message_storage[id+'purchase_all']}\n=>請接著輸入「進貨單價」"
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'cost'
    elif state1[id] == 'cost':
        message_storage[id + 'purchase_cost'] = int(message)
        message_storage[id+'purchase_all'] += f'\n您輸入的進貨單價： {message}'
        check_text = f"{message_storage[id+'purchase_all']}\n=>請接著輸入「進貨時間」"
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'ptime'
    elif state1[id] == 'ptime':
        message_storage[id + 'purchase_time'] = message
        message_storage[id+'purchase_all'] += f'\n您輸入的進貨時間： {message}'
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
            purchase_pid = message_storage[id + "purchase_pid"].strip('{}')
            check_text = check_ok(purchase_pid)
        else:
            check_text = '進貨失敗！稍後再試'
            check_text = TextSendMessage(text=check_text)
        state[id] = 'normal'
        state1[id] = 'NAN'
    return check_text




##1011可成功連接
def renepurchase_info():
    id = manager.user_id
    state = manager.user_state
    state1 = manager.user_state1
    message = manager.msg

    #if message.isdigit():
    if message == '取消':
        state[id] = 'normal'
        state1[id] = 'NAN'
    elif state1[id] == 'num':
        message_storage[id + 'purchase_num'] = int(message)
        message_storage[id+'purchase_all'] += f'\n您修改的進貨數量： {message}'
        check_text = f"{message_storage[id+'purchase_all']}\n=>請接著輸入「進貨單價」"
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'cost'
    elif state1[id] == 'cost':
        message_storage[id + 'purchase_cost'] = int(message)
        message_storage[id+'purchase_all'] += f'\n您輸入的進貨單價： {message}'
        check_text = f"{message_storage[id+'purchase_all']}\n=>請接著輸入「進貨時間」"
        check_text = TextSendMessage(text=check_text)
        state1[id] = 'ptime'
    elif state1[id] == 'ptime':
        message_storage[id + 'purchase_time'] = message
        message_storage[id+'purchase_all'] += f'\n您輸入的進貨時間： {message}'
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
            message_storage[id + 'purchase_time'],
            message_storage[id + 'give_money'],
            message_storage[id + 'money_time']
        )
        if result == 'ok':
            check_text = f'您已成功快速進貨商品{message_storage[id + "purchase_pid"]}' 
        else:
            check_text = '快速進貨失敗！稍後再試'
        check_text = TextSendMessage(text=check_text)
        state[id] = 'normal'
        state1[id] = 'NAN'
    return check_text