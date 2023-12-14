from linebot.models import TextSendMessage,FlexSendMessage,LocationSendMessage
from product.buy_now import Order_buynow
from product.product_preorder import Order_preorder
import info
from ask_wishes.ask import ask
from ask_wishes.wishes import wishes
from database import recent_phone_call, quickcalculation,order_create,cartadd,revise,cartsearch,cartordergo,stockonly,unitsearch
from product.cartlist import cart_list,addcart,cartrevise
from selection_screen import (Order_phonenum_screen,Single_order_confirmation_screen,Order_establishment_message,
                              Cart_join_success_message,Cancel_fail_message,Cart_order_screen,Cartordercheck_establishment_message,
                              Cartorder_establishment_message)

#-------------------使用者狀態檢查----------------------
def product_check():
    id = info.user_id
    state = info.user_state
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
    return check_text

#-------------------訂單檢查----------------------
def orderandpreorder_check():
     # 若使用者已經在等待回覆狀態，則根據回覆進行處理
    id = info.user_id
    state = info.user_state
    message = info.msg
    product = info.product
    product_id = info.product[id+'product_id']
    productname = info.product[id+'product']
    product_order_preorder = info.product_order_preorder
    message_storage = info.storage
    orderall = info.orderall
    storage_multiple = info.storage[id+'multiple']
    phone = recent_phone_call(id)#最近一筆電話取得
    if message.isdigit():
            # 處理完問題後，結束等待回覆狀態
        if state[id] == 'ordering':
            stocknum = stockonly(product_id)
            if stocknum > 0 and int(message) > 0 and int(message) <= stocknum:
                message_storage[id+'num'] = message
                message_storage[id+'ordertype'] = '現購'
                errormsg = 'no'
                check_text = Order_phonenum_screen(product_order_preorder[id],product_id,productname,errormsg,phone,message_storage[id+'num'])
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
                    check_text = Order_phonenum_screen(product_order_preorder[id],product_id,productname,errormsg,phone,message_storage[id+'num'])
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
                    check_text = Order_phonenum_screen(product_order_preorder[id],product_id,productname,errormsg,phone,message_storage[id+'num'])
                elif (len(message) > 10):
                    errormsg = f"輸入電話格式錯誤！(10碼)\n請重新打字輸入正確的電話號碼。"
                    check_text = Order_phonenum_screen(product_order_preorder[id],product_id,productname,errormsg,phone,message_storage[id+'num'])
                elif(message[:2] != '09'):           
                    errormsg = f"輸入電話格式錯誤！(09開頭)\n請重新打字輸入正確的電話號碼。"
                    check_text = Order_phonenum_screen(product_order_preorder[id],product_id,productname,errormsg,phone,message_storage[id+'num'])
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
                        check_text = Single_order_confirmation_screen(product_order_preorder[id],product_id,productname,message_storage[id+'phonenum'],
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
                        pagemin = info.list_page[info.user_id+'現購min']
                        pagemax = info.list_page[info.user_id+'現購max']
                        continue_browsing = "【現購列表下一頁】"+ str(pagemin+1) +"～"+ str(pagemax)
                        check_text = Order_establishment_message(orderinfo[2],str(orderinfo[0]),orderinfo[1],orderinfo[6],
                                                                 str(orderinfo[3]),str(orderinfo[5]),str('{:,}'.format(orderinfo[4])),
                                                                 continue_browsing,message_storage[id+'oderprice'],
                                                                 message_storage[id+'oderdiscount'],message_storage[id+'phonenum'])
                    elif numtype == '預購':
                        pagemin = info.list_page[info.user_id+'預購min']
                        pagemax = info.list_page[info.user_id+'預購max']
                        continue_browsing = "【預購列表下一頁】"+ str(pagemin+1) +"～"+ str(pagemax)
                        check_text = Order_establishment_message(orderinfo[2],str(orderinfo[0]),orderinfo[1],orderinfo[6],
                                                                 str(orderinfo[3]),str(orderinfo[5]),str('{:,}'.format(orderinfo[4])),
                                                                 continue_browsing,message_storage[id+'oderprice'],
                                                                 message_storage[id+'oderdiscount'],message_storage[id+'phonenum'])
                    state[id] = 'normal' #從user_state轉換普通狀態
                    #下方重置
                    message_storage.pop(id+'num',None) 
                    message_storage.pop(id+'phonenum',None)
                    product.pop(id+'product_id',None)
                    product.pop(id+'product_id',None)
                    product.pop(id+'product',None)
                    product_order_preorder.pop(id,None)
                    message_storage.pop(id+'ordertype',None)
                    message_storage.pop(id+'oderprice',None)
                    message_storage.pop(id+'oderdiscount',None)
                    message_storage.pop(id+'multiple',None)            
                else:
                    check_text = TextSendMessage(text=establishment_message)
                    state[id] = 'normal' #從user_state轉換普通狀態
                    #下方重置
                    message_storage.pop(id+'num',None) 
                    message_storage.pop(id+'phonenum',None)
                    product.pop(id+'product_id',None)
                    product.pop(id+'product_id',None)
                    product.pop(id+'product',None)
                    product_order_preorder.pop(id,None)
                    message_storage.pop(id+'ordertype',None)
                    message_storage.pop(id+'oderprice',None)
                    message_storage.pop(id+'oderdiscount',None)
                    message_storage.pop(id+'multiple',None) 
            elif message == '2':
                check_text = '您的商品訂/預購流程\n已經取消囉～'
                check_text = TextSendMessage(text=check_text),Cancel_fail_message(message_storage[id+'ordertype'])
                state[id] = 'normal' #從user_state轉換普通狀態
                #下方重置
                message_storage.pop(id+'num',None) 
                message_storage.pop(id+'phonenum',None)
                product.pop(id+'product_id',None)
                product.pop(id+'product_id',None)
                product.pop(id+'product',None)
                product_order_preorder.pop(id,None)
                message_storage.pop(id+'ordertype',None)
                message_storage.pop(id+'oderprice',None)
                message_storage.pop(id+'oderdiscount',None)
                message_storage.pop(id+'multiple',None) 
            else:
                check_text = Single_order_confirmation_screen(product_order_preorder[id],product_id,productname,message_storage[id+'phonenum'],
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
            message_storage.pop(id+'num',None) 
            message_storage.pop(id+'phonenum',None)
            product.pop(id+'product_id',None)
            product.pop(id+'product_id',None)
            product.pop(id+'product',None)
            product_order_preorder.pop(id,None)
            message_storage.pop(id+'ordertype',None)
            message_storage.pop(id+'oderprice',None)
            message_storage.pop(id+'oderdiscount',None)
            message_storage.pop(id+'multiple',None) 
        elif state[id] in ['ordering','preorder']:
            if state[id] == 'ordering':
                errormsg = f"您輸入的「{message}」不是此現購流程中會出現的內容喔！請重新輸入現購數量。"
                check_text = Order_buynow(errormsg)
            elif state[id] == 'preorder':
                errormsg = f"您輸入的「{message}」不是此預購流程中會出現的內容喔！請重新輸入預購數量。"
                check_text = Order_preorder(errormsg)
        elif state[id] =='phonenum':
            if message == '重新填寫':
                message_storage.pop(id+'num',None)
                message_storage.pop(id+'phonenum',None)
                errormsg = 'no'
                if product_order_preorder[id] == '現購':
                    check_text = Order_buynow(errormsg)
                elif product_order_preorder[id] == '預購':
                    check_text = Order_preorder(errormsg)
            else:
                errormsg = f"您輸入的「{message}」不是此{product_order_preorder[id]}流程中會出現的內容喔！請重新輸入聯絡電話。"
                check_text = Order_phonenum_screen(product_order_preorder[id],product_id,productname,errormsg,phone,message_storage[id+'num'])
        elif state[id] =='end':
            check_text = Single_order_confirmation_screen(product_order_preorder[id],product_id,productname,message_storage[id+'phonenum'],
                                                          message_storage[id+'num'],message_storage[id+'unitin'],
                                                          message_storage[id+'oderprice'],message_storage[id+'oderdiscount'],
                                                          message_storage[id+'subtotalin'])
        else:
            check_text = '您還在訂/預購中喔！\n輸入的 "' + message + '" 不是此流程的填寫！\n請重新輸入，謝謝～'
            check_text = TextSendMessage(text=check_text),TextSendMessage(text='訂/預購流程中，如想取消請打字輸入" 取消 "')    
    return check_text

#購物車商品新增
def cartnum():
    id = info.user_id
    state = info.user_state
    message = info.msg
    product_id = info.product[id+'cartproduct_id']
    product = info.product
    productname = info.product[id+'cartproduct']

    pagemin = info.list_page[info.user_id+'現購min']
    pagemax = info.list_page[info.user_id+'現購max']
    continue_browsing = "【現購列表下一頁】"+ str(pagemin+1) +"～"+ str(pagemax)
    
    if message.isdigit():#是數字
        text = cartadd(id,product_id,int(message))
        if text == 'ok':
            unit = unitsearch(product_id)
            check_text = Cart_join_success_message(productname,product_id,message,unit,continue_browsing)
            state[id] = 'normal' #結束流程將user_state轉換預設狀態
            product.pop(id+'cartproduct_id',None)
            product.pop(id+'cartproduct',None)
        else:
            check_text = TextSendMessage(text='購物車加入失敗！請稍後再試。')
            product.pop(id+'cartproduct_id',None)
            state[id] = 'normal' #結束流程將user_state轉換預設狀態
            product.pop(id+'cartproduct',None)
    else:
        if(message == "取消"):
            check_text = '您的商品加入購物車流程\n已經取消囉～'
            check_text = TextSendMessage(text=check_text),Cancel_fail_message('現購')
            state[id] = 'normal' #結束流程將user_state轉換預設狀態
            product.pop(id+'cartproduct_id',None)
            product.pop(id+'cartproduct',None)
        else:
            errormsg = f"您輸入的「{message}」內容並非數字喔！請重新輸入數量。"
            check_text = addcart(errormsg)
    return check_text

#購物車數量修改
def cartrpnum():
    id = info.user_id
    state = info.user_state
    message = info.msg
    product_iid = info.product
    product_id = info.product[id+'cartreviseproduct_id']
    if message.isdigit():#是數字
        stocknum = stockonly(product_id)
        if stocknum > 0 and int(message) > 0 and int(message) <= stocknum:
            text = revise(id,product_id,int(message))
            if text == 'ok':
                check_text = cart_list()
                state[id] = 'normal' #結束流程將user_state轉換預設狀態
                product_iid.pop(id+'cartreviseproduct_id',None)
            else:
                check_text = TextSendMessage(text='購物車商品數量修改失敗！請稍後再試。')
                state[id] = 'normal' #結束流程將user_state轉換預設狀態
                product_iid.pop(id+'cartreviseproduct_id',None)
        else:
            errormsg = f"您輸入的「{message}」大於現在的庫存數量，請重新輸入。\n目前庫存{stocknum}"
            check_text = cartrevise(errormsg)
    else:
        if(message == "取消"):
            check_text = TextSendMessage(text='您的購物車商品數量修改流程\n已經取消囉～')
            check_text = check_text,cart_list()
            state[id] = 'normal' #結束流程將user_state轉換預設狀態
            product_iid.pop(id+'cartreviseproduct_id',None)
        else:
            errormsg = f"您輸入的「{message}」不在修改購物車數量中的內容喔！"
            check_text = cartrevise(errormsg)
    return check_text

#購物車訂單
def cartorder():
    id = info.user_id
    state = info.user_state
    message = info.msg
    message_storage = info.storage
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
            message_storage.pop(id+'cartodinfo_id',None) #商品ID
            message_storage.pop(id+'cartodinfo_name',None) #商品名稱
            message_storage.pop(id+'cartodinfo_num',None) #商品數量
            message_storage.pop(id+'cartodinfo_unit',None) #商品單位
            message_storage.pop(id+'cartodinfo_subtotal',None) #商品小計
            message_storage.pop(id+'shownum',None) #總額
            message_storage.pop(id+'phonenum',None) #電話
            state[id] = 'normal' #從user_state轉換普通狀態
    else:
        if(message == "取消"):
            check_text = '您的購物車訂單流程\n已經取消囉～'
            message_storage.pop(id+'showp',None) #訂單資訊(之後刪)####
            message_storage.pop(id+'cartodinfo_id',None) #商品ID
            message_storage.pop(id+'cartodinfo_name',None) #商品名稱
            message_storage.pop(id+'cartodinfo_num',None) #商品數量
            message_storage.pop(id+'cartodinfo_unit',None) #商品單位
            message_storage.pop(id+'cartodinfo_subtotal',None) #商品小計
            message_storage.pop(id+'shownum',None) #總額
            message_storage.pop(id+'phonenum',None)
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

