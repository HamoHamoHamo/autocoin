import pyupbit
import time
import threading
from telegrambot import send_message
from day_candle import get_top_price
from datetime import timedelta, datetime, date

def send_target_message(ret):
    text = ret
    send_message(text)
    print("메시지 전송", text)


scan_ticker = True

f = open("upbit_key.txt")
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()

upbit = pyupbit.Upbit(access,secret)



if upbit.get_balance('KRW') is not None:
    send_message("업비트에 성공적으로 로그인 하였습니다")
    login = True
    

    for i in upbit.get_balances():
        text="종류 : " + i['currency'] + "\n주문가능금액/수량 : " + i['balance'] + "\n주문 중 묶여있는 금액/수량 : " + i['locked']+ "\n평단가 : " + i['avg_buy_price']
        print(text)
        #if i['currency'] == 'META':
        #  print("메타========================================")
        #t = threading.Thread(target=send_target_message, args=("메타========================================",)) # 스레드 생성
        #t.start()
        
else:
  send_message("로그인에 실패하였습니다")

#ret = upbit.sell_market_order("KRW-IGNIS", 50)
# 시장가 매도 시 갯수 입력

#ret = upbit.sell_limit_order("KRW-META", 10000, 5)
#print(ret)


'''
now=datetime.now()
if now.hour == 8 and now.minute == 59 and scan_ticker == True:
  try:
    buy_list = get_top_price(scan_ticker)
    text = '전날 거래 대금 상위 5종목 : ' + buy_list[1]
    print(text)
    send_message(text)
    scan_ticker == False
  except Exception as e:
    text = "거래대금 불러오기 에러발생" 
    print(text, e)
    send_message(text + e)
  '''

#upbit.buy_market_order(tickers, NKR*0.2)
#print(buy)
