import pandas as pd


# 读取Excel文件
df = pd.read_excel('parameters_and_prices_with_bool.xlsx', sheet_name='Sheet1')


now_price_index = 26
# 显示读取的数据
print(df)
print(df.iloc[now_price_index, 0])
print(df.iloc[now_price_index, 1])
