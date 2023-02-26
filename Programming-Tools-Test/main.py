# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
from program import Program
from utils import round_value


DATA_PATH = 'C:\\Users\\panos\\Documents\\PhD\\courses\\semester-1\\ProgrammingTools\\Python\\archive\\Stocks\\'

MERGED_DATA_DIR = 'merged\\'

MAX_TRANSACTION_VALUE = 1000000
INITIAL_BUDGET = 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    all_stocks = pd.read_pickle(DATA_PATH + MERGED_DATA_DIR + "all_stocks.pkl")
    all_stocks.reset_index(drop=True, inplace=True)  # reset index to drop rows
    all_stocks.drop(columns=['OpenInt'], inplace=True)
    rowsToDropIndex = all_stocks[(round_value(all_stocks['Low']) == 0) |
                                 (round_value(all_stocks['Volume']) == 0) |
                                 (round_value(all_stocks['High']) == 0)].index
    print(len(rowsToDropIndex))

    all_stocks.drop(rowsToDropIndex, inplace=True)

    all_stocks['Date'] = pd.to_datetime(all_stocks['Date'], format='%Y-%m-%d')
    all_stocks['Date_idx'] = all_stocks['Date']

    all_stocks_idx_df = all_stocks.set_index(['Date_idx'])

    max_date = all_stocks["Date"].max()
    min_date = all_stocks["Date"].min()
    date_diff = (max_date - min_date).days
    print(f'Max Date: {max_date}, Min Date: {min_date}, Date Diff: {date_diff}')

    # N = int(input('Give me the number of trades'))
    N = 5100

    all_stocks_idx_df.sort_index(ascending=True)  # !IMPORTANT: if we don't do this then we won't be able to slice properly

    program = Program(all_stocks_idx_df.head(489500), INITIAL_BUDGET, MAX_TRANSACTION_VALUE, N)

    program.solve()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
