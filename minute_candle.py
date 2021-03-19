import requests
import datetime
import re
import os
import pyupbit
import threading
import time
from pandas import Series, DataFrame



def data(ticker):
    url = "https://api.upbit.com/v1/candles/minutes/1"
    
    #to: 에 있는 날짜 바꿔주면 다른 날짜 데이터 얻어올 수 있음
    # 시간은 +9시간한게 우리나라 시간 지금은 11:00에서 1분봉 121개 가져옴 그래서 09:00 ~ 11:00 1분봉을 다 받아옴
    # count는 최대가 200, 다른시간대도 받으려면 for문 더 돌려야됨
    
    querystring = {"market":ticker,"to":"2021-03-10 02:01:00","count":"121"}

    response = requests.request("GET", url, params=querystring)

    results = response.text.split('},')
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

    df_today = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    today_open = float(df_today['open'])

    save = False
    for result in reversed(results):
        result=result.replace('[','')
        result=result.replace('{','')
        result=result.replace(']','')
        result=result.replace('}','')
        
        #날짜
        time = result[result.find('","opening_price') - (result.find('","opening_price') - result.find('candle_date_time_kst":"') - len('candle_date_time_kst":"')):result.find('","opening_price')]
        candle_time.append(time)
        #print(time)

        #시가
        open_price = result[result.find('0000,"high_price"') - (result.find('0000,"high_price"') - result.find('"opening_price":') - len('"opening_price":')):result.find('0000,"high_price"')]
        open.append(open_price)
        #print(open_price) 

        #고가
        high_price = result[result.find('0000,"low_price"') - (result.find('0000,"low_price"') - result.find('"high_price":') - len('"high_price":')):result.find('0000,"low_price"')]
        high.append(high_price)
        high_percent_candle = (float(high_price) - today_open) / today_open * 100
        high_percent.append(high_percent_candle)

        #print(high_price)
        #저가
        low_price = result[result.find('0000,"trade_price":') - (result.find('0000,"trade_price":') - result.find('"low_price":') - len('"low_price":')):result.find('0000,"trade_price":')]
        low.append(low_price)
        low_percent_candle = (float(low_price) - today_open) / today_open * 100
        low_percent.append(low_percent_candle)
        #print(low_price)
        #종가
        close_price = result[result.find('0000,"timestamp":') - (result.find('0000,"timestamp":') - result.find(',"trade_price":') - len(',"trade_price":')):result.find('0000,"timestamp":')]
        close.append(close_price)
        #print(close_price)
        close_percent_candle = (float(close_price) - today_open) / today_open * 100
        close_percent.append(close_percent_candle)
        #거래대금
        trade_price = result[result.find(',"candle_acc_trade_volume":') - (result.find(',"candle_acc_trade_volume":') - result.find('"candle_acc_trade_price":') - len('"candle_acc_trade_price":')):result.find(',"candle_acc_trade_volume":')]
        price.append(trade_price)    
        ##print(trade_price)
        #거래량
        trade_volume = result[result.find(',"unit"') - (result.find(',"unit"') - result.find('"candle_acc_trade_volume":') - len('"candle_acc_trade_volume":')):result.find(',"unit"')]
        volume.append(trade_volume)
        ##print(trade_volume)
        
        # 차이/시가 *100
        #등락률

        if float(high_price) >= today_open*1.07:
            save = True


    data = {'시가' : open,
            '고가' : high,
            '저가' : low,
            '종가' : close,
            '거래대금' : price,
            '거래량' : volume,
            '고가%' : high_percent,
            '저가%' : low_percent,
            '종가%' : close_percent,
            }
    df = DataFrame(data, index=candle_time)
    
    base_dir = 'C:/Users/Shin/autocoin/data'
    file_name = ticker + '.xlsx'
    xlxs_dir = os.path.join(base_dir, file_name) 
    if save == True:
        print(df)
        df.to_excel(xlxs_dir)
    print(file_name+"완료")
    return None

tickers_list = ('KRW-BTC', 'KRW-ETH', 'KRW-NEO', 'KRW-MTL', 'KRW-LTC', 'KRW-XRP', 'KRW-ETC', 'KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM', 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR', 'KRW-KMD', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-REP', 'KRW-EMC2', 'KRW-ADA', 'KRW-SBD', 'KRW-POWR', 'KRW-BTG', 'KRW-ICX', 'KRW-EOS', 'KRW-TRX', 'KRW-SC', 'KRW-IGNIS', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', 'KRW-ZRX', 'KRW-SRN', 'KRW-LOOM', 'KRW-BCH', 'KRW-ADX', 'KRW-BAT', 'KRW-IOST', 'KRW-DMT', 'KRW-RFR', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-MFT', 'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC', 'KRW-BSV', 'KRW-THETA', 'KRW-EDR', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC', 'KRW-ENJ', 'KRW-TFUEL', 'KRW-MANA', 'KRW-ANKR', 'KRW-NPXS', 'KRW-AERGO', 'KRW-ATOM', 'KRW-TT', 'KRW-CRE', 'KRW-SOLVE', 'KRW-MBL', 'KRW-TSHP', 'KRW-WAXP', 'KRW-HBAR', 'KRW-MED', 'KRW-MLK', 'KRW-STPT', 'KRW-ORBS', 'KRW-VET', 'KRW-CHZ', 'KRW-PXL', 'KRW-STMX', 'KRW-DKA', 'KRW-HIVE', 'KRW-KAVA', 'KRW-AHT', 'KRW-SPND', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA', 'KRW-JST', 'KRW-CRO', 'KRW-TON', 'KRW-SXP', 'KRW-LAMB', 'KRW-HUNT', 'KRW-MARO', 'KRW-PLA', 'KRW-DOT', 'KRW-SRM', 'KRW-MVL', 'KRW-PCI', 'KRW-STRAX', 'KRW-AQT', 'KRW-BCHA', 'KRW-GLM', 'KRW-QTCON', 'KRW-SSX', 'KRW-META', 'KRW-OBSR', 'KRW-FCT2', 'KRW-LBC', 'KRW-CBK', 'KRW-SAND', 'KRW-HUM', 'KRW-DOGE')
threads = []

for ticker in tickers_list:
    t = threading.Thread(target=data, args=(ticker,)) # 스레드 생성
    t.start()
    time.sleep(0.2)
'''
for t in threads:
    t.start()  # 스레드 실행

'''
for t in threads:
    t.join()  # 스레드 종료

print("end")

# true : 8
# false : 12