import yfinance as yf
import os
import pandas as pd

# FUNCTION TO GET THE STOCK DATA FROM YAHOO
def getDataset(startDate, endDate, interval, ticker):
    #define the ticker symbol
    tickerSymbol = ticker

    #get data on this ticker
    tickerData = yf.Ticker(tickerSymbol)

    #get the historical prices for this ticker
    tickerDf = tickerData.history(interval=interval, start=startDate, end=endDate)

    print('ticker interval: ', interval)

    keep_col = ['Date','Open','High','Low','Close','Volume']

    #see your data
    print('Value of Ticker DF: ')
    print(tickerDf)
    #period: the frequency at which to gather the data; common options would include ‘1d’ (daily), ‘1mo’ (monthly), ‘1y’ (yearly)

    temp = os.path.dirname(__file__)
    print("Value of temp: ", temp)


    #drop into 1d folder for data
    if interval == '1d':
        # assign directory
        directory = temp + '/stock_data/daily_stock_data_5_april/'
        print("Directory: ", directory)
        f = directory + ticker + '.csv'
        tickerDf.to_csv(f, index=True)
    #drop into 5d folder for data
    elif interval == '1wk':
        # assign directory
        directory = temp + '/stock_data/weekly_stock_data_4_april/'
        print("Directory: ", directory)
        f = directory + '/' + ticker + '.csv'
        tickerDf.to_csv(f, index=True)
    #drop into other folder
    else:
        pass