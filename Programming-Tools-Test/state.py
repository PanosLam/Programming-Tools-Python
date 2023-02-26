class State:

    def __init__(self, date, move, stock_name, volume, balance_after_trade):
        self.date = date
        self.move = move
        self.stock_name = stock_name
        self.volume = volume
        self.balance_after_trade = balance_after_trade

    def __str__(self):
        return " ".join([str(self.date.date()), self.move, self.stock_name, str(self.volume)])
