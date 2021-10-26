@app.route('/stocker', methods=['POST'])
def nps():

    n = request.form['train']
    n_test = request.form['test']

    df = pd.read_csv(n, index_col='Date', parse_dates=True)

    df.dropna(inplace=True)

    df.rolling(7).mean()

    df.rolling(window=30).mean()['Close']

    df['Close: 30 day mean'] = df['Close'].rolling(window=30).mean()

    df['Close'].expanding(min_periods=1).mean()

    training_set = df['Open']
    training_set = pd.DataFrame(training_set)

    df.dropna(inplace=True)

    sc = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = sc.fit_transform(training_set)

    X_train = []
    Y_train = []

    for i in range(60, 1258):
        X_train.append(training_set_scaled[i-60:i, 0])
        Y_train.append(training_set_scaled[i, 0])

    X_train, Y_train = np.array(X_train), np.array(Y_train)

    # Reshaping
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    regressor = Sequential()

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

    regressor.compile(optimizer='adam', loss='mean_squared_error')

    regressor.fit(X_train, Y_train, epochs=100, batch_size=32)

    df_test = pd.read_csv(n_test, index_col="Date", parse_dates=True)

    real_stock_price = df_test.iloc[:, 1:2].values

    test_set = df_test['Open']
    test_set = pd.DataFrame(test_set)

    df_total = pd.concat((df['Open'], df_test['Open']), axis=0)

    inputs = df_total[len(df_total) - len(df_test) - 60:].values
    inputs = inputs.reshape(-1, 1)
    inputs = sc.transform(inputs)

    X_test = []

    for i in range(60, 356):
        X_test.append(inputs[i-60:i, 0])

    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    predicted_stock_price = regressor.predict(X_test)
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)

    predicted_stock_price = pd.DataFrame(predicted_stock_price)

    return {
        'message': 'Done!',
        'data': predicted_stock_price
    }
