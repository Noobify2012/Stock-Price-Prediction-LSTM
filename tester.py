import data_retriever
import os

# ticker = 'AAPL'
# start = '2017-4-4'
# end = '2022-4-4'
# interval = '1w'
# data_retriever.getDataset(start,end,interval,ticker)

temp = os.path.dirname(__file__)
print("Value of temp: ", temp)

# assign directory
directory = temp + '/stock_data/daily_stock_data_4_april'
print("Directory: ", directory)

data_retriever.sortData(directory)

# iterate over files in
# that directory
# for filename in os.listdir(directory):
#     ticker = filename.strip('.csv')
#     with open('ticker_list.csv', 'a') as fd:
#         fd.write(ticker + ',\n')
#     print(ticker)