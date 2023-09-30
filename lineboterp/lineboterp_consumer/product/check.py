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
from relevant_information import bank

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
        check_text = TextSendMessage(text='===建立廠商===\n=>1.請打字輸入廠商名稱：\n(20字內)')
    elif message == '取消':
        state[id] = 'normal'
        message_storage[id+'manufacturer_name'] = 'NAN'
        message_storage[id+'manufacturer_principal'] = 'NAN'
        message_storage[id+'manufacturer_localcalls'] = 'NAN'
        message_storage[id+'manufacturer_phonenum'] = 'NAN'
        message_storage[id+'manufacturer_Payment'] = 'NAN'
        message_storage[id+'manufacturer_bankid'] = 'NAN'
        message_storage[id+'manufacturer_bankname'] = 'NAN'
        message_storage[id+'manufacturer_bankaccount'] = 'NAN'
        message_storage[id+'manufacturer_all'] = 'NAN'
        check_text = TextSendMessage(text="取消新增廠商流程囉！")
    elif state[id] == 'manufacturer_name':
        if len(message) <= 20:
            message_storage[id+'manufacturer_name'] = message #廠商名暫存
            message_storage[id+'manufacturer_all'] = f"===建立廠商===\n1.廠商名稱：{message_storage[id+'manufacturer_name']}"
            state[id] = 'manufacturer_principal' #狀態負責人
            check_text = TextSendMessage(text=f"{message_storage[id+'manufacturer_all']}\n=>2.請打字輸入負責人或對接人名稱：\n(10字內)")
        else:
            check_text = TextSendMessage(text=f"===建立廠商===\n=>1.請打字輸入廠商名稱：\n(20字內)\n錯誤訊息：輸入的「{message}」名稱大於20字喔！")
    elif state[id] == 'manufacturer_principal':
        if len(message) <= 10:
            message_storage[id+'manufacturer_principal'] = message #負責人暫存
            message_storage[id+'manufacturer_all'] += f"\n2.負責人或對接人名稱：{message_storage[id+'manufacturer_principal']}"
            state[id] = 'manufacturer_localcalls' #狀態市話
            check_text = TextSendMessage(text=f"{message_storage[id+'manufacturer_all']}\n=>3.請打字輸入公司市話(0+2~3碼)+7碼：\nex.039981234、0379981234、08269981234、略過")
        else:
            check_text = TextSendMessage(text=f"===建立廠商===\n=>2.請打字輸入負責人或對接人名稱：\n(10字內)\n錯誤訊息：輸入的「{message}」名稱大於10字喔！")
    elif state[id] == 'manufacturer_localcalls':
        areacode = ['02','03','037','04','049','05','06','07','08','089','082','0826','0836']#所有區碼
        if message.isdigit():
            check_areacode = 'no'
            if len(message) in [9,10,11]:
                if len(message) == 9:
                    cut_areacode = message[:2]
                    if cut_areacode in areacode:
                        check_areacode = 'ok'
                elif len(message) == 10:
                    cut_areacode = message[:3]
                    if cut_areacode in areacode:
                        check_areacode = 'ok'
                elif len(message) == 11:
                    cut_areacode = message[:4]
                    if cut_areacode in areacode:
                        check_areacode = 'ok'
                
                if check_areacode == 'ok':
                    message_storage[id+'manufacturer_localcalls'] = message #市話暫存
                    message_storage[id+'manufacturer_all'] += f"\n3.公司市話：{message_storage[id+'manufacturer_localcalls']}"
                    state[id] = 'manufacturer_phonenum' #狀態電話
                    check_text = TextSendMessage(text=f"{message_storage[id+'manufacturer_all']}\n=>4.請打字輸入行動電話：\nex.0952025413、略過")
                else:
                    check_text = TextSendMessage(text=f"===建立廠商===\n=>3.請打字輸入公司市話(0+2~3碼)+7碼：\nex.039981234、0379981234、08269981234、略過'\n錯誤訊息：輸入的「{message}」區碼錯誤喔！")
            else:
                check_text = TextSendMessage(text=f"===建立廠商===\n=>3.請打字輸入公司市話(0+2~3碼)+7碼：\nex.039981234、0379981234、08269981234、略過'\n錯誤訊息：輸入的「{message}」不是市話的規則喔！")
        else:
            if message == '略過':
                state[id] = 'manufacturer_phonenum' #狀態電話
                message_storage[id+'manufacturer_localcalls'] = message #市話暫存
                message_storage[id+'manufacturer_all'] += f"\n3.公司市話：{message_storage[id+'manufacturer_localcalls']}"
                check_text = TextSendMessage(text=f"{message_storage[id+'manufacturer_all']}\n=>4.請打字輸入行動電話：\nex.0952025413、略過")
            else:
                check_text = TextSendMessage(text=f"===建立廠商===\n=>3.請打字輸入公司市話(0+2~3碼)+7碼：\nex.039981234、0379981234、08269981234'\n錯誤訊息：輸入的「{message}」不是市話的規則喔！")
    elif state[id] == 'manufacturer_phonenum':
        if message.isdigit():
                if(len(message) < 10):
                    check_text =  TextSendMessage(text=f"輸入電話格式錯誤！(10碼)\n請重新打字輸入正確的電話號碼。")
                elif (len(message) > 10):
                    check_text =  TextSendMessage(text=f"輸入電話格式錯誤！(10碼)\n請重新打字輸入正確的電話號碼。")
                elif(message[:2] != '09'):           
                    check_text =  TextSendMessage(text=f"輸入電話格式錯誤！(09開頭)\n請重新打字輸入正確的電話號碼。")
                else:
                    message_storage[id+'manufacturer_phonenum'] = message #行動電話暫存
                    state[id] = 'manufacturer_Payment' #狀態付款方式
                    message_storage[id+'manufacturer_all'] += f"\n4.行動電話：{message_storage[id+'manufacturer_phonenum']}"
                    check_text = TextSendMessage(text=f"{message_storage[id+'manufacturer_all']}\n=>5.請打字輸入付款方式：\nex.現金、匯款")
        else:
            if message == '略過':
                state[id] = 'manufacturer_Payment' #狀態付款方式
                message_storage[id+'manufacturer_phonenum'] = message #行動電話暫存
                message_storage[id+'manufacturer_all'] += f"\n4.行動電話：{message_storage[id+'manufacturer_phonenum']}"
                check_text = TextSendMessage(text=f"{message_storage[id+'manufacturer_all']}\n=>5.請打字輸入付款方式：\nex.現金、匯款")
            else:
                check_text = TextSendMessage(text=f"===建立廠商===\n=>4.請打字輸入行動電話：\nex.0952025413、略過\n錯誤訊息：輸入的「{message}」不是行動電話的規則喔！")
    elif state[id] == 'manufacturer_Payment':
        if message in ['現金','匯款']:
            message_storage[id+'manufacturer_Payment'] = message #付款方式暫存
            message_storage[id+'manufacturer_all'] += f"\n5.付款方式：{message_storage[id+'manufacturer_Payment']}"
            if message == '匯款':
                state[id] = 'manufacturer_bank' #狀態行庫
                check_text = TextSendMessage(text=f"{message_storage[id+'manufacturer_all']}\n=>6.請打字輸入行庫代號(數字3碼)或行庫名稱(30字內)，則一即可：")
            else:
                state[id] = 'manufacturer_end' #狀態確認
                message_storage[id+'manufacturer_bankid'] = "略過"
                message_storage[id+'manufacturer_bankname'] = "略過"
                message_storage[id+'manufacturer_bankaccount'] = "略過"
                check_text = TemplateSendMessage(
                                alt_text='廠商新增資料確認',
                                template=ButtonsTemplate(
                                    text= message_storage[id+'manufacturer_all'],
                                    actions=[
                                        MessageAction(
                                            label='【新增廠商】',
                                            text='1',
                                        ),
                                        MessageAction(
                                            label='【取消】',
                                            text='2',
                                        )
                                    ]
                                )
                            )
            
            
        else:
            check_text = TextSendMessage(text=f"===建立廠商===\n=>5.請打字輸入付款方式：\nex.現金、匯款\n錯誤訊息：輸入的「{message}」不是現金或匯款喔！")
    
    elif state[id] == 'manufacturer_bank':
        bankdata = bank()
        checkbank = 'no'
        if message.isdigit():
            if len(message) <= 3:
                for bankcheck in bankdata:
                    if message == bankcheck['code']:
                        message_storage[id+'manufacturer_bankid'] = message #行庫代號暫存
                        message_storage[id+'manufacturer_all'] += f"\n6.行庫代號：{message_storage[id+'manufacturer_bankid']}"
                        message_storage[id+'manufacturer_bankname'] = bankcheck['name'] #行庫名稱暫存
                        message_storage[id+'manufacturer_all'] += f"\n7.行庫名稱：{message_storage[id+'manufacturer_bankname']}"
                        checkbank = 'yes'
                        break
                if checkbank == 'yes':
                    state[id] = 'manufacturer_bankaccount' #狀態行庫帳號
                    check_text = TextSendMessage(text=f"{message_storage[id+'manufacturer_all']}\n=>8.請打字輸入行庫帳號：\n(數字14碼內)")
                else:
                    check_text = TextSendMessage(text=f"===建立廠商===\n=>6.請打字輸入行庫代號(數字3碼)或行庫名稱(30字內)，則一即可：\n錯誤訊息：輸入的代號「{message}」查無銀行！")      
            else:
                check_text = TextSendMessage(text=f"===建立廠商===\n=>6.請打字輸入行庫代號(數字3碼)或行庫名稱(30字內)，則一即可：\n錯誤訊息：輸入的「{message}」不是銀行代號數字3碼！")
        else:       
            if len(message) <= 30:
                for bankcheck in bankdata:
                    if message in bankcheck['name']:
                        message_storage[id+'manufacturer_bankid'] = bankcheck['code'] #行庫代號暫存
                        message_storage[id+'manufacturer_all'] += f"\n6.行庫代號：{message_storage[id+'manufacturer_bankid']}"
                        message_storage[id+'manufacturer_bankname'] = bankcheck['name'] #行庫名稱暫存
                        message_storage[id+'manufacturer_all'] += f"\n7.行庫名稱：{message_storage[id+'manufacturer_bankname']}"
                        checkbank = 'yes'
                        break
                if checkbank == 'yes':
                    state[id] = 'manufacturer_bankaccount' #狀態行庫帳號
                    check_text = TextSendMessage(text=f"{message_storage[id+'manufacturer_all']}\n=>8.請打字輸入行庫帳號：\n(數字14碼內)")
                else:
                    check_text = TextSendMessage(text=f"===建立廠商===\n=>6.請打字輸入行庫代號(數字3碼)或行庫名稱(30字內)，則一即可：\n錯誤訊息：輸入的行庫名「{message}」查無銀行！")      
            else:
                check_text = TextSendMessage(text=f"===建立廠商===\n=>6.請打字輸入行庫代號(數字3碼)或行庫名稱(30字內)，則一即可：\n錯誤訊息：輸入的「{message}」銀行行庫名大於30字！")

    elif state[id] == 'manufacturer_bankaccount':
        if message.isdigit():
            if len(message) <= 14:
                if len(message) < 14:
                    while len(message) < 14:
                        message = '0'+ message
                message_storage[id+'manufacturer_bankaccount'] = message #行庫帳號暫存
                state[id] = 'manufacturer_end' #狀態新增確認
                message_storage[id+'manufacturer_all'] += f"\n8.行庫帳號：{message_storage[id+'manufacturer_bankaccount']}"
                check_text = TemplateSendMessage(
                                alt_text='廠商新增資料確認',
                                template=ButtonsTemplate(
                                    text= message_storage[id+'manufacturer_all'],
                                    actions=[
                                        MessageAction(
                                            label='【新增廠商】',
                                            text='1',
                                        ),
                                        MessageAction(
                                            label='【取消】',
                                            text='2',
                                        )
                                    ]
                                )
                            )
            else:
                check_text = TextSendMessage(text=f"===建立廠商===\n=>6.請打字輸入行庫名稱：\n(數字3碼)\n錯誤訊息：輸入的「{message}」不是數字3碼！")
        else:
            check_text = TextSendMessage(text=f"===建立廠商===\n=>6.請打字輸入行庫名稱：\n(數字3碼)\n錯誤訊息：輸入的「{message}」不是數字3碼！")
    elif state[id] == 'manufacturer_end':
        if message.isdigit():
            if message in ['1','2']:
                if message == '1':
                    check,info = manufacturer(message_storage[id+'manufacturer_name'],message_storage[id+'manufacturer_principal'],
                                              message_storage[id+'manufacturer_localcalls'],message_storage[id+'manufacturer_phonenum'],
                                              message_storage[id+'manufacturer_Payment'],message_storage[id+'manufacturer_bankid'],
                                              message_storage[id+'manufacturer_bankname'],message_storage[id+'manufacturer_bankaccount'])
                    if check == 'ok':
                        check_text = TextSendMessage(text=f"{info}廠商建立成功！")
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
                message_storage[id+'manufacturer_all'] = 'NAN'
            else:
                check_text = TemplateSendMessage(
                                alt_text='廠商新增資料確認',
                                template=ButtonsTemplate(
                                    text= message_storage[id+'manufacturer_all'],
                                    actions=[
                                        MessageAction(
                                            label='【新增廠商】',
                                            text='1',
                                        ),
                                        MessageAction(
                                            label='【取消】',
                                            text='2',
                                        )
                                    ]
                                )
                            )
        else:
            check_text = TemplateSendMessage(
                                alt_text='廠商新增資料確認',
                                template=ButtonsTemplate(
                                    text= message_storage[id+'manufacturer_all'],
                                    actions=[
                                        MessageAction(
                                            label='【新增廠商】',
                                            text='1',
                                        ),
                                        MessageAction(
                                            label='【取消】',
                                            text='2',
                                        )
                                    ]
                                )
                            )
    return check_text

#-----------------------------------------

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

