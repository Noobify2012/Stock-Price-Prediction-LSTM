# import required module
import os
import pandas as pd

temp = os.path.dirname(__file__)
print("Value of temp: ", temp)

# assign directory
directory = temp + '/stock_data/daily_stock_data_4_april'
print("Directory: ", directory)

# iterate over files in
# that directory
for filename in os.listdir(directory):
    #get the current file
    f = os.path.join(directory, filename)
    print("fileName: ", filename)
    #read the data in the current file
    data = pd.read_csv(f)
    # remove the adjusted close column
    #keep_col = ['Date','Open','High','Low','Close','Volume']
    #data = f[keep_col]
    if data.__contains__('Adj Close'):
        data.drop('Adj Close', inplace=True, axis=1)
    # display data to verify it worked properly
    print("\nCSV Data after deleting the column 'Adj Close':\n")
    print(data)
    data.to_csv(f, index=False)
