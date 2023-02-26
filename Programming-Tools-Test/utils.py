from datetime import timedelta


def get_next_transaction_window(current_date, max_date, number_of_intervals):
    """
    We perform transactions in intervals.
    """
    window = int((max_date - current_date).days / number_of_intervals)
    return current_date.replace(hour=0, minute=0, second=0), (current_date + timedelta(days=window)).replace(hour=0, minute=0, second=0)


def find_starting_dates(df, budget):
    starting_states_df = df[df['Low'] <= budget][['Date', 'StockName', 'Low']].copy()
    starting_states_df.sort_values(by='Date', ascending=True, inplace=True)
    return starting_states_df


def round_value(value, precision=5):
    """
    Helper function to guarantee that all rounded values
    are rounded by default with precision of 4-decimal points.
    """
    return round(value, precision)
