from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import manager

#------------------原本以下要換位置-----------------------
def exist_goods(goods_name): 
    dict_data = manager.dict_data
    """判斷商品是否已經存在""" 
    if goods_name in dict_data:
        message = '有'
    else:
        message = '沒有'
    return message

#'新增商品'
def add_goods(): 
    dict_data = manager.dict_data    
    """補貨""" 
    goods_name = '雞排'
    goods_count = 10  #'進貨数量:'
    # 該商品是否已經存在
    if  exist_goods(goods_name) == '有': 
        # 如果該商品已經存在
        # 就添加對應的數量
        dict_data[goods_name]['inventory'] += goods_count  #添加對應的庫存
    else:
        goods_factory = '哈哈公司'
        goods_cost = 30
        goods_exp ='2023.12.01'
        goods_price = 60
        # 把商品資訊加到字典
        dict_data[goods_name] = {'price': goods_price,'cost':goods_cost,'inventory': goods_count,'sales': 0,'factory':goods_factory,'exp':goods_exp}
    message = (f'{goods_name}補貨成功，目前庫存為{dict_data[goods_name]["inventory"]}')
    return TextSendMessage(text= message)

# 出售商品//
def sell_goods():
    dict_data = manager.dict_data
    """出售商品，庫存減少，銷量增加"""
    goods_name = '雞排'
    if exist_goods(goods_name) == '有':
        goods_count = 2
        dict_data[goods_name]['inventory'] -= goods_count  # 添加對應的庫存
        dict_data[goods_name]['sales'] += goods_count  # 統計總銷量
        message = '銷售成功'
    else:
        message = '商品不存在111'
    return TextSendMessage(text= message)

# 查詢個別商品資訊
def select_goods():
    dict_data = manager.dict_data
    """查詢個別商品資訊"""
    goods_name = '雞排'
    if exist_goods(goods_name) == '有':
        message = (f'{dict_data[goods_name]}')
    else:
        message = '商品不存在222' 
    return TextSendMessage(text= message)

# 查詢所有商品資訊//
def select_all_goods():
    dict_data = manager.dict_data
    """查詢所有商品資訊"""
    for i in dict_data.items():
        message = i 
    return TextSendMessage(text= message)
#------------------------------------------------
