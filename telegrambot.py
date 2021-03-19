import telegram


f = open("telegram_token.txt", encoding='utf8')
lines = f.readlines()
telgm_token = lines[1].strip()
chat_id = lines[2].strip()
message_bot = telegram.Bot(token = telgm_token)

log_token = lines[5].strip()
log_chat_id = lines[6].strip()
log_bot = telegram.Bot(token = log_token)




def send_message(text):
    message_bot.sendMessage(chat_id=chat_id, text=text)

def send_log(text):
    log_bot.sendMessage(chat_id=log_chat_id, text=text)