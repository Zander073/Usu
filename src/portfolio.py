import pandas as pd
import yfinance as yf
from collections import namedtuple
from constants import *
from trade import *

"""
Builds the user's present day portfolio by examining the
user's transaction history. The result is written into
the portfolio object. Specifically, the 'portfolio'
dictionary attribute is keyed with ticker names and its
values are Stock objects. 
ptb: portfolio object to be built upon, empty initially
"""
def build_portfolio(ptb):
    transaction_df = pd.read_csv(Constants.TRANSACTION_DATA_PATH)

    for index, row in transaction_df.iterrows():
        action = row['action']
        stock = Stock(row['ticker'], row['num_shares'], row['price'])
        cost = stock.num_shares * stock.price

        if action == Constants.BUY_ACTION:
            buy(stock, cost, ptb)
        else:
            sell(stock, cost, ptb)
          
    return ptb 


#Returns a list of df objects indexed by date (from transaction history)
def sort_transaction():
    return None

#Prints our stock portfolio in a nice format
def print_portfolio(portfolio):
    for ticker, stock in portfolio.items():
        print(ticker, ' - ', stock.num_shares, ' - ', '${:,.2f}'.format(stock.price))

#Returns the total value of the user's current portfolio
def stock_portfolio_value(portfolio):
    total_value = 0
    for ticker, stock in portfolio.items():
        total_value += (get_price(ticker) * stock.num_shares) 
    return total_value

class Portfolio:
    def __init__(self):
        # Stock portfolio dictionary is keyed by ticker name and its value is a Stock object
        self.stock_portfolio = {}
        self.cash_balance = Constants.INITIAL_CASH_BALANCE
        self.performance = []

    def get_stock_portfolio(self):
        return self.stock_portfolio

    def get_cash_balance(self):
        return self.cash_balance
           
class Stock:
    def __init__(self, ticker, num_shares, price):
        self.ticker = ticker
        self.num_shares = num_shares
        self.price = price

# Driver code
if __name__=="__main__":
    my_portfolio = build_portfolio(Portfolio())
    my_order = TradeOrder('BUY', 'AAPL', 5)
    my_order_cost = get_price(my_order.ticker) * my_order.num_shares
    if validate_trade(my_order, my_portfolio):
        temp = Stock(my_order.ticker, my_order.num_shares, get_price(my_order.ticker))
        buy(temp, my_order_cost, my_portfolio)

        print_portfolio(my_portfolio.stock_portfolio)
        print('Current Portfolio Value: ', '${:,.2f}'.format(stock_portfolio_value(my_portfolio.stock_portfolio)))
        print('Current Cash Balance: ', '${:,.2f}'.format(my_portfolio.cash_balance)) 