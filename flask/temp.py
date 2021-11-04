import pandas as pd
# df_test = pd.read_csv('../datasets/Nifty_50_Test.csv',
#                       index_col="Date", parse_dates=True)
# real_stock_price = df_test.iloc[:, 1:2].values

# df = pd.DataFrame(real_stock_price, columns=['Open'])
# df = df['Open'].tolist()
# print(df)

file_read1 = pd.read_csv('../datasets/NIFTY_50_Train.csv',
                         index_col='Date', parse_dates=True)

file_read2 = pd.read_csv('../datasets/Nifty_50_Test.csv',
                         index_col="Date", parse_dates=True)

df = None
df_test = None

if len(file_read1.index) > len(file_read2.index):
    df = file_read1
    df_test = file_read2

else:
    df = file_read2
    df_test = file_read1

df_test['Date'] = df_test.index

print(df_test)
