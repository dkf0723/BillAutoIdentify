from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from product.buy_now import *
from product.product_preorder import *
import lineboterp
from ask_wishes.ask import *
from ask_wishes.wishes import *
from database import *
from product.cartlist import cart_list,addcart,cartrevise,checkcart
from selection_screen import (Order_phonenum_screen,Single_order_confirmation_screen,Order_establishment_message,
                              Cart_join_success_message,Cancel_fail_message,Cart_order_screen,Cartordercheck_establishment_message,
                              Cartorder_establishment_message)
###---
from relevant_information import bank,Citytalk#廠商建立用，未來拔掉
from FM import Manufacturer_fillin_and_check_screen,Manufacturer_establishment_screen,Manufacturer_edit_screen #廠商建立用，未來拔掉
from vendor_management import Manufacturer_edit#廠商建立用，未來拔掉
#----

#-------------------使用者狀態檢查----------------------
def product_check():
    id = lineboterp.user_id
    state = lineboterp.user_state
     #判斷user狀態
    if state[id] in ['ordering','preorder','phonenum','end']: #單筆訂預購
        check_text = orderandpreorder_check()
    elif state[id] == 'cartnum':#新增購物車
        check_text = cartnum()
    elif state[id] == 'cartrevise':#修改購物車單項商品數量
        check_text = cartrpnum()
    elif state[id] in ['cartorderphonenum','cartorderrun']:#購物車訂單
        check_text = cartorder()
    elif state[id] == 'ask':#QA
        check_text = ask()
    elif state[id] in ['wishes','wishesreason','wishessource','wishesimg','wishescheck']:#願望清單
        check_text = wishes()
    #-------------------廠商管理-新增廠商----------------------
    elif state[id] in ['manufacturer_name','other_manufacturer_add','manufacturer_principal',
                       'manufacturer_localcalls','manufacturer_phonenum','manufacturer_Payment',
                       'manufacturer_bank','manufacturer_bankaccount','manufacturer_end']:#新增廠商
        check_text = new_manufacturer()#single_manufacturer_num單獨建立；other_manufacturer新商品新廠商過來的
    elif 'manufacturer_edit_' in state[id]:
        check_text = manufacturer_editinfo()
    #-----------------------------------------
    return check_text

#-------------------廠商管理-新增廠商----------------------
def new_manufacturer():
    id = lineboterp.user_id
    state = lineboterp.user_state
    message = lineboterp.msg
    message_storage = lineboterp.storage
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

#-------------------廠商管理-修改廠商資料----------------------
def manufacturer_editinfo():
    id = lineboterp.user_id
    state = lineboterp.user_state
    message = lineboterp.msg
    message_storage = lineboterp.storage
    #editfield=廠商名, 負責或對接人, 市話, 電話, 付款方式, 行庫名, 行庫代號, 匯款帳號
    show = [Manufacturer_edit()]#退回修改清單頁
    if message == '取消':
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
        check_text = Manufacturer_edit()
    elif state[id] == 'manufacturer_edit_name':
        if message_storage[id+'manufacturer_list_name'] == message:#判斷有沒有修改
            state[id] = 'normal'
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
                state[id] = 'normal'
            else:
                check_text = Manufacturer_edit_screen(1,textmsg,message_storage[id+'manufacturer_list_name'])#edittype,errormsg,before..名稱
    elif state[id] == 'manufacturer_edit_principal':
        if message_storage[id+'manufacturer_list_principal'] == message:#判斷有沒有修改
            state[id] = 'normal'
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
                state[id] = 'normal'
            else:
                check_text = Manufacturer_edit_screen(2,textmsg,message_storage[id+'manufacturer_list_principal'])#edittype,errormsg,before..負責人
    elif state[id] == 'manufacturer_edit_localcalls':
        if message_storage[id+'manufacturer_list_localcalls'] == message:#判斷有沒有修改
            state[id] = 'normal'
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
                state[id] = 'normal'
            else:
                check_text = Manufacturer_edit_screen(3,textmsg,message_storage[id+'manufacturer_list_localcalls'])#edittype,errormsg,before..市話
    elif state[id] == 'manufacturer_edit_phonenum':
        if message_storage[id+'manufacturer_list_phone'] == message:#判斷有沒有修改
            state[id] = 'normal'
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
                state[id] = 'normal'
            else:
                check_text = Manufacturer_edit_screen(4,textmsg,message_storage[id+'manufacturer_list_phone'])#edittype,errormsg,before..電話
    elif state[id] == 'manufacturer_edit_payment':
        if message_storage[id+'manufacturer_list_payment'] == message:#判斷有沒有修改
            state[id] = 'normal'
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
                        state[id] = 'normal'
                        check_text = Manufacturer_edit()
                else:
                    show.append(TextSendMessage(text='付款方式修改失敗！請稍後在試。'))
                    check_text = Manufacturer_edit()#退回修改清單頁
                    state[id] = 'normal'
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
                    state[id] = 'normal'
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
                state[id] = 'normal'
        else:
            before = [str(message_storage[id+'manufacturer_list_bankid']),message_storage[id+'manufacturer_list_bankname']]
            check_text = Manufacturer_edit_screen(6,textmsg,before)#edittype,errormsg,before..行庫/代號
    elif state[id] == 'manufacturer_edit_bankaccount':
        if message_storage[id+'manufacturer_list_bankaccount'] == message:#判斷有沒有修改
            state[id] = 'normal'
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
                state[id] = 'normal'
            else:
                check_text = Manufacturer_edit_screen(7,textmsg,message_storage[id+'manufacturer_list_bankaccount'])#edittype,errormsg,before..行庫帳號
    else:
        state[id] = 'normal'
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
    id = lineboterp.user_id
    message = lineboterp.msg
    message_storage = lineboterp.storage
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
    id = lineboterp.user_id
    message = lineboterp.msg
    message_storage = lineboterp.storage
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
    id = lineboterp.user_id
    message = lineboterp.msg
    message_storage = lineboterp.storage
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
                            check_text = f"「{info['code']}」區碼正確，電話號碼開頭錯誤！"
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
    id = lineboterp.user_id
    message = lineboterp.msg
    message_storage = lineboterp.storage
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
    id = lineboterp.user_id
    message = lineboterp.msg
    message_storage = lineboterp.storage
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
    id = lineboterp.user_id
    message = lineboterp.msg
    message_storage = lineboterp.storage
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
    id = lineboterp.user_id
    message = lineboterp.msg
    message_storage = lineboterp.storage
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
#---------------------///--------------------

#-------------------訂單檢查----------------------
def orderandpreorder_check():
     # 若使用者已經在等待回覆狀態，則根據回覆進行處理
    id = lineboterp.user_id
    state = lineboterp.user_state
    message = lineboterp.msg
    product_id = lineboterp.product[id+'product_id']
    product = lineboterp.product[id+'product']
    product_order_preorder = lineboterp.product_order_preorder
    message_storage = lineboterp.storage
    orderall = lineboterp.orderall
    storage_multiple = lineboterp.storage[id+'multiple']
    phone = recent_phone_call(id)#最近一筆電話取得
    if message.isdigit():
            # 處理完問題後，結束等待回覆狀態
        if state[id] == 'ordering':
            stocknum = stockonly(product_id)
            if stocknum > 0 and int(message) > 0 and int(message) <= stocknum:
                message_storage[id+'num'] = message
                message_storage[id+'ordertype'] = '現購'
                errormsg = 'no'
                check_text = Order_phonenum_screen(product_order_preorder[id],product_id,product,errormsg,phone,message_storage[id+'num'])
                state[id] = 'phonenum' #從user_state轉換輸入電話狀態
            else:
                errormsg = f"您輸入的數量「{message}」有誤！請重新輸入現購數量。\n目前庫存{stocknum}"
                check_text = Order_buynow(errormsg)
        elif state[id] == 'preorder':
            if int(message) > 0:
                if int(message) % storage_multiple == 0:
                    message_storage[id+'num'] = message
                    message_storage[id+'ordertype'] = '預購'
                    errormsg = 'no'
                    check_text = Order_phonenum_screen(product_order_preorder[id],product_id,product,errormsg,phone,message_storage[id+'num'])
                    state[id] = 'phonenum' #從user_state轉換輸入電話狀態
                else:
                    errormsg = f"您輸入的預購倍數「{message}」不是{str(storage_multiple)}的倍數喔！請重新輸入預購數量。"
                    check_text = Order_preorder(errormsg)
            else:
                errormsg = f"您輸入的數量「{message}」有誤！請重新輸入預購數量。"
                check_text = Order_preorder(errormsg)
        elif state[id] == 'phonenum':
            if message.isdigit():
                if(len(message) < 10):
                    errormsg = f"輸入電話格式錯誤！(10碼)\n請重新打字輸入正確的電話號碼。"
                    check_text = Order_phonenum_screen(product_order_preorder[id],product_id,product,errormsg,phone,message_storage[id+'num'])
                elif (len(message) > 10):
                    errormsg = f"輸入電話格式錯誤！(10碼)\n請重新打字輸入正確的電話號碼。"
                    check_text = Order_phonenum_screen(product_order_preorder[id],product_id,product,errormsg,phone,message_storage[id+'num'])
                elif(message[:2] != '09'):           
                    errormsg = f"輸入電話格式錯誤！(09開頭)\n請重新打字輸入正確的電話號碼。"
                    check_text = Order_phonenum_screen(product_order_preorder[id],product_id,product,errormsg,phone,message_storage[id+'num'])
                else:
                    message_storage[id+'phonenum'] = message
                    state[id] = 'end'#從user_state轉換確認狀態
                    localsubtotal,dbunitin,price,discount = quickcalculation(product_id,int(message_storage[id+'num']))#快速計算小計
                    if str(localsubtotal).isdigit():
                        subtotal = str('{:,}'.format(localsubtotal))
                        message_storage[id+'subtotalin'] = subtotal
                        message_storage[id+'unitin'] = dbunitin
                        message_storage[id+'oderprice'] = price
                        message_storage[id+'oderdiscount'] = discount
                        check_text = Single_order_confirmation_screen(product_order_preorder[id],product_id,product,message_storage[id+'phonenum'],
                                                          message_storage[id+'num'],message_storage[id+'unitin'],
                                                          message_storage[id+'oderprice'],message_storage[id+'oderdiscount'],
                                                          message_storage[id+'subtotalin'])
                    else:
                        check_text = TextSendMessage(text="訂單確認頁面生成失敗，請輸入'取消'。")
                       
        elif state[id] =='end':
            if message == '1':
                numtype = message_storage[id+'ordertype']
                orderall[id] = [product_id,message_storage[id+'num']]#商品紀錄以便存入資料庫
                orderinfo, establishment_message = order_create()#資料庫訂單建立
                if establishment_message == 'ok':
                    orderinfo = orderinfo[0]
                    if numtype == '現購':
                        pagemin = lineboterp.list_page[lineboterp.user_id+'現購min']
                        pagemax = lineboterp.list_page[lineboterp.user_id+'現購max']
                        continue_browsing = "【現購列表下一頁】"+ str(pagemin+1) +"～"+ str(pagemax)
                        check_text = Order_establishment_message(orderinfo[2],str(orderinfo[0]),orderinfo[1],orderinfo[6],
                                                                 str(orderinfo[3]),str(orderinfo[5]),str('{:,}'.format(orderinfo[4])),
                                                                 continue_browsing,message_storage[id+'oderprice'],
                                                                 message_storage[id+'oderdiscount'],message_storage[id+'phonenum'])
                    elif numtype == '預購':
                        pagemin = lineboterp.list_page[lineboterp.user_id+'預購min']
                        pagemax = lineboterp.list_page[lineboterp.user_id+'預購max']
                        continue_browsing = "【預購列表下一頁】"+ str(pagemin+1) +"～"+ str(pagemax)
                        check_text = Order_establishment_message(orderinfo[2],str(orderinfo[0]),orderinfo[1],orderinfo[6],
                                                                 str(orderinfo[3]),str(orderinfo[5]),str('{:,}'.format(orderinfo[4])),
                                                                 continue_browsing,message_storage[id+'oderprice'],
                                                                 message_storage[id+'oderdiscount'],message_storage[id+'phonenum'])
                    state[id] = 'normal' #從user_state轉換普通狀態
                    #下方重置
                    message_storage[id+'num'] = 'NaN'
                    message_storage[id+'phonenum'] = 'NaN'
                    product_id = 'NaN'
                    product = 'NaN'
                    product_order_preorder[id] = 'NaN'
                    message_storage[id+'ordertype'] = 'NaN'
                    message_storage[id+'oderprice'] = 'NaN'
                    message_storage[id+'oderdiscount'] = 'NaN'
                else:
                    check_text = TextSendMessage(text=establishment_message)
                    state[id] = 'normal' #從user_state轉換普通狀態
                    #下方重置
                    message_storage[id+'num'] = 'NaN'
                    message_storage[id+'phonenum'] = 'NaN'
                    product_id = 'NaN'
                    product = 'NaN'
                    product_order_preorder[id] = 'NaN'
                    message_storage[id+'ordertype'] = 'NaN'
                    message_storage[id+'oderprice'] = 'NaN'
                    message_storage[id+'oderdiscount'] = 'NaN'
            elif message == '2':
                check_text = '您的商品訂/預購流程\n已經取消囉～'
                check_text = TextSendMessage(text=check_text),Cancel_fail_message(message_storage[id+'ordertype'])
                state[id] = 'normal' #從user_state轉換普通狀態
                #下方重置
                message_storage[id+'num'] = 'NaN'
                message_storage[id+'phonenum'] = 'NaN'
                product_id = 'NaN'
                product = 'NaN'
                product_order_preorder[id] = 'NaN'
                message_storage[id+'ordertype'] = 'NaN'
                message_storage[id+'oderprice'] = 'NaN'
                message_storage[id+'oderdiscount'] = 'NaN'
            else:
                check_text = Single_order_confirmation_screen(product_order_preorder[id],product_id,product,message_storage[id+'phonenum'],
                                                          message_storage[id+'num'],message_storage[id+'unitin'],
                                                          message_storage[id+'oderprice'],message_storage[id+'oderdiscount'],
                                                          message_storage[id+'subtotalin'])
    else:
        if(message == "取消"):
            check_text = '您的商品現/預購流程\n已經取消囉～'
            if state[id] == 'ordering':
                message_storage[id+'ordertype'] = '現購'
            if state[id] == 'preorder':
                message_storage[id+'ordertype'] = '預購'
            check_text = TextSendMessage(text=check_text),Cancel_fail_message(message_storage[id+'ordertype'])
            state[id] = 'normal' #從user_state轉換普通狀態
            #下方重置
            message_storage[id+'num'] = 'NaN'
            message_storage[id+'phonenum'] = 'NaN'
            product_id = 'NaN'
            product = 'NaN'
            product_order_preorder[id] = 'NaN'
            message_storage[id+'ordertype'] = 'NaN'
            message_storage[id+'oderprice'] = 'NaN'
            message_storage[id+'oderdiscount'] = 'NaN'
        elif state[id] in ['ordering','preorder']:
            if state[id] == 'ordering':
                errormsg = f"您輸入的「{message}」不是此現購流程中會出現的內容喔！請重新輸入現購數量。"
                check_text = Order_buynow(errormsg)
            elif state[id] == 'preorder':
                errormsg = f"您輸入的「{message}」不是此預購流程中會出現的內容喔！請重新輸入預購數量。"
                check_text = Order_preorder(errormsg)
        elif state[id] =='phonenum':
            if message == '重新填寫':
                message_storage[id+'num'] = 'NaN'
                message_storage[id+'phonenum'] = 'NaN'
                errormsg = 'no'
                if product_order_preorder[id] == '現購':
                    check_text = Order_buynow(errormsg)
                elif product_order_preorder[id] == '預購':
                    check_text = Order_preorder(errormsg)
            else:
                errormsg = f"您輸入的「{message}」不是此{product_order_preorder[id]}流程中會出現的內容喔！請重新輸入聯絡電話。"
                check_text = Order_phonenum_screen(product_order_preorder[id],product_id,product,errormsg,phone,message_storage[id+'num'])
        elif state[id] =='end':
            check_text = Single_order_confirmation_screen(product_order_preorder[id],product_id,product,message_storage[id+'phonenum'],
                                                          message_storage[id+'num'],message_storage[id+'unitin'],
                                                          message_storage[id+'oderprice'],message_storage[id+'oderdiscount'],
                                                          message_storage[id+'subtotalin'])
        else:
            check_text = '您還在訂/預購中喔！\n輸入的 "' + message + '" 不是此流程的填寫！\n請重新輸入，謝謝～'
            check_text = TextSendMessage(text=check_text),TextSendMessage(text='訂/預購流程中，如想取消請打字輸入" 取消 "')    
    return check_text

#購物車商品新增
def cartnum():
    id = lineboterp.user_id
    state = lineboterp.user_state
    message = lineboterp.msg
    product_id = lineboterp.product[id+'cartproduct_id']
    product = lineboterp.product[id+'cartproduct']

    pagemin = lineboterp.list_page[lineboterp.user_id+'現購min']
    pagemax = lineboterp.list_page[lineboterp.user_id+'現購max']
    continue_browsing = "【現購列表下一頁】"+ str(pagemin+1) +"～"+ str(pagemax)
    
    if message.isdigit():#是數字
        text = cartadd(id,product_id,int(message))
        if text == 'ok':
            unit = unitsearch(product_id)
            check_text = Cart_join_success_message(product,product_id,message,unit,continue_browsing)
            state[id] = 'normal' #結束流程將user_state轉換預設狀態
        else:
            check_text = TextSendMessage(text='購物車加入失敗！請稍後再試。')
            state[id] = 'normal' #結束流程將user_state轉換預設狀態
    else:
        if(message == "取消"):
            check_text = '您的商品加入購物車流程\n已經取消囉～'
            check_text = TextSendMessage(text=check_text),Cancel_fail_message('現購')
            state[id] = 'normal' #結束流程將user_state轉換預設狀態
        else:
            errormsg = f"您輸入的「{message}」內容並非數字喔！請重新輸入數量。"
            check_text = addcart(errormsg)
    return check_text

#購物車數量修改
def cartrpnum():
    id = lineboterp.user_id
    state = lineboterp.user_state
    message = lineboterp.msg
    product_id = lineboterp.product[id+'cartreviseproduct_id']
    product = lineboterp.product[id+'cartreviseproduct_name']
    if message.isdigit():#是數字
        stocknum = stockonly(product_id)
        if stocknum > 0 and int(message) > 0 and int(message) <= stocknum:
            text = revise(id,product_id,int(message))
            if text == 'ok':
                check_text = cart_list()
                state[id] = 'normal' #結束流程將user_state轉換預設狀態
            else:
                check_text = TextSendMessage(text='購物車商品數量修改失敗！請稍後再試。')
                state[id] = 'normal' #結束流程將user_state轉換預設狀態
        else:
            errormsg = f"您輸入的「{message}」大於現在的庫存數量，請重新輸入。\n目前庫存{stocknum}"
            check_text = cartrevise(errormsg)
    else:
        if(message == "取消"):
            check_text = TextSendMessage(text='您的購物車商品數量修改流程\n已經取消囉～')
            check_text = check_text,cart_list()
            state[id] = 'normal' #結束流程將user_state轉換預設狀態
        else:
            errormsg = f"您輸入的「{message}」不在修改購物車數量中的內容喔！"
            check_text = cartrevise(errormsg)
    return check_text

#購物車訂單
def cartorder():
    id = lineboterp.user_id
    state = lineboterp.user_state
    message = lineboterp.msg
    message_storage = lineboterp.storage
    check_text = ''
    phone = recent_phone_call(id)#最近一筆電話取得
    if message.isdigit():
        if state[id] == 'cartorderphonenum':
            if message.isdigit():
                if(len(message) < 10):
                    errormsg = '輸入電話格式錯誤！(10碼)\n請重新打字輸入正確的電話號碼'
                    check_text = Cart_order_screen(phone,errormsg)
                elif (len(message) > 10):
                    errormsg = '輸入電話格式錯誤！(10碼)\n請重新打字輸入正確的電話號碼'
                    check_text = Cart_order_screen(phone,errormsg)
                elif(message[:2] != '09'): 
                    errormsg = '輸入電話格式錯誤！(09碼)\n請重新打字輸入正確的電話號碼'
                    check_text = Cart_order_screen(phone,errormsg)          
                else:
                    state[id] = 'cartorderrun'#從user_state轉換確認狀態
                    db_cartshow = cartsearch()
                    showp = f"電話號碼：{message}\n\n"
                    tnum = 0#總額
                    #訂單編號, 商品ID, 商品名稱, 訂購數量, 商品單位, 商品小計
                    cartodinfo_id = []
                    cartodinfo_name = []
                    cartodinfo_num = []
                    cartodinfo_unit = []
                    cartodinfo_subtotal = []
                    for totallist in db_cartshow:
                        cartodinfo_id.append(totallist[1])
                        cartodinfo_name.append(totallist[2])
                        cartodinfo_num.append(totallist[3])
                        cartodinfo_unit.append(totallist[4])
                        cartodinfo_subtotal.append(totallist[5])
                        tnum += totallist[5]
                    message_storage[id+'cartodinfo_id'] = cartodinfo_id #商品ID
                    message_storage[id+'cartodinfo_name'] = cartodinfo_name #商品名稱
                    message_storage[id+'cartodinfo_num'] = cartodinfo_num #商品數量
                    message_storage[id+'cartodinfo_unit'] = cartodinfo_unit #商品單位
                    message_storage[id+'cartodinfo_subtotal'] = cartodinfo_subtotal #商品小計
                    message_storage[id+'shownum'] = tnum #總額
                    message_storage[id+'phonenum'] = message
                    check_text = Cartordercheck_establishment_message()#購物車確認畫面
        elif state[id] == 'cartorderrun':
            if message == '1':
                orderinfo, establishment_message = cartordergo(message_storage[id+'phonenum'])#執行購物車訂單建立
                '''訂單編號, 商品名稱, 現預購商品, 訂購數量, 商品小計, 商品單位, 商品ID , 電話, 總額'''
                if establishment_message == 'ok':
                    check_text = Cartorder_establishment_message(orderinfo)
                else:
                    check_text = cart_list(),TextSendMessage(text='購物車訂單成立異常，請稍後再試！')
            elif message == '2':
                check_text = '您的購物車訂單流程\n已經取消囉～'
                check_text = TextSendMessage(text=check_text),cart_list()
            else:
                check_text = Cartordercheck_establishment_message()#購物車確認畫面
            message_storage[id+'cartodinfo_id'] = 'NaN' #商品ID
            message_storage[id+'cartodinfo_name'] = 'NaN' #商品名稱
            message_storage[id+'cartodinfo_num'] = 'NaN' #商品數量
            message_storage[id+'cartodinfo_unit'] = 'NaN' #商品單位
            message_storage[id+'cartodinfo_subtotal'] = 'NaN' #商品小計
            message_storage[id+'shownum'] = 'NaN' #總額
            message_storage[id+'phonenum'] = 'NaN'#電話
            state[id] = 'normal' #從user_state轉換普通狀態
    else:
        if(message == "取消"):
            check_text = '您的購物車訂單流程\n已經取消囉～'
            message_storage[id+'showp'] = 'NaN' #訂單資訊(之後刪)####
            message_storage[id+'cartodinfo_id'] = 'NaN' #商品ID
            message_storage[id+'cartodinfo_name'] = 'NaN' #商品名稱
            message_storage[id+'cartodinfo_num'] = 'NaN' #商品數量
            message_storage[id+'cartodinfo_unit'] = 'NaN' #商品單位
            message_storage[id+'cartodinfo_subtotal'] = 'NaN' #商品小計
            message_storage[id+'shownum'] = 'NaN' #總額
            message_storage[id+'phonenum'] = 'NaN'
            errormsg = 'no'
            check_text = TextSendMessage(text=check_text)
            check_text = check_text,cart_list()
            state[id] = 'normal' #結束流程將user_state轉換預設狀態
        elif state[id] == 'cartorderphonenum':
            errormsg = '您還在購物車訂單流程，請重新輸入行動電話'
            check_text = Cart_order_screen(phone,errormsg)
        elif state[id] == 'cartorderrun':
            check_text = Cartordercheck_establishment_message()#購物車確認畫面
    return check_text
#-------------------商家地址----------------------
def Company_location():
    location = LocationSendMessage(
    title='高逸嚴選百貨團購',
    address='235新北市中和區員山路325-4號',
    latitude='25.000965554762445',#緯度
    longitude='121.48115945271607'#經度
    )
    return location

#-------------------商家資訊----------------------
def business_information():
    '''business_detail= TextSendMessage(text='歡迎來到「高逸嚴選百貨團購」\n'\
    '\n我們的營業時間：\n一至五9:00-20:00\n(六日會發公告是否有營業)\n'\
    '\n簡介：\n高逸團購注重天然、高品質、高CP值商品，讓您們安心選購～若有任何許願商品也歡迎告知！感謝支持與陪伴，很開心能為您們服務！\n'\
    '\n地址：\n新北市中和區員山路325之4號2樓'
    ),Company_location()'''
    business_info = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "image",
                            "url": "https://i.imgur.com/hQ0qG9c.jpg",
                            "size": "5xl",
                            "aspectMode": "cover",
                            "aspectRatio": "150:196",
                            "gravity": "center",
                            "flex": 1
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "image",
                                "url": "https://i.imgur.com/XsyIMd0.jpg",
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "150:98",
                                "gravity": "center"
                            },
                            {
                                "type": "image",
                                "url": "https://i.imgur.com/4Nh5x9j.jpg",
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "150:98",
                                "gravity": "center"
                            }
                            ],
                            "flex": 1
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "image",
                                "url": "https://i.imgur.com/rGlTAt3.jpg",
                                "aspectMode": "cover",
                                "size": "full"
                            }
                            ],
                            "cornerRadius": "100px",
                            "width": "80px",
                            "height": "80px"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "contents": [
                                {
                                    "type": "span",
                                    "text": "高逸嚴選百貨團購",
                                    "weight": "bold",
                                    "color": "#000000",
                                    "size": "lg"
                                }
                                ],
                                "size": "sm",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": "營業時間：\n週一至五9:00-20:00\n(六、日會發公告) ",
                                "wrap": True
                            }
                            ]
                        }
                        ],
                        "spacing": "xl",
                        "paddingAll": "20px"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "separator"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "簡介",
                                    "wrap": True,
                                    "size": "xl",
                                    "offsetTop": "xxl",
                                    "weight": "bold"
                                }
                                ],
                                "cornerRadius": "100px",
                                "width": "30px",
                                "height": "100px"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "高逸團購注重天然、高品質、高CP值商品，讓您們安心選購～若有任何許願商品也歡迎告知！感謝支持與陪伴，很開心能為您們服務！",
                                    "wrap": True
                                }
                                ]
                            }
                            ],
                            "spacing": "xl",
                            "paddingAll": "20px"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "uri",
                            "label": "FB粉絲專頁",
                            "uri": "https://www.facebook.com/profile.php?id=100063943548653&mibextid=LQQJ4d"
                            },
                            "style": "primary",
                            "color": "#a8c1c9",
                            "margin": "sm"
                        },
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "地址",
                                    "wrap": True,
                                    "size": "xl",
                                    "weight": "bold"
                                }
                                ],
                                "cornerRadius": "100px",
                                "width": "25px",
                                "height": "72px"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "新北市中和區員山路325之4號2樓(全家-中和員山店旁)",
                                    "wrap": True,
                                    "offsetTop": "lg"
                                }
                                ]
                            }
                            ],
                            "spacing": "xl",
                            "paddingAll": "20px"
                        }
                        ]
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "uri",
                        "label": "地圖導航",
                        "uri": "https://goo.gl/maps/N1Rq3nX3XEpdtxLm9"
                        },
                        "style": "primary",
                        "color": "#C9B0A8"
                    }
                    ],
                    "paddingAll": "0px"
                }
                }

    business_detail =FlexSendMessage(
                            alt_text='營業資訊',
                            contents={
                                "type": "carousel",
                                "contents": [business_info]   
                                } 
                            )
    return business_detail

