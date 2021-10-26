import pandas as pd
df_test = pd.read_csv('../datasets/Nifty_50_Test.csv',
                      index_col="Date", parse_dates=True)
real_stock_price = df_test.iloc[:, 1:2].values

df = pd.DataFrame(real_stock_price, columns=['Open'])
df = df['Open'].tolist()
print(df)
