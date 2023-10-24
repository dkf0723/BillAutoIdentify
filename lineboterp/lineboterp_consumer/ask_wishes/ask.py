from linebot.models import *
from product.buy_now import *
from product.product_preorder import *
import lineboterp
from database import databasetest

def ask():
    id = lineboterp.user_id
    state = lineboterp.user_state
    message = lineboterp.msg
    return