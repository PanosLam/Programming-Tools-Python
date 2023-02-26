from transaction_codes import TransactionCode
from suggested_transaction import SuggestedTransaction
from utils import round_value
from optimizer import Optimizer
from exceptions import OptimizationError


class TradingEngine:

    def __init__(self) -> None:
        super().__init__()
        self.optimizer = Optimizer()

    def find_trades(self, stocks_df) -> list[SuggestedTransaction]:
        """
        Finds best trades within a time window for each stock in it.
        The strategy is to find the lowest price inside the window,
        buy the stock and sell it in the next available highest price,
        within the same window.
        """
        stock_names = stocks_df['StockName'].unique()
        suggested_transaction_list = []

        for stock_name in stock_names:
            stock_df = stocks_df[stocks_df['StockName'] == stock_name].copy()

            min_stock_price = round_value(stock_df['Low'].min())

            min_price_date = stock_df.index[round_value(stock_df['Low']) == min_stock_price].min()  # get date index of min value

            trading_df = stock_df.loc[stock_df.index >= min_price_date].copy()

            try:
                max_profit_sell_price, max_price_date, transaction_volume = self.optimizer.optimize_buy_low_sell_high(trading_df, min_stock_price, min_price_date)
                buy_trade_type, sell_trade_type = TransactionCode.BUY_LOW, TransactionCode.SELL_HIGH
            except OptimizationError:
                min_open_price = round_value(stock_df['Open'].min())
                min_open_date = stock_df.index[round_value(stock_df['Open']) == min_open_price].min()
                trading_open_df = stock_df.loc[stock_df.index >= min_open_date].copy()
                max_profit_sell_price, max_price_date, transaction_volume = self.optimizer.optimize_buy_open_sell_high(trading_open_df, min_open_price)
                buy_trade_type, sell_trade_type = TransactionCode.BUY_OPEN, TransactionCode.SELL_HIGH
                min_stock_price = min_open_price  # TODO: Hot fix, please make it better
                min_price_date = min_open_date

            suggested_transaction_list.append(SuggestedTransaction(min_stock_price, min_price_date, buy_trade_type,
                                                                   max_profit_sell_price, max_price_date,
                                                                   sell_trade_type,
                                                                   transaction_volume, stock_name))
        return suggested_transaction_list
