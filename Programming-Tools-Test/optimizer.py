import pandas as pd
from exceptions import OptimizationError
from utils import round_value


class Optimizer:

    def __init__(self) -> None:
        super().__init__()

    def optimize_buy_low_sell_high(self, trading_data_df, min_price, min_price_date):
        trading_data_df['cummin'] = trading_data_df['Low'].cummin()  # TODO: Improvement - put directly the min_price, because the local df starts from the min price because of the caller
        trading_data_df['cummax_rev'] = list(pd.Series(reversed(trading_data_df['High'])).cummax())
        trading_data_df['diff_rev'] = trading_data_df['cummax_rev'] - trading_data_df['cummin']

        max_profit = trading_data_df['diff_rev'].max()
        max_profit_sell_price_df = trading_data_df[trading_data_df['diff_rev'] == max_profit].head(1)

        max_profit_sell_price = max_profit_sell_price_df['cummax_rev'].iloc[0]

        max_profit_sell_price_df_row = trading_data_df[trading_data_df['High'] == max_profit_sell_price].head(1)
        volume_in_max_price = max_profit_sell_price_df_row['Volume'].iloc[0]
        max_price_date = max_profit_sell_price_df_row['Date'].iloc[0]

        if max_price_date == min_price_date:
            raise OptimizationError('Cannot optimize (BUY_LOW, SELL_HIGH) within the same day.')

        volume_in_min_price = trading_data_df[round_value(trading_data_df['Low']) == round_value(min_price)].head(1)['Volume'].iloc[0]
        return max_profit_sell_price, max_price_date, min(volume_in_max_price, volume_in_min_price)

    def optimize_buy_open_sell_high(self, trading_data_df, min_open_price):
        """
        Profit here is >= 0
        """
        trading_data_df['cummin_bopen_shigh'] = trading_data_df['Open'].cummin()
        trading_data_df['cummax_rev_bopen_shigh'] = list(pd.Series(reversed(trading_data_df['High'])).cummax())
        trading_data_df['diff_rev_bopen_shigh'] = trading_data_df['cummax_rev_bopen_shigh'] - trading_data_df['cummin_bopen_shigh']

        max_profit = round_value(trading_data_df['diff_rev_bopen_shigh'].max())
        max_profit_sell_price_df = trading_data_df[round_value(trading_data_df['diff_rev_bopen_shigh']) == max_profit].head(1)

        max_profit_sell_price = max_profit_sell_price_df['cummax_rev_bopen_shigh'].iloc[0]

        max_profit_sell_price_df_row = trading_data_df[trading_data_df['High'] == max_profit_sell_price].head(1)
        volume_in_max_price = max_profit_sell_price_df_row['Volume'].iloc[0]
        max_price_date = max_profit_sell_price_df_row['Date'].iloc[0]

        volume_in_min_price = trading_data_df[round_value(trading_data_df['Open']) == round_value(min_open_price)].head(1)['Volume'].iloc[0]
        return max_profit_sell_price, max_price_date, min(volume_in_max_price, volume_in_min_price)

    def __optimize_buy_low_sell_close__(self, trading_data_df, min_low_price):
        """
        Profit here is >= 0
        """
        trading_data_df['cummin_blow_sclose'] = trading_data_df['Low'].cummin()
        trading_data_df['cummax_rev_blow_sclose'] = list(pd.Series(reversed(trading_data_df['Close'])).cummax())
        trading_data_df['diff_rev_blow_sclose'] = trading_data_df['cummax_rev_blow_sclose'] - trading_data_df['cummin_blow_sclose']

        max_profit = trading_data_df['diff_rev_blow_sclose'].max()
        max_profit_sell_price_df = trading_data_df[trading_data_df['diff_rev_blow_sclose'] == max_profit].head(1)

        max_profit_sell_price = max_profit_sell_price_df['cummax_rev_blow_sclose'].iloc[0]

        max_profit_sell_price_df_row = trading_data_df[trading_data_df['Close'] == max_profit_sell_price].head(1)
        volume_in_max_price = max_profit_sell_price_df_row['Volume'].iloc[0]
        max_price_date = max_profit_sell_price_df_row['Date'].iloc[0]

        volume_in_min_price = trading_data_df[trading_data_df['Low'] == min_low_price].head(1)['Volume'].iloc[0]
        return max_profit_sell_price, max_price_date, min(volume_in_max_price, volume_in_min_price)
