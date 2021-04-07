import pyupbit
import os
import time
import sys
from datetime import timedelta, datetime, date
import requests
import time
import requests
import json
import websockets
import asyncio
import threading
from day_candle import get_top_price
from telegrambot import send_message, send_log

UPBIT_WEB_SOCKET_ADD = 'wss://api.upbit.com/websocket/v1'

HOLD_CHECK = []

f = open("upbit_key.txt")
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()
upbit = pyupbit.Upbit(access,secret)

async def do_async_loop(ticker, target, reset):
    #list_coin = []
    #list_coin.append(ticker)
    update_time = '00:00'
    
    break_check = False
    connect_check = False

    #money = 100000
    money = 15000
    #money=0
    #count = int(money/target)

    buy_check = {}
    # buy_check 저장된 값 불러오기
    if reset == False:
        read_check = []
        with open("buy_check.txt", "r", encoding='utf8') as f:
            lines = f.readlines()
            line = lines[0].split(":")
            
        for i in range(len(line)):
            if "True" in line[i]:
                read_check.append(True)
            if "False" in line[i]:
                read_check.append(False)
        for y in range(len(ticker)):
            buy_check[ticker[y]] = read_check[y]
        print("불러옴")
    else:
        # buy_check['티커'] = True 로 초기값 넣어주기
        for i in ticker:
            buy_check[i] = True
        with open("buy_check.txt", "w", encoding='utf8') as f:
            text = str(buy_check) + "\n"
            f.write(text)

    text = "구매 완료 목록 확인 " + str(buy_check)
    send_message(text,)
    print(text)

    async with websockets.connect(UPBIT_WEB_SOCKET_ADD, ping_interval=None) as websocket:
        # ss format ex : '[{"ticket":"test1243563456"},{"type":"trade","codes":["KRW-BTC", "KRW-ETH"]}]'
        ss = '[{"ticket":"test1243563456"},{"type":"ticker","codes":' + str(ticker).replace("'", '"') +'}]'
        await websocket.send(ss)
            
        while(1) :
            try:
                data_rev = await websocket.recv()
                my_json = data_rev.decode('utf8').replace("'", '"')
                data = json.loads(my_json)
                now_ticker = data['code']

                # 00초일때 연결확인용으로 프린트
                if str(datetime.now())[17:19] == '00':
                    print(data['code'], data['trade_time'], data['trade_price'])
                
                # 30분마다 연결확인 텔레그램 메시지 보내기
                if str(datetime.now())[14:16] != '30':
                    connect_check = True
                if str(datetime.now())[14:16] == '30' and connect_check == True:
                    text = "연결확인\n" + str(buy_check)
                    checking_message = threading.Thread(target=send_log, args=(text,)) # 스레드 생성
                    checking_message.start()
                    connect_check = False
                

                # 현재가가 목표가가 되면 매수 주문 넣고 매시지 보내기
                if target[now_ticker] == data['trade_price'] and buy_check[now_ticker] == True:
                    count = float(money/int(target[now_ticker]))
                    ret = upbit.buy_limit_order(now_ticker, target[now_ticker], count)
                    print("주문완료\n",ret, count)

                    with open("buy_log.txt", "a", encoding='utf8') as f:
                        text = "\n" + str(datetime.now()) + str(ret)
                        f.write(text)

                    buy_check[now_ticker] = False
                    with open("buy_check.txt", "w", encoding='utf8') as f:
                        text = str(buy_check) + "\n"
                        f.write(text)

                    # ret type은 dict
                    
                    text= "주문 완료\n종류 : {0}\n매수가격 : {1}\n시간 : {2}\n수량 : {3}".format(str(ret['market']), float(ret['price']), str(ret['created_at']), float(ret['volume']))
                    #send_message(text)
                    # 스레드로 텔레그램 메시지 전송하면 에러 남 문자열이 쪼개져서 들어가는듯
                    # TypeError: send_message() takes 1 positional argument but 71 were given
                    # ars를 2개로 주면 됨 뭐야 이거 >> args에 , 찍어줘야됨 
                    t_buy_log = threading.Thread(target=send_message, args=(text,)) # 스레드 생성
                    t_buy_log.start()

                    t_update = threading.Thread(target=send_target_message, args=(data['code'], data['trade_price'], buy_check)) # 스레드 생성
                    t_update.start()
                    
            except Exception as e:
                print("=========ERROR=======")
                print(e)
                send_message(str(e),)
                with open("error_log.txt", "a", encoding='utf8') as f:
                    text = str(datetime.now()) + str(e) + "\n"
                    f.write(text)

                if str(e) == "code = 1006 (connection closed abnormally [internal]), no reason":
                    print("프로그램 종료")
                    sys.exit("프로그램 종료")

            # 지정된 시간이 되면 멈추고 종목 업데이트
            if str(datetime.now())[11:16] != update_time:
                break_check = True
            if str(datetime.now())[11:16] == update_time and break_check == True:
                print("==============BREAK==============")
                print(datetime.now())
                break_check = False
                
                break
            
    return "END"

async def sell_all():
    # 우리나라 시간은  +9시간 해야됨
    sell_time = '23:59'
    
    sell_check = True
    percent = 1

    # 09:00이 되면 전부 매도
    while(1) :
        now = datetime.now()
        print(now)
        await asyncio.sleep(10)
        if str(now)[11:16] != sell_time:
                sell_check = True
        if str(datetime.now())[11:16] == sell_time and sell_check == True:
            sell_check = False
            balances = upbit.get_balances()

            text = str(datetime.now()) + "\n===============매도 전 잔고===============\n"
            send_message(text,)
            print(text)
            with open("sell_log.txt", "a", encoding='utf8') as f:
                f.write(text)

            for i in balances:
                print(i)
                with open("sell_log.txt", "a", encoding='utf8') as f:
                    text = str(datetime.now()) + str(i) + "\n"
                    f.write(text)
                
                if i['currency'] == "KRW":
                    send_message(text,)
                    continue
                try:
                    ret = upbit.sell_market_order("KRW-{}".format(i['currency']), float(i['balance'])*percent)
                    price = float(i['avg_buy_price']) * float(i['balance'])
                    text="종류 : " + i['currency'] + "\n주문가능금액/수량 : " + i['balance'] + "\n주문 중 묶여있는 금액/수량 : " + i['locked']+ "\n평단가 : " + i['avg_buy_price'] + "\n금액 : " + str(price)
                    t_sell_log = threading.Thread(target=send_message, args=(text,)) # 스레드 생성
                    t_sell_log.start()
                    t_sell_log.join()
                    print(text)

                    #print(ret)
                    print("sell", i['currency'])
                except Exception as e:
                    print(i['currency'], "에러발생")
                    print(e)

            text = "===============매도 후 잔고==============="
            send_message(text,)
            print(text)

            await asyncio.sleep(3)
            with open("sell_log.txt", "a", encoding='utf8') as f:
                f.write("매도 후 잔고\n")
            for i in upbit.get_balances():
                with open("sell_log.txt", "a", encoding='utf8') as f:
                    text = str(datetime.now()) + str(i) + "\n"
                    f.write(text)

                text="종류 : " + i['currency'] + "\n주문가능금액/수량 : " + i['balance'] + "\n주문 중 묶여있는 금액/수량 : " + i['locked']
                t2_sell_log = threading.Thread(target=send_message, args=(text,)) # 스레드 생성
                t2_sell_log.start()
                t2_sell_log.join()
            print("SELL END")
            break
    return ("SELL END")
        


async def trading_main(trading_coins, run_check, target):
    #while(run_check):
    print("================================START================================")
    loop1 = do_async_loop(trading_coins[0], target, trading_coins[2])
    #loop2 = do_async_loop(trading_coins[1][1], target[1])
    #loop3 = do_async_loop(trading_coins[1][2], target[2])
    #loop4 = do_async_loop(trading_coins[1][3], target[3])
    #loop5 = do_async_loop(trading_coins[1][4], target[4])
    #loop6 = do_async_loop(trading_coins[1][5], target[5])
    #loop7 = do_async_loop(trading_coins[1][6], target[6])
    #loop8 = do_async_loop(trading_coins[1][7], target[7])
    #loop9 = do_async_loop(trading_coins[1][8], target[8])
    #loop10 = do_async_loop(trading_coins[1][9], target[9])
    sell = sell_all()
    stop_check = await asyncio.gather(
        sell,
        loop1,
        #loop2,
        #loop3,
        #loop4,
        #loop5,
        #loop6,
        #loop7,
        #loop8,
        # loop9,
        # loop10,
    )
    time.sleep(1)
    print(stop_check)
    print("===========09시 종목 업데이트===========")
    sys.exit("프로그램 종료")
        


def send_target_message(ticker, price, check):

    text = str(ticker) + "\n현재가 : " + str(price) + "\n" + str(check)
    send_message(text)
    print("메시지 전송", text)


def testtest(trading_coins):
    while(1):
        print("==============START==============")
        asyncio.get_event_loop().run_until_complete(do_async_loop(trading_coins))
        time.sleep(1)

target_list = {}

buy_list = get_top_price()
#buy_list = [[470853572636, 649622744160, 2307348519849, 941919650445, 838187329117], ['KRW-META', 'KRW-CHZ', 'KRW-STMX', 'KRW-DKA', 'KRW-MVL']]

for i in range(len(buy_list[1])):
    target_list[buy_list[0][i]] = (float(buy_list[1][i]['target']))

#print("==================================\n", target_list['KRW-ETH'])


asyncio.get_event_loop().run_until_complete(trading_main(buy_list, True, target_list))

print("END")