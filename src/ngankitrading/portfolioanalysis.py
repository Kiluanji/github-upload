#!/usr/bin/env python3
"""
Module for the Nganki project's classic portfolio analysis functions, pioneered
by Harry Markowitz.
"""

import pandas as pd
import statsmodels.api as sm

class StatsGen:
    """
    Generate required statistics for portfolio analysis; must first run the
    generate_rets() method, as all statistics are applied on the subject
    financial instruments' returns.
    """
    def generate_rets(self, df, periods=1):
        """
        df: a data frame of price levels
        """
        self.rets = df.pct_change(periods=periods).iloc[periods:].fillna(0)
        # The above fillna(0) might not reflect the real reason for non-
        # -applicable returns, such as IPOs taking place within the data's
        # time frame. Future stages will need to revisit this issue.

    def generate_fits(self, market_index):
        """
        market_index: a string indicating the variable to be used as a proxy
            for market returns.
        """
        x = pd.DataFrame(1, index=self.rets.index, columns=['b0'])
        X = pd.DataFrame(self.rets.eval(market_index), columns=[market_index])
        X = x.merge(X, left_index=True, right_index=True)
        model = lambda x: sm.OLS(self.rets[x], X).fit()
        fits = list(map(model, list(self.rets)))
        self.fits = pd.Series(fits, index=list(self.rets))
        betas = [fits[x].params[1] for x in range(len(fits))]
        self.betas = pd.Series(betas, index=list(self.rets))
        resids = [fits[x].resid for x in range(len(fits))]
        self.resids = pd.concat(resids, axis=1)
        self.resids.columns = list(self.rets) 

    def generate_covrho(self):
        """
        Generate the variance-covariance and correlation matrices
        """
        self.varcov = self.rets.cov()
        self.rho = self.rets.corr()
        self.resids_var = self.resids.var()

class EltonPortfolio:
    """
    Apply the portfolio optimization algorithms as described in Elton et al.
    (2014). Must be run after the portfolioanalysis.StatsGen class of methods,
    which in turn must be run after the dataimport.Equities and
    dataimport.Yields classes of methods.
    """
    def si_optimise(self, market_index, r_f_maturity='1 month'):
        """
        Apply the single-index portfolio optimization algorith as described by
        Elton et al. (2014).

        market_index: a string indicating the variable to be used as a proxy
            for market returns.
        r_f_maturity: the maturity to be used for the risk-free rate of return.
            For avaible options, see 'downloads/ch_yield.csv'.
        """
        if self.yields_df.loc[r_f_maturity] > 0:
            r_f = (self.yields_df.loc[r_f_maturity] /
                    self.days_dict[r_f_maturity])
        else:
            r_f = 0
        mkt_var = self.varcov.eval(market_index).loc[market_index]

        r_ex = (self.rets.mean() - r_f) / self.betas
        r_ex = r_ex.sort_values(ascending=False)
        c_3 = r_ex * self.betas / self.resids_var
        c_4 = self.betas ** 2 / self.resids_var
        df = pd.concat([r_ex, c_3, c_4], axis=1)
        df.columns = ['r_ex', 'c_3', 'c_4']
        df['c_i'] = (mkt_var * df.c_3.cumsum()) / (
                1 + mkt_var * df.c_4.cumsum()) 
        r_ex_star = df[df.r_ex < df.c_i].iloc[0].r_ex
        c_star = df[df.r_ex < df.c_i].iloc[0].c_i
        df = df[df.r_ex > r_ex_star]
        df['z_i'] = (self.betas / self.resids_var) * (df.r_ex - c_star)
        df['x_i'] = df.z_i / df.z_i.sum()
        portfolio = pd.concat([df.x_i, self.rets.mean(), self.rets.std()],
                axis=1, join='inner')
        portfolio.columns = ['x_i', 'r_i', 'sd']
        self.portfolio = portfolio

if __name__ == '__main__':
    pass
