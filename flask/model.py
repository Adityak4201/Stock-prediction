import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

# """## Task 1: Raw Data (Google Stock Prices from 2012 to 2017)"""


def stockModel(file, file2):

    file_read1 = pd.read_csv(file, index_col='Date', parse_dates=True)

    file_read2 = pd.read_csv(file2, index_col="Date", parse_dates=True)

    df = None
    df_test = None

    if len(file_read1.index) > len(file_read2.index):
        df = file_read1
        df_test = file_read2

    else:
        df = file_read2
        df_test = file_read1

    df.head()

    df.isna().any()

    df.dropna(inplace=True)

    df.info()
    df["Open"] = df["Open"].astype(float)
    df["Close"] = df["Close"].astype(float)
    df["High"] = df["High"].astype(float)
    df["Low"] = df["Low"].astype(float)
    df["Volume"] = df["Volume"].astype(float)

    df['Open'].plot(figsize=(16, 6))

    # 7 day rolling mean
    df.rolling(7).mean().head(20)

    df['Open'].plot(figsize=(16, 6))
    df.rolling(window=30).mean()['Close'].plot()

    df['Close: 30 day mean'] = df['Close'].rolling(window=30).mean()
    df[['Close', 'Close: 30 day mean']].plot(figsize=(16, 6))

    df['Close'].expanding(min_periods=1).mean().plot(figsize=(16, 6))

    training_set = df['Open']
    training_set = pd.DataFrame(training_set)

    # """## Task 2: Data Preprocessing"""

    df.isna().any()

    # Feature Scaling
    sc = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = sc.fit_transform(training_set)

    # Creating a data structure with 60 timesteps and 1 output
    X_train = []
    Y_train = []

    for i in range(60, len(df.index)):
        X_train.append(training_set_scaled[i-60:i, 0])
        Y_train.append(training_set_scaled[i, 0])

    X_train, Y_train = np.array(X_train), np.array(Y_train)

    # Reshaping
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    # """## Task 3: Feature Extraction"""

    # Initializing RNN
    regressor = Sequential()

    # """## Task 4: Training the Neural Network"""

    regressor.add(LSTM(units=50, return_sequences=True,
                  input_shape=(X_train.shape[1], 1)))
    regressor.add(Dropout(0.2))

    regressor.add(LSTM(units=50, return_sequences=True))
    regressor.add(Dropout(0.2))

    regressor.add(LSTM(units=50, return_sequences=True))
    regressor.add(Dropout(0.2))

    regressor.add(LSTM(units=50))
    regressor.add(Dropout(0.2))

    regressor.add(Dense(units=1))

    # """## Task 5: Output Generation"""

    regressor.compile(optimizer='adam', loss='mean_squared_error')

    regressor.fit(X_train, Y_train, epochs=100, batch_size=32)

    # """## Task 6: Visualization """

    real_stock_price = df_test.iloc[:, 1:2].values
    type(real_stock_price)

    df_test.head()

    df_test.info()

    df_test["Open"] = df_test["Open"].astype(float)
    df_test["Close"] = df_test["Close"].astype(float)
    df_test["High"] = df_test["High"].astype(float)
    df_test["Low"] = df_test["Low"].astype(float)
    df_test["Volume"] = df_test["Volume"].astype(float)

    df_test.dropna(inplace=True)

    test_set = df_test['Open']
    df_test['Date'] = df_test.index
    test_set = pd.DataFrame(test_set)

    test_set.info()

    df_total = pd.concat((df['Open'], df_test['Open']), axis=0)
    inputs = df_total[len(df_total) - len(df_test) - 60:].values
    inputs = inputs.reshape(-1, 1)
    inputs = sc.transform(inputs)
    X_test = []
    for i in range(60, len(test_set)):
        X_test.append(inputs[i-60:i, 0])

    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predicted_stock_price = regressor.predict(X_test)
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)

    predicted_stock_price = pd.DataFrame(predicted_stock_price)
    real_stock_price = pd.DataFrame(real_stock_price, columns=['Open'])
    print(predicted_stock_price)
    print(real_stock_price)
    predicted_stock_price = predicted_stock_price[0].tolist()
    real_stock_price = real_stock_price['Open'].tolist()

    d = {'real': None, 'predicted': None, 'date': None}
    d['real'] = real_stock_price
    d['predicted'] = predicted_stock_price
    d['date'] = df_test['Date'].tolist()

    return d

    # predicted_stock_price.info()

    # plt.plot(real_stock_price, color="red", label="Real Google Stock Price")
    # plt.plot(predicted_stock_price, color="blue",
    #          label="Predicted Google Stock Price")
    # plt.title('Stock Price Prediction')
    # plt.xlabel('Time')
    # plt.ylabel('Google Stock Price')
    # plt.legend()
    # plt.show()
