#!/usr/bin/env python3
"""
This module hosts all functions used to import data into the Nganki Project's
trading system.
"""

from dateutil.relativedelta import relativedelta
import controlmodule
import requests
import pandas as pd
import datetime as dt
import yfinance as yf
import os

download_dir = controlmodule.download_dir
ch_eq_file = controlmodule.ch_eq_file

class Yields:
    def scraped_yields(self, download_dir, ch_yield_file):
        """
        Import yield data scraped by the webcrawling module
        """
        df = pd.read_csv(download_dir+'/'+ch_yield_file, index_col=0)
        self.yields_df = df.squeeze()
        self.days_dict = {'1 month': 30, '2 months': 60, '6 months': 180,
                '1 year': 360}

class Equities(Yields):
    def __init__(self, download_dir, ch_eq_file, start_date, end_date):
        self.download_dir = download_dir
        self.ch_eq_file = ch_eq_file
        self.start_date = start_date
        self.end_date = end_date

    def import_yahoo_data(self, market_index):
        """
        Download Swiss daily equity price data from Yahoo Finance.
        """
        col_list = ['Symbol']
        self.symbols = pd.read_csv(
                download_dir+'/'+ch_eq_file, delimiter=';', usecols=col_list)
        self.symbols = self.symbols.append(
                pd.DataFrame([market_index], columns=col_list))
        # Necessary for Yahoo Finance
        suffix = '.SW'
        self.symbols = self.symbols['Symbol'].astype(str) + suffix

        # Download and format Yahoo Finance data
        # In a loop, as some tickers may not be available
        def build_df(start_date, end_date, symbols):
            dates = pd.date_range(start=self.start_date, end=self.end_date)
            six_eq_yahoo = pd.DataFrame(dates, columns=['Date'])
            for ticker in self.symbols:
                try:
                    df = yf.download(
                            ticker, start_date, end_date, interval='1d',
                            progress=False)['Adj Close']
                    df = df.rename(ticker)
                    df = df.reset_index()
                    six_eq_yahoo = pd.merge(
                            six_eq_yahoo, df, on='Date', how='outer')
                except Exception: # This exception needs to be improved
                    pass

            six_eq_yahoo = six_eq_yahoo.set_index('Date')
            six_eq_yahoo = six_eq_yahoo.dropna(how='all')
            six_eq_yahoo.columns = six_eq_yahoo.columns.str.rstrip(suffix)

            return six_eq_yahoo

        self.yahoo_df = build_df(self.start_date, self.end_date, self.symbols)

if __name__ == '__main__':
    pass
