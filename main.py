#use csv for tickers
#!/usr/bin/python3

# TODO Read tickers without index 




for subdir, dirs, files in os.walk(directory):
    for file in files:
        if file != '.DS_Store':
            print("subdir: ", subdir, " file: ", file)
            print("Path of files: ", os.path.join(subdir, file))
            stock = file
            fileName = os.path.join(subdir, file)
            ticker = stock.strip('.csv')
            # if ticker == "PFE" or ticker == "DAL" or ticker == "AAPL" or ticker == "JNJ":
            if 'weekly' in subdir:
                print("weekly")
                topLayer = [64]
                dateList = [3]
                for top in topLayer:
                    for date in dateList:
                        print ("Value of top: ", top)
                        print("ticker: ", ticker)
                        stockPrediction(fileName, top, date, ticker)
            else :
                print("daily")
                topLayer = [200]
                dateList = [3]
                for top in topLayer:
                    print ("Value of top: ", top)
                    print("ticker: ", ticker)
                    stockPrediction(fileName, top, date, ticker)