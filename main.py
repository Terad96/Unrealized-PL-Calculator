import yfinance as yf
import pandas as pd
import csv
import matplotlib.pyplot as plt
from datetime import date

today = date.today()
stock = list()
stockcount = list()
stockcost = list()
buydate = list()
fdata = list()
PL = list()

# get stock buy date and cost
print("*** Loading list of stocks ***")
with open('list.csv', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        line = csv_reader.line_num
        stock.append(row[0])
        stockcount.append(row[1])
        stockcost.append(row[2])
        buydate.append(row[3])

# Get stock data
print("*** Loading stock historical data ***")
for x in range(len(stock)):
    ticker = yf.Ticker(stock[x])
    df_list = list()
    data = ticker.history(start=buydate[x], end=today)
    df_list.append(data)
    fdata.append(data)
    # combine all dataframes into a single dataframe
    df = pd.concat(df_list)
    # dataframe clean up
    df = df.drop(columns= ["Open", "High", "Low","Volume", "Dividends", "Stock Splits"], errors='ignore')
    df["Cost"] = stockcost[x]
    df["Ticker symbol"] = stock[x]
    # convert series in dataframe to int
    df['Close'] = df['Close'].astype(float)
    df['Cost'] = df['Cost'].astype(float)
    # calculate PL
    df["PL"] = (df["Close"]*float(stockcount[x])) - df["Cost"]
    # print(df)
    # save to csv
    if x == 0:
        df2 = df.copy()
        length = len(df)
    else:
        df2 = df2.append(df)
    # df.to_csv( str(x) + 'ticker.csv')


# convert date index into column
df2 = df2.reset_index()
# calculate cumulative PL
print("*** Calculating historical PL *** ")
# for each of these dates, add up the PL
for x in range(0, length):
    for i in range (length, len(df2)):
        if df2.iat[x,0] == df2.iat[i,0]:
            df2.iat[x,4] = df2.iat[x,4] + df2.iat[i,4]
# clean up data frame
df2 = df2.drop(df2.index[length:len(df2)])
df2 = df2.drop(columns= ["Close", "Cost", "Ticker symbol"])
# save changes
print("*** Saving results to 'PL Results.csv' ***")
df2.to_csv('PL Results.csv')
# plot PL data
print("*** Plotting PL chart ***")
df2.plot(x ='Date', y='PL', kind = 'line')
plt.show()


