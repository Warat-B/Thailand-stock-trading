import urllib
import urllib.request
import ssl
import os
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from os.path import join, exists
from os import remove, makedirs

# Example url
# https://www.set.or.th/set/historicaltrading.do?symbol=BBL&page=2&language=en&country=US&type=trading

# Init variable
context = ssl._create_unverified_context()
OUTPUT_DIR = "stock_data"


def getTableData(symbol, page=1):
    if page > 3:
        page = 3  # limit at 3
    url_string = "https://www.set.or.th/set/historicaltrading.do?symbol={0}".format(
        symbol)
    url_string += '&page={0}&language=en&country=US&type=trading'.format(
        page-1)

    page = urllib.request.urlopen(url_string, context=context).read()
    soup = BeautifulSoup(page, 'lxml')
    table_element = soup.find('table', class_='table table-hover table-info')
    return table_element, url_string


def createDataFrame(table_element):
    row_list = []
    head_list = []

    if table_element is None:
        return None

    tr_list = table_element.findAll('tr')

    for tr in tr_list:
        th_list = tr.findAll('th')
        if th_list is not None:
            for th in th_list:
                head_list.append(th.find(text=True))

        td_list = tr.findAll('td')

        for td in td_list:
            row_list = np.append(row_list, td.find(text=True))

    num_col = len(head_list)
    total_col = int(len(row_list)/num_col)
    row_list = np.reshape(row_list, (total_col, num_col))
    df = pd.DataFrame(columns=head_list, data=row_list)
    return df


def create_all_data(symbol, total_page=1):
    # get stock data from set.or.th web (total page)
    df = None
    for p in range(1, total_page+1):
        table_element, url_string = getTableData(symbol, page=p)
        # print(url_string)
        df_temp = createDataFrame(table_element)
        if df is None:
            df = df_temp
        else:
            df = df.append(df_temp)
    return df


def writeCSVFile(df, symbol, output_path=OUTPUT_DIR, include_index=False):
    csv_file = "{}.csv".format(join(output_path, symbol))
    df.to_csv(csv_file, index=include_index)


def removeOldFile(symbol, output_path=OUTPUT_DIR):
    csv_file = "{}.csv".format(join(output_path, symbol))
    if exists(output_path) == False:
        makedirs(output_path)
    if exists(csv_file):
        remove(csv_file)


if __name__ == "__main__":
    # Get tabel data
    # table_element, url_string = getTableData("PTT")
    # tr_list = table_element.findAll('tr')
    # print(tr_list[0:2])

    symbol_list = ['PTT']
    for symbol in symbol_list:
        # 1 total_page equal to 29 active days/page not include weekend
        df = create_all_data(symbol, total_page=4)
        print('\n********* %s **********' % symbol)
        print(df.tail())

        # save csv files (all stock data)
        removeOldFile(symbol)  # clear old files
        writeCSVFile(df, symbol)
