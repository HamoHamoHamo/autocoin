import requests
import re
import os
import pyupbit
import threading
import time
import pandas as pd
from pandas import Series, DataFrame
from datetime import timedelta, datetime, date
from telegrambot import send_log, send_message



#pd.set_option('display.max_columns', None) ## 모든 열을 출력한다.


#'KRW-BTC', 'KRW-ETH', 'KRW-CHZ', 'KRW-XRP', 티커 목록 제외
tickers_list = ('KRW-BTC', 'KRW-ETH', 'KRW-NEO', 'KRW-MTL', 'KRW-LTC', 'KRW-XRP', 'KRW-ETC', 'KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM', 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR', 'KRW-KMD', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-REP', 'KRW-EMC2', 'KRW-ADA', 'KRW-SBD', 'KRW-POWR', 'KRW-BTG', 'KRW-ICX', 'KRW-EOS', 'KRW-TRX', 'KRW-SC', 'KRW-IGNIS', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', 'KRW-ZRX', 'KRW-LOOM', 'KRW-BCH', 'KRW-ADX', 'KRW-BAT', 'KRW-IOST', 'KRW-DMT', 'KRW-RFR', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-MFT', 'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC', 'KRW-BSV', 'KRW-THETA', 'KRW-EDR', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC', 'KRW-ENJ', 'KRW-TFUEL', 'KRW-MANA', 'KRW-ANKR', 'KRW-AERGO', 'KRW-ATOM', 'KRW-TT', 'KRW-CRE', 'KRW-SOLVE', 'KRW-MBL', 'KRW-TSHP', 'KRW-WAXP', 'KRW-HBAR', 'KRW-MED', 'KRW-MLK', 'KRW-STPT', 'KRW-ORBS', 'KRW-VET', 'KRW-CHZ', 'KRW-PXL', 'KRW-STMX', 'KRW-DKA', 'KRW-HIVE', 'KRW-KAVA', 'KRW-AHT', 'KRW-STRK', 'KRW-PUNDIX', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA', 'KRW-JST', 'KRW-CRO', 'KRW-TON', 'KRW-SXP', 'KRW-LAMB', 'KRW-HUNT', 'KRW-MARO', 'KRW-PLA', 'KRW-DOT', 'KRW-SRM', 'KRW-MVL', 'KRW-PCI', 'KRW-STRAX', 'KRW-AQT', 'KRW-BCHA', 'KRW-GLM', 'KRW-QTCON', 'KRW-SSX', 'KRW-META', 'KRW-OBSR', 'KRW-FCT2', 'KRW-LBC', 'KRW-CBK', 'KRW-SAND', 'KRW-HUM', 'KRW-DOGE')
#tickers_list = ('KRW-BTC', 'KRW-ETH', 'KRW-NEO', 'KRW-MTL', 'KRW-LTC', 'KRW-XRP', 'KRW-ETC', 'KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM', 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR', 'KRW-KMD', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-REP', 'KRW-EMC2', 'KRW-ADA', 'KRW-SBD', 'KRW-POWR', 'KRW-BTG', 'KRW-ICX', 'KRW-EOS', 'KRW-TRX', 'KRW-SC', 'KRW-IGNIS', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', 'KRW-ZRX', 'KRW-LOOM', 'KRW-BCH', 'KRW-ADX', 'KRW-BAT', 'KRW-IOST', 'KRW-DMT', 'KRW-RFR', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-MFT', 'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC', 'KRW-BSV', 'KRW-THETA', 'KRW-EDR', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC', 'KRW-ENJ', 'KRW-TFUEL', 'KRW-MANA', 'KRW-ANKR', )

count = len(tickers_list)
buy_ticker =  []
#buy_price =  []
ticker_data =  []

def get_top_price():
    now=datetime.now()
    
    today = str(now)[:10]
    text = "오늘날짜" + today
    send_message(text,)
    print("현재 시간", now)

    # gcp에서 시간이 우리나라 시간 -9시간 이라서 필요없음
    '''
    if now.hour >= 15:
        today = str(now - timedelta(days=1))[:10]
    '''
    for ticker in tickers_list:
        url = "https://api.upbit.com/v1/candles/days"

        #querystring = {"market":ticker,"to":"{0} 00:00:00".format(str(datetime.now()+timedelta(days=1))[:10]),"count":"1"}
        querystring = {"market":ticker,"to":"{0} 00:00:00".format(today),"count":"1"}
        #querystring = {"market":ticker,"to":"2021-03-17 00:00:00","count":"1"}
        #print(querystring)
        response = requests.request("GET", url, params=querystring)
        #print(response.text)    

        results = response.text.split('},')
        #print(results)
        r = []

        candle_time = []
        open = []
        high = []
        low = []
        close = []
        price = []
        volume = []
        close_percent = []
        high_percent = []
        low_percent = []

        #df_today = pyupbit.get_ohlcv(ticker, interval="day", count=1)
        #today_open = float(df_today['open'])

        save = False
        for result in reversed(results):
            result=result.replace('[','')
            result=result.replace('{','')
            result=result.replace(']','')
            result=result.replace('}','')
            
            #날짜
            date = result[result.find('","opening_price') - (result.find('","opening_price') - result.find('candle_date_time_kst":"') - len('candle_date_time_kst":"')):result.find('","opening_price')]
            candle_time.append(date)
            #print(time)

            #시가
            open_price = result[result.find('0000,"high_price"') - (result.find('0000,"high_price"') - result.find('"opening_price":') - len('"opening_price":')):result.find('0000,"high_price"')]
            open.append(open_price)
            #print(open_price) 

            #고가
            high_price = result[result.find('0000,"low_price"') - (result.find('0000,"low_price"') - result.find('"high_price":') - len('"high_price":')):result.find('0000,"low_price"')]
            high.append(high_price)
            #high_percent_candle = (float(high_price) - today_open) / today_open * 100
            #high_percent.append(high_percent_candle)

            #print(high_price)
            #저가
            low_price = result[result.find('0000,"trade_price":') - (result.find('0000,"trade_price":') - result.find('"low_price":') - len('"low_price":')):result.find('0000,"trade_price":')]
            low.append(low_price)
            #low_percent_candle = (float(low_price) - today_open) / today_open * 100
            #low_percent.append(low_percent_candle)
            #print(low_price)
            #종가
            close_price = result[result.find('0000,"timestamp":') - (result.find('0000,"timestamp":') - result.find(',"trade_price":') - len(',"trade_price":')):result.find('0000,"timestamp":')]
            close.append(close_price)
            #print(close_price)
            #close_percent_candle = (float(close_price) - today_open) / today_open * 100
            #close_percent.append(close_percent_candle)
            #거래대금
            trade_price = result[result.find(',"candle_acc_trade_volume":') - (result.find(',"candle_acc_trade_volume":') - result.find('"candle_acc_trade_price":') - len('"candle_acc_trade_price":')):result.find(',"candle_acc_trade_volume":')]
            price.append(trade_price)    
            ##print(trade_price)
            #거래량
            trade_volume = result[result.find(',"prev_closing_price"') - (result.find(',"prev_closing_price"') - result.find('"candle_acc_trade_volume":') - len('"candle_acc_trade_volume":')):result.find(',"prev_closing_price"')]
            volume.append(trade_volume)
            ##print(trade_volume)
            
            # 차이/시가 *100
            #등락률

            #if float(high_price) >= today_open*1.07:
            #    save = True


        data = {'시가' : open,
                '고가' : high,
                '저가' : low,
                '종가' : close,
                '거래대금' : price,
                '거래량' : volume,
                }
        
        df = DataFrame(data, index=candle_time)
        df['range'] = (float(df['고가']) - float(df['저가'])) * 0.032
        
        target_price = round(float(df['종가']) + float(df['range']), 1)
        # 목표가가 100 이상이면 정수형으로 변환
        if target_price >= float(100):
            target_price = int(target_price)
        
        if target_price >= float(1000000) and str(target_price)[-3] != "0":
            target_price = int(str(target_price)[:-3] + "000")         
        elif target_price >= float(100000) and str(target_price)[-2] != "0":
            target_price = int(str(target_price)[:-2] + "00")
        elif target_price >= float(10000) and str(target_price)[-1] != "0":
            target_price = int(str(target_price)[:-1] + "0")
        elif target_price >= float(1000) and str(target_price)[-1] != "0":
            target_price = int(str(target_price)[:-1] + "5")             
        

        df['target'] = target_price

        # txt파일에 저장
        #log_list = [ticker, df]
        #save_log(log_list)

        # 텔레그램으로 로그 전송
        #t = threading.Thread(target=send_telgm_log, args=(log_list,)) # 스레드 생성
        #t.start()

        '''
        min_price = min(buy_price)
        pr = float(data['거래대금'][0])
        pr = int(pr)
        if min_price < pr:
            num = buy_price.index(min_price)
            buy_price[num] = pr
            buy_ticker[num] = ticker
            ticker_data[num] = df
        print("buy_price", buy_price)
        '''
        print("buy_ticker", buy_ticker)
        buy_ticker.append(ticker)
        ticker_data.append(df)
        time.sleep(0.15)

        #print(buy_ticker, buy_price)


    
    buy_list = [buy_ticker, ticker_data, True]
    
    '''
    if now.hour >= 15:
        data_date = str(now - timedelta(days=2))[:10]
    else:
    '''
    data_date = str(now - timedelta(days=1))[:10]
    res = read_log()

    # 오늘 날짜 -1 이 저장된 로그 날짜와 같으면 구매완료 목록 초기화 안함
    if data_date == res:
        buy_list[2] = False

    
    # 거래대금 상위 종목 저장 및 텔레그램 메시지 전송
    t2 = threading.Thread(target=save_buy_list, args=(buy_list,)) # 스레드 생성
    t2.start()
    t2.join()


    print("===========종목 업데이트 완료===========\n\n\n\n\n")
    t_start = threading.Thread(target=send_message, args=("감시 시작",)) # 스레드 생성
    t_start.start()

    

    return buy_list

def read_log():
    with open("day_candle_log.txt", "r", encoding='utf8') as f:
        lines = f.readlines()
        res = str(lines[-3])[:10]
        print("read log", res)
    return res

def save_buy_list(get_list):
    # "a"는 현재내용에 추가 "w"는 새로 작성
    with open("day_candle_log.txt", "a", encoding='utf8') as f:
        for cnt in range(count):
            #print(get_list[1][cnt], get_list[0][cnt], get_list[2][cnt])
            f.write(str(get_list[0][cnt]) + str(get_list[1][cnt]) + "\n")
            text = "종목 업데이트\n" + get_list[0][cnt] + "\n날짜 : " + str(get_list[1][cnt].index[0]) +  "\n시가 : {0}\n고가 : {1}\n저가 : {2}\n종가 : {3}\nRANGE : {4}\n목표가 : {5} ".format(float(get_list[1][cnt]['시가']),float(get_list[1][cnt]['고가']),float(get_list[1][cnt]['저가']),float(get_list[1][cnt]['종가']),float(get_list[1][cnt]['range']),float(get_list[1][cnt]['target']))
            #print(text)
            send_log(text)


def save_log(get_list):    
    # "a"는 현재내용에 추가 "w"는 새로 작성
    with open("day_candle_log.txt", "a", encoding='utf8') as f:
        f.write(str(get_list[0]) + str(get_list[1]) + "\n")
    
    
def send_telgm_log(get_list):
    
    text = "\n날짜 : " + str(get_list[0].index[0]) + "\n시가 : {0}\n고가 : {1}\n저가 : {2}\n종가 : {3}\nRANGE : {4}\n목표가 : {5} ".format(float(get_list[0]['시가']),float(get_list[0]['고가']),float(get_list[0]['저가']),float(get_list[0]['종가']),float(get_list[0]['range']),float(get_list[0]['target']))
    #print(text)
    send_log(text)

# 거래대금 상위 5종목 가져오기
#check=True
#get_list = get_top_price()
#print("END")



'''
t = threading.Thread(target=get_top_price, args=(True,)) # 스레드 생성
t.start()
time.sleep(0.2)
for t in threads:
    t.start()  # 스레드 실행

for thread in t:
    thread.join()  # 스레드 종료

'''