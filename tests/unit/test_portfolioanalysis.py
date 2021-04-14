#!/usr/bin/env python3

from ngankitrading.portfolioanalysis import EltonPortfolio
from ngankitrading.portfolioanalysis import StatsGen
import pandas as pd
import unittest
import os

dir_path = os.path.dirname(os.path.realpath(__name__))
fixtures_path = 'tests/fixtures/test_'
fixtures = os.path.join(dir_path, fixtures_path)
market_index = 'SMICHA'

class TestEltonPortfolio(unittest.TestCase):
    def test_si_optimise(self):
        series = ['yields_df', 'days_dict', 'betas', 'resids_var']
        df = ['rets', 'varcov']
        a = EltonPortfolio()
        [a.__setattr__(x, pd.read_csv(fixtures + x + '.csv', index_col=0,
            squeeze=True)) for x in series]
        [a.__setattr__(x, pd.read_csv(fixtures + x + '.csv', index_col=0))
            for x in df]
        a.si_optimise(market_index=market_index)
        self.assertTrue(a.portfolio.x_i.sum() > 0.999)

class TestStatsGen(unittest.TestCase):
    def test_generate_fits(self):
        a = StatsGen()
        a.rets = pd.read_csv(fixtures + 'rets.csv', index_col=0)
        a.generate_fits(market_index=market_index)
        self.assertEqual(a.rets.shape, a.resids.shape)

if __name__ == '__main__':
    unittest.main()
