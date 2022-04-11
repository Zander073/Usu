import pandas as pd
import yfinance as yf
from collections import namedtuple
from constants import *

"""
This file is responsible for reading and writing transaction tuples 
to the data file so users' portfolios can be created. Because users 
automatically start off with $x USD, by tracking every transaction, 
we do not have to manipulate the current portfolio rather we can build
it and track the users performance.
"""

"""
A transaction tuple which packages all of the necessary information 
to build a user's portfolio and performance based on history.

action: Bought or sold the stock.
ticker_name: The ticker name of the stock.
num_shares: The number of shares. 
price: The price in which the action was executed.
date_executed: The date the transaction took place in format YEAR-MONTH-DAY.
"""

#ptb: portfolio to be built
def build_portfolio(ptb):
    transaction_df = pd.read_csv(Constants.DATA_PATH)

    for index, row in transaction_df.iterrows():
        action = row['action']
        stock = Stock(row['ticker'], row['num_shares'], row['price'])
        cost = stock.num_shares * stock.price

        # Buy action:
        if action == 'BUY':
            if stock.ticker in ptb.stock_portfolio:
                owned_stock = ptb.stock_portfolio.get(stock.ticker)
                new_cost_avg = ((owned_stock.num_shares * owned_stock.price) + cost) / (owned_stock.num_shares + stock.num_shares)             
                ptb.stock_portfolio[stock.ticker] = Stock(stock.ticker, (owned_stock.num_shares + stock.num_shares), new_cost_avg)
                ptb.cash_balance -= cost
            else:
                ptb.stock_portfolio[stock.ticker] = Stock(stock.ticker, stock.num_shares, stock.price)
                ptb.cash_balance -= cost

        # Sell action:
        else:
            owned_stock = ptb.stock_portfolio.get(stock.ticker)
            if (stock.num_shares - owned_stock.num_shares) == 0:
                del ptb.stock_portfolio[stock.ticker]
            else:
                ptb.stock_portfolio[stock.ticker] = Stock(stock.ticker, owned_stock.num_shares - stock.num_shares, owned_stock.price)
            ptb.cash_balance += cost

    print_portfolio(ptb.stock_portfolio)
    print('Current Portfolio Value: ', '${:,.2f}'.format(stock_portfolio_value(ptb.stock_portfolio)))
    print('Current Cash Balance: ', '${:,.2f}'.format(ptb.cash_balance))      
    
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
        ticker_yahoo = yf.Ticker(ticker)
        data = ticker_yahoo.history()
        # Credit for this handy expression to get closing price of ticker: https://stackoverflow.com/a/61892312
        lastest_price = data['Close'].iloc[-1]
        total_value += (lastest_price * stock.num_shares) 
    return total_value

class Portfolio:
    def __init__(self):
        # Stock portfolio dictionary is keyed by ticker name and its value is a Stock object
        self.stock_portfolio = {}
        self.cash_balance = Constants.INITIAL_CASH_BALANCE
        self.performance = []
        
class Stock:
    def __init__(self, ticker, num_shares, price):
        self.ticker = ticker
        self.num_shares = num_shares
        self.price = price

# Driver code
if __name__=="__main__":
    build_portfolio(Portfolio())