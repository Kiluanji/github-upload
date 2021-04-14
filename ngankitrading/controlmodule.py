#!/usr/bin/env python3
"""
This module controls the universal inputs and timing of the Nganki Project's
trading system.
"""

import datetime as dt
import os

dir_path = os.path.dirname(os.path.realpath(__name__))
download_dir = os.path.join(dir_path, 'downloads/')
output_dir = os.path.join(dir_path, 'outputs/')
try:
    os.mkdir(download_dir)
except FileExistsError:
    pass
try:
    os.mkdir(output_dir)
except FileExistsError:
    pass
ch_yield_file = 'ch_yield.csv'
ch_eq_file = 'six_eq.csv'
portfolio_file = 'portfolio.csv'
end_date = dt.datetime.now().date() - dt.timedelta(days=1)
start_date = end_date - dt.timedelta(days=365)
market_index = 'SMICHA'
