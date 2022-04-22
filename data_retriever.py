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
        directory = temp + '/stock_data/daily_stock_data_4_april/'
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

def removeDumplicates(file):
    df = pd.read_csv(file)
    df.drop_duplicates()
    df.to_csv(file, index=False)

def sortData(directory):
    for filename in os.listdir(directory):
        # get the current file
        f = os.path.join(directory, filename)
        print("fileName: ", filename)
        # read the data in the current file
        data = pd.read_csv(f)
        print(filename + " data: ", data)
        # remove the adjusted close column
        # keep_col = ['Date','Open','High','Low','Close','Volume']
        # data = f[keep_col]
        if data.__contains__('Adj Close'):
            data.drop('Adj Close', inplace=True, axis=1)
        if data.__contains__('Dividends'):
            data.drop('Dividends', inplace=True, axis=1)
        if data.__contains__('Stock Splits'):
            data.drop('Stock Splits', inplace=True, axis=1)
        ## need to figure out how to get balnk entries out of the data
        if ',,,,' in data:
            print("FOUND ONE")
            # df_s1 = data[:5]
            # df_s1 = df_s1.drop(df_s1.query('Open==,').index)
        # display data to verify it worked properly
        print("\nCSV Data after deleting the column 'Adj Close':\n")
        print(data)

        # sort data by date
        data['Date'] = pd.to_datetime(data.Date, infer_datetime_format=True)
        # pd.display(data.head())

        data.sort_values(by='Date', ascending=False, inplace=True)
        # pd.display(data.head())

        data.to_csv(f, index=False)