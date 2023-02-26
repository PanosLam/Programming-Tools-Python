from trading_engine import TradingEngine
from collections import deque
from utils import get_next_transaction_window, round_value
from suggested_transaction import SuggestedTransaction
from state import State
from datetime import timedelta
from exceptions import ValidationError
import pandas as pd


class Trader:

    def __init__(self, stock_history, initial_budget, max_transaction_value, number_of_transactions):
        self.stock_history = stock_history
        self.budget = initial_budget
        self.max_transaction_value = max_transaction_value
        if number_of_transactions < 1:
            raise ValueError('Number of transactions cannot be zero or negative.')
        elif number_of_transactions % 2 != 0:
            raise ValueError('Number of transactions must be even number.')
        self.number_of_transactions = number_of_transactions // 2
        self.engine = TradingEngine()

    def trade(self):
        current_date = self.stock_history["Date"].min()
        max_date = self.stock_history["Date"].max()
        trades = deque()

        trade_history_df = pd.DataFrame(columns=self.stock_history.columns)
        desired_transactions = self.number_of_transactions

        while desired_transactions > 0 and current_date < max_date:
            start_date, end_date = get_next_transaction_window(current_date, (max_date + timedelta(days=1)),
                                                               desired_transactions)
            end_date -= timedelta(days=1)

            slice_df = self.stock_history.loc[(self.stock_history.index >= start_date) &
                                              (self.stock_history.index <= end_date)]
            suggested_trade_list = self.engine.find_trades(slice_df)
            best_trade, max_profit, trade_volume = self.__decide_best_trade__(suggested_trade_list)

            if not (best_trade is None):
                # go to next window if we didn't find any best trade in the window
                desired_transactions -= 1
                # Get the DF related to the best trade for the wide trading window
                best_trade_df = slice_df[slice_df['StockName'] == best_trade.stock_name].copy()
                best_trade_df['Balance'] = self.budget  # initialize Balance BEFORE performing any trade
                best_trade_df['Portfolio'] = 0

                buy_trade = self.__buy_stock__(best_trade, trade_volume, best_trade_df)
                sell_trade = self.__sell_stock__(best_trade, trade_volume, best_trade_df)

                trades.append(buy_trade)
                trades.append(sell_trade)
                trade_history_df = pd.concat([best_trade_df, trade_history_df])
                current_date = sell_trade.date + timedelta(days=1)  # set current date the next day after selling a stock
            else:
                current_date = end_date

        return trades, trade_history_df

    def __decide_best_trade__(self, suggested_trade_list: list[SuggestedTransaction]) \
            -> tuple[SuggestedTransaction, int, int]:
        """
        Best trade is decided by maximizing: unit_profit * volume
        """
        best_trade = None
        max_profit = 0
        trade_volume = 0
        for suggested_trade in suggested_trade_list:
            if not self.__can_buy_unit__(suggested_trade.min_price):
                continue  # check next stock if we cannot buy not even a single unit from the current one
            stock_profit, volume = self.__calculate_profit_for_trade__(suggested_trade)
            if stock_profit > max_profit:
                max_profit = stock_profit
                best_trade = suggested_trade
                trade_volume = volume

        return best_trade, max_profit, trade_volume

    def __can_buy_unit__(self, stock_price):
        return round_value(self.budget) >= round_value(stock_price)

    def __calculate_profit_for_trade__(self, suggested_trade: SuggestedTransaction):
        volume_to_buy = self.__calculate_volume_afford_to_buy__(suggested_trade)
        return round_value((suggested_trade.max_price - suggested_trade.min_price) * volume_to_buy), volume_to_buy

    def __calculate_volume_afford_to_buy__(self, suggested_trade: SuggestedTransaction):
        """
        We can trade specific stock volumes:
        1. What we can buy based on our current budget
        2. What we can buy based on the available stock volume
        3. What we can buy in regards to the restriction of not buying stocks
           with value more than the maximum transaction threshold

        From those three categories, we select the minimum volume, because
        either our budget is not enough to buy more, or there is no more
        stocks to trade that day, or we are capped by the transaction threshold.
        """

        volume = min(suggested_trade.transaction_volume,
                     int(self.budget / suggested_trade.min_price),
                     int(self.max_transaction_value / suggested_trade.min_price))

        if volume * suggested_trade.min_price > self.max_transaction_value:
            raise ValidationError(f'Max allowed daily limit is: {self.max_transaction_value}, ' +
                                  f'you bought {volume * suggested_trade.min_price} ')

        return volume

    def __buy_stock__(self, best_trade: SuggestedTransaction, trade_volume: int, best_trade_df: pd.DataFrame):
        """
        Update Balance & Portfolio for all the dates after buying the stock.
        Subsequent dates will be corrected when we will sell the stock.

        Create the buy state.
        """
        self.budget = round_value(self.budget - best_trade.min_price * trade_volume)

        select_mask = best_trade_df.index >= best_trade.min_price_date
        best_trade_df.loc[select_mask, 'Balance'] = self.budget
        best_trade_df.loc[select_mask, 'Portfolio'] = best_trade_df.loc[select_mask]['High'] * trade_volume

        return State(best_trade.min_price_date,
                     best_trade.buy_transaction_code,
                     best_trade.stock_name,
                     trade_volume,
                     self.budget)

    def __sell_stock__(self, best_trade: SuggestedTransaction, trade_volume: int, best_trade_df: pd.DataFrame):
        """
        The trade model is to buy as much stocks as you want and sell them at the next best price,
        since the moment of the buy. After selling the stock, the portfolio is empty, thus why we
        fill with zero value.
        """
        self.budget = round_value(self.budget + best_trade.max_price * trade_volume)

        select_mask = best_trade_df.index >= best_trade.max_price_date
        best_trade_df.loc[select_mask, 'Balance'] = self.budget
        best_trade_df.loc[select_mask, 'Portfolio'] = 0

        return State(best_trade.max_price_date,
                     best_trade.sell_transaction_code,
                     best_trade.stock_name,
                     trade_volume,
                     self.budget)
