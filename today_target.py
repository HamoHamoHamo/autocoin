import pyupbit
import os
from day_candle import get_top_price

total_percent = 0
result_ticker = []
result_target = []


#get_list = get_top_price(True)
#tickers_list = get_list[1]

tickers_list = ('KRW-BTC', 'KRW-ETH', 'KRW-NEO', 'KRW-MTL', 'KRW-LTC', 'KRW-XRP', 'KRW-ETC', 'KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM', 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR', 'KRW-KMD', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-REP', 'KRW-EMC2', 'KRW-ADA', 'KRW-SBD', 'KRW-POWR', 'KRW-BTG', 'KRW-ICX', 'KRW-EOS', 'KRW-TRX', 'KRW-SC', 'KRW-IGNIS', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', 'KRW-ZRX', 'KRW-SRN', 'KRW-LOOM', 'KRW-BCH', 'KRW-ADX', 'KRW-BAT', 'KRW-IOST', 'KRW-DMT', 'KRW-RFR', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-MFT', 'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC', 'KRW-BSV', 'KRW-THETA', 'KRW-EDR', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC', 'KRW-ENJ', 'KRW-TFUEL', 'KRW-MANA', 'KRW-ANKR', 'KRW-NPXS', 'KRW-AERGO', 'KRW-ATOM', 'KRW-TT', 'KRW-CRE', 'KRW-SOLVE', 'KRW-MBL', 'KRW-TSHP', 'KRW-WAXP', 'KRW-HBAR', 'KRW-MED', 'KRW-MLK', 'KRW-STPT', 'KRW-ORBS', 'KRW-VET', 'KRW-CHZ', 'KRW-PXL', 'KRW-STMX', 'KRW-DKA', 'KRW-HIVE', 'KRW-KAVA', 'KRW-AHT', 'KRW-SPND', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA', 'KRW-JST', 'KRW-CRO', 'KRW-TON', 'KRW-SXP', 'KRW-LAMB', 'KRW-HUNT', 'KRW-MARO', 'KRW-PLA', 'KRW-DOT', 'KRW-SRM', 'KRW-MVL', 'KRW-PCI', 'KRW-STRAX', 'KRW-AQT', 'KRW-BCHA', 'KRW-GLM', 'KRW-QTCON', 'KRW-SSX', 'KRW-META', 'KRW-OBSR', 'KRW-FCT2', 'KRW-LBC', 'KRW-CBK', 'KRW-SAND', 'KRW-HUM', 'KRW-DOGE')
#tickers_list = ('KRW-ORBS', 'KRW-CHZ', 'KRW-DKA', 'KRW-MVL', 'KRW-XRP')

for ticker in tickers_list:
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    
    df['range'] = (df['high'] - df['low']) * 0.5
    df['target'] = df['open'] + df['range'].shift(1)

    income = [None for i in range(len(df.values))]
    max=0
    mdd_percent = [None for i in range(len(df.values))]
    for data in range(len(df.values)):
        if df['high'][data] >= df['target'][data] > df['low'][data]:
            if data == len(df.values)-1:
                income[data]='End'
            else:
                if df['high'][data] > max:
                    max=df['high'][data]
                mdd = (max-df['open'][data]) / max * 100
                mdd_percent[data] = mdd
                percent = (df['open'][data+1] - df['target'][data]) / df['target'][data] * 100
                total_percent += percent
                income[data] = percent
        else:
            income[data]="False"

    #df['mdd'] = mdd_percent
    df['수익'] = income
    print(df['target'][1])
    #print(df['mdd'])
    print(total_percent)

    result_ticker.append(ticker)
    result_target.append(df['target'][1])

result = {
    '종목' : result_ticker,
    '매수가격' : result_target,
}

print(result['종목'][0])

'''
    base_dir = 'C:/Users/Shin/autocoin/2021.03.16_data'
    file_name = ticker + '.xlsx'
    xlxs_dir = os.path.join(base_dir, file_name) 
    df.to_excel(xlxs_dir)
'''