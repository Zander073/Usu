import pandas as pd
import yfinance as yf
import numpy as np
from csv import writer
from datetime import datetime
from constants import *

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

#Prints stock portfolio in a nice format
def print_portfolio(portfolio):
    print('Total Portfolio Value: ', '${:,.2f}'.format(stock_portfolio_value(portfolio.stock_portfolio) + portfolio.cash_balance))
    print('Total Position Value: ', '${:,.2f}'.format(stock_portfolio_value(portfolio.stock_portfolio)))
    print('Total Cash Available for Trading: ', '${:,.2f}'.format(portfolio.cash_balance))
    header = '%12s %12s %15s %12s' % ('Ticker', 'Num Shares', 'Price Bought', 'Current Price')
    print(header)
    for ticker, stock in portfolio.stock_portfolio.items():
        new_line = '%12s  %10s  %12s %12s' % (ticker, stock.num_shares, '${:,.2f}'.format(stock.price), '${:,.2f}'.format(get_price(ticker)))
        print(new_line)
    print()

#Returns the total value of the user's current portfolio
def stock_portfolio_value(portfolio):
    total_value = 0
    for ticker, stock in portfolio.items():
        total_value += (get_price(ticker) * stock.num_shares) 
    return total_value

"""
Adds trade transaction to user's transaction
history.
"""
def add_record(action, ticker, num_shares, price):
    date = datetime.today().strftime('%Y-%m-%d')
    fields = [action, ticker, num_shares, price, date]
    with open(Constants.TRANSACTION_DATA_PATH, 'a', newline='') as f_object:  
        writer_object = writer(f_object)
        writer_object.writerow(fields)  
        f_object.close()

"""
Returns True if the trade order is valid and
False otherwise.
order: A trade order object
portfolio: A portfolio object
"""
def validate_trade(order, portfolio):    
    if order.action == Constants.BUY_ACTION:
        # If the user's cash balance does not exceed the order total, then  true.
        if (get_price(order.ticker) * np.float64(order.num_shares)) <= portfolio.cash_balance:
            return True
    else:
        # If the user owns the stock already and the number of shares in the order is less than or equal to what they already own, then true.
        if order.ticker in portfolio.stock_portfolio and (int(portfolio.stock_portfolio.get(order.ticker).num_shares) >= int(order.num_shares)):
            return True
    print('Error with trade order. Make sure you are within the bounds of your current cash balance/number of owned shares.')
    return False

"""
Checks if the stock ticker exists. Returns true or false.
ticker: String ticker name to be checked.
"""
def check_ticker(ticker):
    print('Checking ticker...')
    ticker = yf.Ticker(ticker)
    if (ticker.info['regularMarketPrice'] == None):
        return False
    return True

"""
Either adds stock into portfolio or adds to position
in portfolio and updates cash balance accordingly.
stock: Stock object
cost: Total cost of trade
portfolio: Portfolio object
"""
def buy(stock, cost, portfolio):
    if stock.ticker in portfolio.stock_portfolio:
        owned_stock = portfolio.stock_portfolio.get(stock.ticker)
        new_cost_avg = ((owned_stock.num_shares * owned_stock.price) + cost) / (owned_stock.num_shares + stock.num_shares)             
        portfolio.stock_portfolio[stock.ticker] = Stock(stock.ticker, (owned_stock.num_shares + stock.num_shares), new_cost_avg)
        portfolio.cash_balance -= cost
    else:
        portfolio.stock_portfolio[stock.ticker] = Stock(stock.ticker, stock.num_shares, stock.price)
        portfolio.cash_balance -= cost

"""
Either removes or reduces position based on trade and
updates cash balance accordingly.
stock: Stock object
cost: Total cost of trade
portfolio: Portfolio object
"""
def sell(stock, cost, portfolio):
    owned_stock = portfolio.stock_portfolio.get(stock.ticker)
    if (stock.num_shares - owned_stock.num_shares) == 0:       
        del portfolio.stock_portfolio[stock.ticker]
        portfolio.cash_balance += cost
    else:
        portfolio.stock_portfolio[stock.ticker] = Stock(stock.ticker, owned_stock.num_shares - stock.num_shares, owned_stock.price)
        portfolio.cash_balance += cost

"""
***Maybe move to file  which handles stock information
Returns the current price of a stock.
ticker: A string of a ticker name of a stock 
price to be returned.
"""
def get_price(ticker):
    ticker_yahoo = yf.Ticker(ticker)
    data = ticker_yahoo.history()
    # Credit for this handy expression to get closing price of ticker: https://stackoverflow.com/a/61892312
    latest_price = data['Close'].iloc[-1]
    return latest_price

class  TradeOrder:
    def __init__(self, action, ticker, num_shares):
        self.action = action
        self.ticker = ticker
        self.num_shares = num_shares

"""
Does a lot of the heavy lifting in terms of needed variables.
stock_portfolio: Dictionary where k = tickers and v = Stock objects
cash_balance: The available balance of cash that can be used for trading
performance: A list of closing position values indexed by date.
"""
class Portfolio:
    def __init__(self):
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
    price = get_price(my_order.ticker)
    my_order_cost = price * my_order.num_shares
    if validate_trade(my_order, my_portfolio):
        temp = Stock(my_order.ticker, my_order.num_shares, price)
        buy(temp, my_order_cost, my_portfolio)
        add_record(my_order.action, my_order.ticker, my_order.num_shares, price)

    print_portfolio(my_portfolio.stock_portfolio)
    print('Current Portfolio Value: ', '${:,.2f}'.format(stock_portfolio_value(my_portfolio.stock_portfolio)))
    print('Current Cash Balance: ', '${:,.2f}'.format(my_portfolio.cash_balance))     