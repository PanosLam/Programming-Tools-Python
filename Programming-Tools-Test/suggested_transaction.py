class SuggestedTransaction:

    def __init__(self, min_price, min_price_date, min_transaction_code,
                 max_price, max_price_date, max_transaction_code,
                 transaction_volume, stock_name) -> None:
        super().__init__()
        self.min_price = min_price
        self.min_price_date = min_price_date
        self.buy_transaction_code = min_transaction_code
        self.max_price = max_price
        self.max_price_date = max_price_date
        self.sell_transaction_code = max_transaction_code
        self.transaction_volume = transaction_volume
        self.stock_name = stock_name

    def __str__(self) -> str:
        return " ".join([str(self.min_price), str(self.min_price_date), self.buy_transaction_code,
                         str(self.max_price), str(self.max_price_date), self.sell_transaction_code,
                         str(self.transaction_volume), self.stock_name])

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SuggestedTransaction) and \
               (other.stock_name == self.stock_name) and \
               (other.min_price_date == self.min_price_date) and \
               (other.max_price_date == self.max_price_date)

    def __hash__(self) -> int:
        return hash("".join([self.stock_name, str(self.min_price_date), str(self.max_price_date)]))

