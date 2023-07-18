from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from product.buy_now import *
from product.product_preorder import *
import lineboterp
from database import databasetest

def wishes():
    id = lineboterp.user_id
    state = lineboterp.user_state
    message = lineboterp.msg
    return