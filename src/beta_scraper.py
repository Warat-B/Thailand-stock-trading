import tkinter as tk
from tkinter import ttk
from dataset_tools.web_set_price import get_beta_from_set
import pandas as pd


def get_beta():
    beta_object = {}
    ytd_list = []
    last_year_list = []
    last_2_year_list = []
    # Extract input values from ui
    symbols = symbol_entry.get().replace(" ", '').upper().split(',')
    beta_object['Symbol'] = symbols
    for symbol in symbols:
        beta_value_buffer = get_beta_from_set(symbol)
        ytd_list.append(beta_value_buffer[0])
        last_year_list.append(beta_value_buffer[1])
        last_2_year_list.append(beta_value_buffer[2])
    beta_object['Beta (YTD)'] = ytd_list
    beta_object['Beta (Last Year)'] = last_year_list
    beta_object['Beta (Last Two Year)'] = last_2_year_list
    df = pd.DataFrame(beta_object)
    df.set_index('Symbol')
    df.to_csv('beta_list.csv', index=False)
    return df


if __name__ == '__main__':
    # Create simple ui to get symbol input
    window = tk.Tk()
    window.title('Beta Scraper')
    window.configure(background="white")

    style = ttk.Style(window)
    # change theme, you can use style.theme_names() to list themes
    style.theme_use('clam')

    tk.Label(window, text="Symbol List").grid(row=0)
    tk.Label(window, text="EX. A, B, ...").grid(row=1)
    symbol_entry = tk.Entry(window, borderwidth=2)

    symbol_entry.grid(row=0, column=1, pady=10)
    symbol_entry.focus_set()

    button = tk.Button(window, text='Submit',
                       command=get_beta)
    button.grid(row=2, column=1)
    window.mainloop()
