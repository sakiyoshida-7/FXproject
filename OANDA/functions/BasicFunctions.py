# OANDA
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments

#グラフ
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from matplotlib.finance import candlestick2_ohlc as plt_candle
import time

def get_data(api_key, instrument, params):
    api = API(access_token=api_key, environment="practice")
    r = instruments.InstrumentsCandles(instrument=instrument, params=params)
    api.request(r)
    data = []
    for raw in r.response['candles']:
        data.append([raw['time'], raw['volume'], raw['mid']['o'], raw['mid']['h'], raw['mid']['l'], raw['mid']['c']])
    # リストからデータフレームへ変換
    df = pd.DataFrame(data)
    for i in range(4):
        df[i+2] = df[i+2].astype('float')
    df.columns = ['time', 'volume', 'open', 'high', 'low', 'close']
    df = df.set_index('time')
    # date型を綺麗にする
    df.index = pd.to_datetime(df.index)
    return df

def get_csvdata(instrument, params, api_key):
    api          = API(access_token = api_key, environment="practice")
    request      = instruments.InstrumentsCandles(instrument = instrument,params = params)
    api.request(request)
    filename = "candle.csv"
    candle = pd.DataFrame.from_dict([ row['mid'] for row in request.response['candles'] ])
    candle['time'] = [ row['time'] for row in request.response['candles'] ]
    candle.to_csv(filename)
    return candle

def show_chart(candle):
    seaborn.set_style('darkgrid')
    # csvを読み込む
    candle = pd.read_csv('candle.csv')

    # 移動平均
    window_size  = [5,13,21] 
    sma5         = pd.Series.rolling(candle.c, window = window_size[0]).mean()
    sma13        = pd.Series.rolling(candle.c, window = window_size[1]).mean()
    sma21        = pd.Series.rolling(candle.c, window = window_size[2]).mean()

    # 移動平均と実際のローソク足を合わせる
    candle = candle[window_size[2]:].reset_index(drop = True)
    sma5 = sma5[ window_size[2]: ].reset_index(drop=True)
    sma13 = sma13[ window_size[2]: ].reset_index(drop=True)
    sma21 = sma21[ window_size[2]: ].reset_index(drop=True)

    # X軸の見た目を整える
    # 時間だけを切り出すために先頭からの12文字目から取るようにしている
    xticks_number = 15 #15分刻みに目盛りを書く
    xticks_index = range(0,len(candle), xticks_number)
    xticks_date = [candle.time.values[i][11:16] for i in xticks_index]

    plt.figure(figsize=(25,10), dpi=50)
    figure, ax = plt.subplots(figsize=(25,10))
    plt_candle( ax,
                opens = candle.o.values,
                highs = candle.h.values,
                lows = candle.l.values,
                closes = candle.c.values,
                width=0.6,
                colorup='#DC143C',
                colordown='white')
    plt.plot(sma5, color='red')
    plt.plot(sma13, color='yellow')
    plt.plot(sma21, color='blue')
    plt.xticks(xticks_index, xticks_date, rotation=80)
    plt.show()
