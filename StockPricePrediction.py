# IMPORTING IMPORTANT LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math, os
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
import preprocessing
import os
import tensorflow as tf

# FOR REPRODUCIBILITY
np.random.seed(7)

temp = os.path.dirname(__file__)
print("Value of temp: ", temp)

# assign directory
directory = temp + '/stock_data/'
print("Directory: ", directory)


rootdir = 'C:/Users/sid/Desktop/test'

for subdir, dirs, files in os.walk(directory):
    for file in files:
        if file != '.DS_Store':
            print("subdir: ", subdir, " file: ", file)
            print("Path of files: ", os.path.join(subdir, file))
            stock = file
            fileName = os.path.join(subdir, file)
            ticker = stock.strip('.csv')

            ###################
            # IMPORTING DATASET
            #dataset = pd.read_csv('apple_share_price.csv', usecols=[1,2,3,4])
            dataset = pd.read_csv(fileName, usecols=[1,2,3,4])
            dataset = dataset.reindex(index = dataset.index[::-1])

            # # CREATING OWN INDEX FOR FLEXIBILITY
            obs = np.arange(1, len(dataset) + 1, 1)
            #
            # TAKING DIFFERENT INDICATORS FOR PREDICTION
            OHLC_avg = dataset.mean(axis = 1)
            HLC_avg = dataset[['High', 'Low', 'Close']].mean(axis = 1)
            close_val = dataset[['Close']].mean(axis = 1)
            #
            # # PLOTTING ALL INDICATORS IN ONE PLOT
            plt.plot(obs, OHLC_avg, 'r', label = 'OHLC avg')
            plt.plot(obs, HLC_avg, 'b', label = 'HLC avg')
            plt.plot(obs, close_val, 'g', label = 'Closing price')
            plt.legend(loc = 'upper left')
            plt.savefig(temp + '/stock-data-charts/' + ticker + '.png')
            #plt.show()
            plt.close()
            #
            # PREPARATION OF TIME SERIES DATASET
            OHLC_avg = np.reshape(OHLC_avg.values, (len(OHLC_avg),1)) # 1664
            scaler = MinMaxScaler(feature_range=(0, 1))
            OHLC_avg = scaler.fit_transform(OHLC_avg)
            #
            # TRAIN-TEST SPLIT
            train_OHLC = int(len(OHLC_avg) * 0.75)
            test_OHLC = len(OHLC_avg) - train_OHLC
            train_OHLC, test_OHLC = OHLC_avg[0:train_OHLC,:], OHLC_avg[train_OHLC:len(OHLC_avg),:]
            #
            # # TIME-SERIES DATASET (FOR TIME T, VALUES FOR TIME T+1)
            trainX, trainY = preprocessing.new_dataset(train_OHLC, 1)
            testX, testY = preprocessing.new_dataset(test_OHLC, 1)
            #
            # # RESHAPING TRAIN AND TEST DATA
            trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
            testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
            step_size = 1
            #
            # # LSTM MODEL
            model = Sequential()
            model.add(LSTM(32, input_shape=(1, step_size), return_sequences = True))
            model.add(LSTM(16))
            model.add(Dense(1))
            model.add(Activation('linear'))
            #
            # # MODEL COMPILING AND TRAINING
            model.compile(loss='mean_squared_error', optimizer='adagrad') # Try SGD, adam, adagrad and compare!!!
            model.fit(trainX, trainY, epochs=5, batch_size=1, verbose=2)
            #
            # # PREDICTION
            trainPredict = model.predict(trainX)
            testPredict = model.predict(testX)
            #
            # # DE-NORMALIZING FOR PLOTTING
            trainPredict = scaler.inverse_transform(trainPredict)
            trainY = scaler.inverse_transform([trainY])
            testPredict = scaler.inverse_transform(testPredict)
            testY = scaler.inverse_transform([testY])
            #
            #
            # # TRAINING RMSE
            trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
            print('Train RMSE: %.2f' % (trainScore))
            #
            # # TEST RMSE
            testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
            print('Test RMSE: %.2f' % (testScore))
            #
            # # CREATING SIMILAR DATASET TO PLOT TRAINING PREDICTIONS
            trainPredictPlot = np.empty_like(OHLC_avg)
            trainPredictPlot[:, :] = np.nan
            trainPredictPlot[step_size:len(trainPredict)+step_size, :] = trainPredict
            #
            # # CREATING SIMILAR DATASSET TO PLOT TEST PREDICTIONS
            testPredictPlot = np.empty_like(OHLC_avg)
            testPredictPlot[:, :] = np.nan
            testPredictPlot[len(trainPredict)+(step_size*2)+1:len(OHLC_avg)-1, :] = testPredict
            #
            # # DE-NORMALIZING MAIN DATASET
            OHLC_avg = scaler.inverse_transform(OHLC_avg)
            #
            # # PREDICT FUTURE VALUES
            last_val = testPredict[-1]
            last_val_scaled = last_val / last_val
            next_val = model.predict(np.reshape(last_val_scaled, (1, 1, 1)))
            print("Last Day Value:", np.ndarray.item(last_val))
            print("Next Day Value:", np.ndarray.item(last_val * next_val))
            # need to substitue np.asscalar for this numpy.ndarray.item()
            # print np.append(last_val, next_val)

             # PLOT OF MAIN OHLC VALUES, TRAIN PREDICTIONS AND TEST PREDICTIONS
            plt.plot(OHLC_avg, 'g', label = 'original dataset')
            plt.plot(trainPredictPlot, 'r', label = 'training set')
            plt.plot(testPredictPlot, 'b', label = 'predicted stock price/test set')
            plt.legend(loc = 'upper left')
            plt.xlabel('Time in Days')
            plt.ylabel('OHLC Value of ' + ticker + ' Stocks')
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            plt.annotate("Last Day Value: "+ str(round(np.ndarray.item(last_val),2)) + "\nNext Day Value: " + str(round(np.ndarray.item(last_val*next_val),2)), xy=(0.05, 0.05), xycoords='axes fraction')
            #need to add value of next day prediction and data
            #need to add RMSE for next days
            plt.savefig(temp + '/stock-predict-charts/' + ticker + '.png')
            plt.close()
            #plt.show()
































































































