# import required module
import os, csv
import pandas as pd
import data_retriever

#get path of current directory
temp = os.path.dirname(__file__)
print("Value of temp: ", temp)

#set tickerfile to the path plus the file extension
tickerfile = temp + '/ticker_list.csv'
print("ticker file path: ", tickerfile)
#initialize ticker set
tickerSet = []
with open(tickerfile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            print("Row value: ", row[1])
            tickerSet.append(row[1])
            line_count += 1
    print(f'Processed {line_count} lines.')
print(tickerSet)
# tickerset = pd.read_csv(tickerfile, usecols=[0,1])
#get the weekly interval data
for ticker in tickerSet:
    if ticker != 'Ticker' or ticker != 'Index':
        print('current ticker: ', ticker)
        #ticker = 'AAPL'
        start = '2017-4-4'
        end = '2022-4-4'
        interval = '1wk'
        #get ticker data
        data_retriever.getDataset(start,end,interval,ticker)

#get the daily interval data
# for ticker in tickerSet:
#     if ticker != 'Ticker' or ticker != 'Index':
#         print('current ticker: ', ticker)
#         #ticker = 'AAPL'
#         start = '2017-4-4'
#         end = '2022-4-4'
#         interval = '1d'
#         #get ticker data
#         data_retriever.getDataset(start,end,interval,ticker)




# assign directory
directory = temp + '/stock_data/weekly_stock_data_4_april'
print("Directory: ", directory)

# iterate over files in
# that directory
for filename in os.listdir(directory):
    #get the current file
    f = os.path.join(directory, filename)
    print("fileName: ", filename)
    #read the data in the current file
    data = pd.read_csv(f)
    print(filename+ " data: ", data)
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

    #sort data by date
    data['Date'] = pd.to_datetime(data.Date, infer_datetime_format=True)
    #pd.display(data.head())

    data.sort_values(by='Date', ascending=False, inplace=True)
    #pd.display(data.head())

    data.to_csv(f, index=False)
