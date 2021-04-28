#!/usr/bin/env python3
"""
This script is used to run Nganki Project's deployed trading system.
"""

from emailmodule import email_results
import controlmodule
import dataimport
import portfolioanalysis

download_dir = controlmodule.download_dir
output_dir = controlmodule.output_dir
ch_yield_file = controlmodule.ch_yield_file
ch_eq_file = controlmodule.ch_eq_file
portfolio_file = controlmodule.portfolio_file
end_date = controlmodule.end_date
start_date = controlmodule.start_date
market_index = controlmodule.market_index

class TradingObject(dataimport.Equities, dataimport.Yields,
        portfolioanalysis.StatsGen,
        portfolioanalysis.EltonPortfolio):
    pass

ch_eq = TradingObject(download_dir, ch_eq_file, start_date, end_date)
ch_eq.import_yahoo_data(market_index=market_index)
ch_eq.scraped_yields(download_dir, ch_yield_file)
ch_eq.generate_rets(df=ch_eq.yahoo_df, periods=1)
ch_eq.generate_fits(market_index)
ch_eq.generate_covrho()
ch_eq.si_optimise(market_index=market_index)
ch_eq.portfolio.to_csv(output_dir + portfolio_file)

if __name__ == '__main__':
    email_results(files=[output_dir + portfolio_file])
    pass
