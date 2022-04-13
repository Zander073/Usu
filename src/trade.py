from ast import And
import yfinance as yf
from portfolio import Portfolio, Stock
from constants import *

"""
Returns True if the trade order is valid and
False otherwise.
order: A trade order object
"""
def validate_trade(order, portfolio):    
    if order.action == Constants.BUY_ACTION:
        # If the user's cash balance does not exceed the order total, then  true.
        if (get_price(order.ticker) * order.num_shares) <= portfolio.cash_balance:
            return True
    else:
        # If the user owns the stock already and the number of shares in the order is less than or equal to what they already own, then true.
        if order.ticker in portfolio.stock_portfolio and (portfolio.stock_portfolio.get(order.ticker).num_shares >= order.num_shares):
            return True
    return False

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

