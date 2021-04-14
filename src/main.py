from indicator import *
from dataset_tools.pandas_reader import load_OHLCV
import numpy as np
import os
import pandas as pd
from datetime import datetime
import time
import os.path
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from mplfinance.original_flavor import candlestick_ohlc
DIR_CSV = 'stock_data'


def load_OHLC_from_csv(symbol, dates,
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


def calculate_beta():
    # Extract input values from ui
    symbol = symbol_entry.get()
    start_date = start_date_calendar.get_date()
    end_date = end_date_calendar.get_date()
    print(symbol, start_date, end_date)
    dates = pd.date_range(start_date, end_date)

    # Download latest stock data
    df = load_OHLCV(symbol, start_date, end_date)
    df.drop(['Volume', 'Adj Close'], axis='columns', inplace=True)

    # Load set index data
    set_df = load_OHLC_from_csv("set_index", dates, dayfirst=False)

    print(df.tail())
    print("+++++EMA+++++")
    ema15 = ema(df, 15)
    print(ema15.tail())
    ema45 = ema(df, 45)
    ema100 = ema(df, 100)
    print("+++++Beta+++++")
    beta = getBeta(df, set_df)
    beta_label.config(text=str(beta))
    print(beta)
    values = [df, ema15, ema45, ema100]
    window.update()
    plot_graph(values)


if __name__ == '__main__':
    # Create simple ui to get symbol input
    window = tk.Tk()
    window.title('Beta Calculator')
    window.configure(background="white")

    style = ttk.Style(window)
    # change theme, you can use style.theme_names() to list themes
    style.theme_use('clam')

    tk.Label(window, text="Symbol").grid(row=0)
    tk.Label(window, text="Start Date").grid(row=1)
    tk.Label(window, text="End Date").grid(row=2)
    tk.Label(window, text="Beta").grid(row=3)
    beta_label = tk.Label(window, text="", borderwidth=2)
    beta_label.grid(row=3, column=1)

    start_date_calendar = Calendar(
        window, selecetmode="day", year=2021, month=4)
    end_date_calendar = Calendar(window, selecetmode="day", year=2021, month=4)
    symbol_entry = tk.Entry(window, borderwidth=2)

    symbol_entry.grid(row=0, column=1, pady=10)
    start_date_calendar.grid(row=1, column=1, pady=10)
    end_date_calendar.grid(row=2, column=1, pady=10)

    symbol_entry.focus_set()

    button = tk.Button(window, text='Submit',
                       command=calculate_beta)
    button.grid(row=4, column=1)
    window.mainloop()
