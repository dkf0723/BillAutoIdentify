# from linebot import LineBotApi, WebhookHandler
# # 載入對應的函式庫
# from linebot.models import *
# line_bot_api = LineBotApi('KuaXaQ9Xkb3HUPhlYh+NkB1mtGHzvL6pt2aSFDOkM/ZDdQBKEus7vqSfw0K5t8aN4FK9O7eqJWIOhLAzf6l2WL/fyxwlW4DtH3RRv8C4aJx9gRd8wRBBCYZlp++4x/TBFmrksxOE+91yuI0W0d7HDwdB04t89/1O/w1cDnyilFU=')
# # 剛剛 Flex Message 的 JSON 檔案就貼在下方
# user_ids = 'Uc889c85fdfd36d82a427672383a73572'#培,我,蓉
# import mysql.connector
# from mysql.connector import errorcode
# #-------------------------------
# actions = []
# options = ["a", "b", "c"]
# for option in options:
#     actions.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
# line_bot_api.push_message(user_ids, TextSendMessage(text='請點選以下操作功能', quick_reply=QuickReply(items=actions)))
