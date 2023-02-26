from time import time
from trader import Trader
from collections import deque
import pandas as pd
import matplotlib.pyplot as plt


class Program:

    def __init__(self, stock_history, initial_budget, max_transaction_value, number_of_transactions) -> None:
        self.stock_history = stock_history
        self.number_of_trades = number_of_transactions
        self.trader = Trader(stock_history, initial_budget, max_transaction_value, number_of_transactions)

    def solve(self):
        trade_start = time()
        trades, trade_history_df = self.trader.trade()
        trade_end = time()
        self.__write_trades__(trades)
        print(f'Total trading time: {round((trade_end - trade_start) // 60, 3)} minutes '
              f'{round((trade_end - trade_start) % 60, 3)} seconds.')
        last_trade = trades.pop()
        print(f'Total profit: {last_trade.balance_after_trade}')
        trades.append(last_trade)
        self.__plot__(trade_history_df)

    def __write_trades__(self, trades: deque):
        f = open(f'./trades/trades-{self.number_of_trades}.txt', "w")
        f.write(str(self.number_of_trades) + '\n')
        for trade in trades:
            f.write(str(trade) + '\n')
        f.close()

    def __plot__(self, plot_df: pd.DataFrame):
        plt.bar(plot_df['Date'], plot_df['Balance'], color='b', label='Balance')
        plt.bar(plot_df['Date'], plot_df['Portfolio'], color='tab:orange', label='Portfolio')

        plt.yscale("log")
        plt.legend()
        plt.savefig(f'./plots/trade-plot-{self.number_of_trades}.png', dpi=800)
        # plt.show()
