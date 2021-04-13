from indicator import ema, get_rate_of_change, getBeta
import numpy as np
import os
import pandas as pd
from datetime import datetime
import time
import os.path
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from mplfinance.original_flavor import candlestick_ohlc
DIR_CSV = 'stock_data'


def load_OHLC(symbol, dates,
              column_names=['Open', 'High', 'Low', 'Close'],
              base_dir=DIR_CSV, dayfirst=True):
    if 'Date' not in column_names:
        column_names = np.append(['Date'], column_names)

    csv_file = os.path.join(base_dir, "{}.csv".format(symbol))
    df_csv = pd.read_csv(csv_file, index_col='Date',
                         parse_dates=True, dayfirst=dayfirst, usecols=column_names,
                         na_values=['nan'])

    if dates is None:
        dates = df_csv.index
    df_main = pd.DataFrame(index=dates)
    df_main = df_main.join(df_csv)
    df_main = df_main.dropna(0)
    return df_main

# code from : http://matplotlib.org/examples/pylab_examples/finance_demo.


def plotCandlestick(symbol, dates, title="Selected data"):
    # quotes = loadStockQuotes(symbol, dates)

    mondays = WeekdayLocator(MONDAY)
    # alldays = DayLocator()
    # weekFormatter = DateFormatter('%b %d')
    # dayFormatter = DateFormatter('%d')

    # fig, ax = plt.subplots()
    # fig.subplots_adjust(bottom=0.2)
    # ax.xaxis.set_major_locator(mondays)
    # ax.xaxis.set_minor_locator(alldays)
    # ax.xaxis.set_major_formatter(weekFormatter)

    # candlestick_ohlc(ax, quotes, width=0.6)

    # ax.xaxis_date()
    # ax.autoscale_view()
    # ax.set_title(title)
    # plt.setp(plt.gca().get_xticklabels(),
    #          rotation=45, horizontalalignment='right')

    # plt.show()


def plot_graph(values):
    style = ['b-', 'r-', 'g-', 'k-', 'y-']
    column_list = values[0].columns
    num_stock = len(column_list)
    date = values[0].index

    if num_stock > 6:
        num_stock = 6
    for pos in range(0, num_stock):
        column = column_list[pos]
        plt.subplot(2, 3, pos+1)
        for i in range(0, len(values)):
            plt.plot(date, values[i][column], style[i])
            plt.title(column)
            plt.xticks([])

    plt.show()


if __name__ == '__main__':
    startDate = '2021-01-01'
    # datetime.now() will use your local time zone as refernce
    endDate = datetime.now().strftime("%Y-%m-%d")
    dates = pd.date_range(startDate, endDate)

    # Load data from csv file
    ptt_df = load_OHLC("DELTA", dates)
    set_df = load_OHLC("set_index", dates, dayfirst=False)

    print(ptt_df.tail())
    # ptt_df.drop(['Total Volume'], axis='columns', inplace=True)

    print("+++++EMA+++++")
    ema15 = ema(ptt_df, 15)
    print(ema15.tail())
    ema45 = ema(ptt_df, 45)
    ema100 = ema(ptt_df, 100)
    print("+++++Beta+++++")
    beta = getBeta(ptt_df, set_df)
    print(beta)
    values = [ptt_df, ema15, ema45, ema100]
    plot_graph(values)
