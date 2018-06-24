import datetime
import pandas as pd
from scipy import stats

class Stock:
    def __init__(self, symbol, type, last_div, par_val, fixed_div=None):
        """
        :param symbol: str Stock symbol.
        :param type: str Stock type; 'common' or 'preferred'.
        :param last_div: float Last dividend in pennies.
        :param par_val: float Par value in pennies.
        :param fixed_div: float Fixed dividend percentage. Required for 'preferred' type.
        """
        self.symbol = symbol
        self.type = type.lower()
        assert self.type in ['common', 'preferred'], "type must be either 'common' or 'preferred'."
        self.last_div = float(last_div)
        if self.type == 'preferred':
            assert isinstance(fixed_div, (int, float)), "numeric fixed_div must be provided for 'preferred' type stock."
            self.fixed_div = float(fixed_div) / 100
        self.par_val = float(par_val)
        self.trades = pd.DataFrame()
    def div_yield(self, price):
        if self.type == 'preferred':
            return (self.fixed_div * self.par_val) / float(price)
        else:
            return self.last_div / float(price)
    def p_e_ratio(self, price):
        return float(price) / self.last_div
    def trade(self, quantity, bs, price):
        assert bs.lower() in ['buy', 'sell'], "designate whether trade is to 'buy' or 'sell'."
        data = {
            'Quantity': quantity,
            'Buy/Sell': bs.lower(),
            'Price': price,
        }
        record = pd.DataFrame(data, index=[pd.Timestamp.now()])
        self.trades = self.trades.append(record)
    def volume_weighted_stock_price(self, age=5 * 60):
        recent_trades = self.trades[(datetime.datetime.now() - self.trades.index).total_seconds() <= age]
        if not recent_trades.empty:
            return (recent_trades.Price * recent_trades.Quantity).sum() / recent_trades.Quantity.sum()

def gbce_all_share_index(stocks, age=5 * 60):
    vwsp = []
    for stock in stocks:
        stock_vwsp = stock.volume_weighted_stock_price(age)
        if stock_vwsp:
            vwsp.append(stock_vwsp)
    if vwsp:
        return stats.gmean(vwsp)
