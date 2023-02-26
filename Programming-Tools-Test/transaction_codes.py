from enum import Enum, unique


@unique
class TransactionCode(str, Enum):
    BUY_OPEN = 'buy-open'
    SELL_OPEN = 'sell-open'
    BUY_LOW = 'buy-low'
    SELL_HIGH = 'sell-high'
    BUY_CLOSE = 'buy-close'
    SELL_CLOSE = 'sell-close'

    @staticmethod
    def is_buy_transaction(transaction):
        return transaction in [TransactionCode.BUY_LOW, TransactionCode.BUY_CLOSE, TransactionCode.BUY_OPEN]

#     @staticmethod
#     def get_priority(moveCode):
#         if moveCode in {MoveCode.BUY_OPEN, MoveCode.SELL_OPEN}:
#             return 1
#         elif moveCode in {MoveCode.BUY_LOW, MoveCode.SELL_HIGH}:
#             return 2
#         elif moveCode in {MoveCode.BUY_CLOSE, MoveCode.SELL_CLOSE}:
#             return 3
#         else:
#             raise TypeError('Unknown MoveCode')
