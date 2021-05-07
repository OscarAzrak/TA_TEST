import talib as ta
import pandas_datareader as web

import pandas as pd
import numpy as np
import yfinance as yf
import pandas_datareader as pdr
import datetime as dt
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

import trendln
pd.options.display.max_columns = None
pd.options.display.max_rows = None

##Get stock price data
ticker = 'ticker'

# Data time period
now = dt.datetime.now()
startyear = 2020
startmonth = 1
startday = 1
start = dt.datetime(startyear, startmonth, startday)

# get data from YFinance
#df = web.DataReader(ticker, 'yahoo', start, now)
df = pdr.get_data_yahoo(ticker, start, now)

# get the RSI
df['RSI'] = ta.RSI(df['Adj Close'],14)
price_list = list(df['Adj Close'])

# create buy and sells signals columns
df['Buy Signal'] = np.nan
df['Sell Signal'] = np.nan

#MACD #MACD SIGNAL is the 'SMOOTH'
df['MACD'], df['MACD_SIGNAL'], df['MACD_HIST'] = ta.MACD(df['Adj Close'], 8, 21, 5)

#STOCHASTIC SLOW
# overbought if the value is above 80
# oversold if the value is below 20
df['slowk'], df['slowd'] = ta.STOCH(df['High'], df['Low'], df['Adj Close'], fastk_period=14, slowk_period=3, slowk_matype=3, slowd_period=3, slowd_matype=0)



# finding buy/sell signals and short/long signals
for x in range(15, len(df)):

    # if RSI is below 50, and stoch is above 80 and MACD crosses down, short
    #OM RSI ÄR UNDER 50, OCH STOCH ÄR ÖVER 80 OCH MACD CROSSING DOWN, SHORTA
    try:
        if round(float(df['MACD'][x]), 2) <= round(df['MACD_SIGNAL'][x], 2)\
                and round(df['MACD'][x + 1], 2) >= round(df['MACD_SIGNAL'][x + 1], 2):
            if df['RSI'][x] <= 50:
                if df['slowk'][x] and df['slowd'][x] >= 80:
                    #print('Short at ', df['Adj Close'][x])
                    print('Short at ', df['Adj Close'][x])
        #Exit when RSI and stochastic are oversold, RSI above 50 at the same time as stoch is below 20
        if df['RSI'][x] >= 50:
            if df['slowk'][x] and df['slowd'][x] <= 20:
                print('Stop shorting at',df['Adj Close'][x],df.index[x])
        #get in to buy position when MACD crosses up, RSI is below 50 and STOCH is below 20
        if round(float(df['MACD'][x]), 2) >= round(df['MACD_SIGNAL'][x], 2) \
                and round(df['MACD'][x + 1], 2) <= round(df['MACD_SIGNAL'][x + 1], 2):
            if df['RSI'][x] <= 50:
                if df['slowk'][x] and df['slowd'][x] <= 20:
                    print('Buy or Long at ',df['Adj Close'][x], df.index[x])
        if df['RSI'][x] >= 70:
            if df['slowk'][x] and df['slowd'][x] >= 80:
                print('Stop longing or sell at', df['Adj Close'][x],df.index[x])
    except ValueError and IndexError:
        pass

plt.style.use('classic')
fig, axs = plt.subplots(4, sharex=True, figsize=(13, 9))
fig.suptitle('Stock Price (top) &  RSI (bottom)')

axs[0].scatter(df.index, df['Buy Signal'], color='green', marker='^', alpha=1)
axs[0].scatter(df.index, df['Sell Signal'], color='red', marker='v', alpha=1)
axs[0].plot(df['Adj Close'], alpha=0.8)
axs[0].grid()

axs[1].plot(df['RSI'], alpha=0.8)
axs[1].grid()
#axs[1].axhline(y=70, color='g', linestyle='-') #   some uses two lines, one with 70, one with 30
#axs[1].axhline(y=30, color='g', linestyle='-')
axs[1].axhline(y=50, color='g', linestyle='-') #   others use one line at 50

axs[2].plot(df['slowk'], alpha=0.6)
axs[2].plot(df['slowd'], alpha=0.5)
axs[2].axhline(y=80, color='g', linestyle='-')
axs[2].axhline(y=20, color='g', linestyle='-')
axs[2].grid()

axs[3].plot(df['MACD'], alpha=0.6)
axs[3].plot(df['MACD_SIGNAL'], alpha=0.5)
axs[3].grid()
plt.show()

# IF RSI IS BELOW 50 AND STOCH ABOVE 80 ::: SHORT
#
# STOP SHORT WHEN RSI IS BELOW 50 AND STOCH BELOW 20
# IF RSI IS ABOVE 50 AND STOCH BELOW 20 AND IF MACD CROSSES UP BUY/LONG
#
# STOP LONG/ WHEN RSI IS ABOVE 50 AND STOCH IS ABOVE 20


