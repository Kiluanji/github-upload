#!/usr/bin/env python3
"""
This module runs separate to the other components of Nganki project's trading
system, and it is responsible for retrieving web-scraped data.
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import re
import pandas as pd
import requests
import controlmodule

parser = 'html5lib'
download_dir = controlmodule.download_dir
ch_yield_file = controlmodule.ch_yield_file

def scrape_ch_yield(url=
        'http://www.worldgovernmentbonds.com/country/switzerland/',
        file_name=ch_yield_file):
    """
    Scrape yield data for Swiss Federal Bonds.
    """
    html = urlopen(url)
    bs = BS(html.read(), parser)
    table_body = bs.find('a', href=re.compile('1-month')).parent.parent.parent
    rows = table_body.find_all('tr')
    cols = len(rows[0])
    df = pd.DataFrame(columns=list(range(cols)))

    for row in rows:
        cols = row.find_all('td')
        cols = [x.text.strip() for x in cols]
        df = df.append(pd.DataFrame(cols).T)
    
    df = df.reset_index(drop=True)
    df = df[[1,2]]
    colnames = ['maturity', 'ytm']
    df.columns = colnames
    df.index = df[colnames[0]]
    df = df[colnames[1]]
    df = df.str.rstrip('%').astype('float')/100

    df.to_csv(download_dir + '/' + file_name)

def get_ch_listed_eq(url='https://www.six-group.com/sheldon/'
        'equity_issuers/v1/equity_issuers.csv', file_name='six_eq.csv'):
    """
    Scrape the list of equities publicly listed in the main Swiss exchange
    """
    six_eq = requests.get(url)
    
    with open(download_dir + '/' + file_name, 'wb') as f:
        f.write(six_eq.content)

if __name__ == '__main__':
    get_ch_listed_eq()
    scrape_ch_yield()
    pass
