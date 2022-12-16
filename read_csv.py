import pandas as pd

df = pd.read_csv('data/modis_2021_United_States.csv', sep=',')

df = df.sort_values(by=['brightness'], ascending=False)


print(df.values)

print(df)

print(df.values[0])