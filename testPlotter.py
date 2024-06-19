import yfinance as yf
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from datetime import datetime
todays_date = datetime.today().strftime('%Y-%m-%d')

# tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'NVDA' ]
temp = os.path.dirname(__file__)
# print("Value of temp: ", temp)

#set tickerfile to the path plus the file extension
data = None
tickerfile = (temp + 
# '/ticker_list.csv')
'/top_500_stocks - Sheet1.csv')

def getTickerData(tickers: dict) -> dict:
    data = None
    try:
        data = {ticker: yf.download(ticker, period='2y') for ticker in tickers}
    except:
        pass
    return data

def plotCrossingTickers(tickerLis: dict):
    print("Tickers to be printed: %s" % tickerLis)
    data = getTickerData(tickerLis)
    for (ticker, df) in data.items():
        df['50_MA'] = df['Close'].rolling(window=50).mean()
        df['200_MA'] = df['Close'].rolling(window=200).mean()
        plt.figure(num=ticker)

        plt.plot(df['Close'], 'k')
        plt.plot(df['50_MA'], 'r')
        plt.plot(df['200_MA'], 'b')
        plt.tight_layout()
        plt.title(ticker)
        plt.legend(["Close", "50_MA", "200_MA"])
        plt.savefig("%s.png" % ticker)
        plt.show()
    # fig, axes = plt.subplots(nrows=len(tickerLis), ncols=1, figsize=(10, 15), sharex=True)
    # print("fig: %s, axes: %s" % (fig, axes))

    # print(data)


    # # for ax, (ticker, df) in zip(axes, data.items()):
    # for ax, (tickerLis, df) in zip(axes, data.items()):
    #     print("Ticker List: %s" % tickerLis)
    #     # print("data items: %s" % data.items())
    #     # df['50_MA'] = df['Close'].rolling(window=50).mean()
    #     # df['200_MA'] = df['Close'].rolling(window=200).mean()
    #     # if abs(df['50_MA'].iloc[df.shape[0]-1] - df['200_MA'].iloc[df.shape[0]-1]) <= 20 :
    #     df['Close'].plot(ax=ax, label='Closing Price', color='black')
    #     df['50_MA'].plot(ax=ax, label='50-Day MA', color='blue')
    #     df['200_MA'].plot(ax=ax, label='200-Day MA', color='red')
    #     # print("AX: %s, ticker: %s, df: %s, df.shape: %s" % (ax, ticker, df, df.shape[0]-1))
    #     # print("df 50: %s, df200: %s" % (df['50_MA'].iloc[df.shape[0]-1], df['200_MA'].iloc[df.shape[0]-1]))
    #     ax.set_title(tickerLis)
    #     ax.legend()

    # plt.tight_layout()
    # plt.savefig("simplefinance.png", dpi=200)
    # plt.show()


with open(tickerfile, 'r') as tickers:
    # print("How many tickers do we have: %s " % len(tickers.readlines()))
    # for ticker in tickers:
    #     print("current ticker: %s" % ticker)
    data = getTickerData(tickers)
    # data = {ticker: yf.download(ticker, period='2y') for ticker in tickers}
    



# data = {ticker: yf.download(ticker, period='2y') for ticker in tickers}

    tickerLis = []
    for (ticker, df) in data.items():
        df['50_MA'] = df['Close'].rolling(window=50).mean()
        df['200_MA'] = df['Close'].rolling(window=200).mean()
        df['20_MA'] = df['Close'].rolling(window=20).mean()
        try:
            # print("DF 200 iloc[-1]: %s" % float(df['200_MA'].iloc[-1]))
            # print("DF 50 iloc[-1]: %s" % float(df['50_MA'].iloc[-1]))
            # print("DF 200 iloc[-1] - DF 50: %s" % (float(df['200_MA'].iloc[-1]) - float(df['50_MA'].iloc[-1])))
            
            cross_val = int(float(df['200_MA'].iloc[-1]) - float(df['50_MA'].iloc[-1]))
            trend_val = int(float(df['50_MA'].iloc[-1]) - float(df['20_MA'].iloc[-1]))
            print("Ticker: %s, Cross Val: %s, trend_val: %s" % (ticker, cross_val, trend_val))

            
            # print("ticker: %s, cross_val: %s" % (ticker, cross_val))
            cross_bool = cross_val>0
            # print("cross_val: %s, cross_bool: %s" % (cross_val, cross_bool))
            # df['200_MA'].iloc[df.shape[0]-1] - df['50_MA'].iloc[df.shape[0]-1]
            # if cross_bool:
            if cross_val > 0 and trend_val < 0:
            # and df['50_MA'].iloc[df.shape[0]-1] < df['200_MA'].iloc[df.shape[0]-1]:
                # print("%s is near a cross!!!!!" % ticker)
                tickerLis.append(ticker.strip())
        except:
            pass
            # print("Need to debug: %s" % ticker)
    plotCrossingTickers(tickerLis)


# getTickerData(tickers)
# print("the length of tickerList: %s " % len(tickerList))

# fig, axes = plt.subplots(nrows=len(tickers), ncols=1, figsize=(10, 15), sharex=True)

# ############
# # get tickers

# # get ticker data
# tickerData = getTickerData

