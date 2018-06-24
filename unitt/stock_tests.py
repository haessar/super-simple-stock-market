from unittest import TestCase
import numpy as np

import src.main as main

class TestStock(TestCase):
    def setUp(self):
        stocks = (
            ('TEA', 'common', 0, 100),
            ('POP', 'common', 8, 100),
            ('ALE', 'common', 23, 60),
            ('GIN', 'preferred', 8, 100, 2),
            ('JOE', 'common', 13, 250),
        )
        self.trade_instructions = (
            [(2, 'buy', 30)],
            [(3, 'sell', 15), (4, 'buy', 10)],
            [(1, 'sell', 45)],
            [(2, 'sell', 50)],
            [(1, 'buy', 25), (2, 'buy', 30)],
        )
        self.stocks = []
        for stock, instructions in zip(stocks, self.trade_instructions):
            stock = main.Stock(*stock)
            self.stocks.append(stock)
            for instruction in instructions:
                stock.trade(*instruction)
    def test_init(self):
        bad_stocks = (
            ('BAD1', 'typeless', 0, 100),
            ('BAD2', 'preferred', 0, 100, 'nan')
        )
        for stock in bad_stocks:
            with self.assertRaises(AssertionError):
                main.Stock(*stock)
    def test_prices(self):
        prices = [1.0, 20, 50, 100]
        for stock in self.stocks:
            with self.assertRaises(ValueError):
                stock.div_yield('not_a_price')
            with self.assertRaises(ZeroDivisionError):
                stock.div_yield(0)
            for price in prices:
                if stock.type == 'common':
                    self.assertEqual(stock.last_div / price, stock.div_yield(price))
                elif stock.type == 'preferred':
                    self.assertEqual(stock.fixed_div * stock.par_val / price, stock.div_yield(price))
                if stock.last_div == 0:
                    with self.assertRaises(ZeroDivisionError):
                        stock.p_e_ratio(price)
    def test_trades(self):
        for stock, instructions in zip(self.stocks, self.trade_instructions):
            with self.assertRaises(AssertionError):
                stock.trade(1, 'unknown', 0)
            self.assertEqual(len(stock.trades), len(instructions))
            self.assertIsInstance(stock.volume_weighted_stock_price(np.inf), (int, float))
            self.assertEqual(stock.volume_weighted_stock_price(0), None)
    def test_all_share_index(self):
        self.assertIsInstance(main.gbce_all_share_index(self.stocks, age=np.inf), np.float)
        self.assertEqual(main.gbce_all_share_index(self.stocks, age=0), None)
