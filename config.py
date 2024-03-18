import os
TOKEN = os.environ['TOKEN']
ADMINS = [int(os.environ['ADMIN_1'])]
SBERBANK = os.environ['SBERBANK']
TINKOFF = os.environ['TINKOFF']
ADVERTISING_MANAGER = os.environ['ADVERTISING_MANAGER'] # ник без `@`!
MODERATION_CHAT_ID = os.environ['MODERATION_CHAT_ID']
OPINION_TIME = 15
VIOLATIONS_COUNT_FOR_MUT = 4 
BOT_NICKAME = 'AnonymousAlatyr_bot'
MUT_TIME = 1 # в часах
CLEANER_PERIOD = 180 # в минутах
TIME_BETWEEN_SENDLER_MESSAGE = 5 # в секундах