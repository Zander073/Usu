import yfinance as yf
import numpy as np
import os
from constants import *
from portfolio import *


# Prints the available actions the user may take.
def print_menu():
    print("Available actions:")
    print("1. Trade \n2. View performance \n3. Observe a stock quote \n4. Exit")

# Prompts user what action they would like to take and returns which action.
def prompt_action():
    print_menu()
    while True:
        action = input("Select an action (input the action's number: ")
        if (action == '1' or action == '2' or action == '3' or action == '4'):
            break
        else:
            print(Constants.SPACER)
            print("Invalid input. Please select from the following choices:")           
            print_menu()
    print()
    return action

def prompt_trade_action():
    print('1. Buy \n2. Sell')
    while True:
        action = input("Select an action (input the action's number): ")
        if (action == '1' or action == '2'):
            break
        else:
            print(Constants.SPACER)
            print('Invalid input, please input 1 to buy or 2 to sell.')                
    return action

def print_order_summary(ticker, num_shares, cost):
    print('Order summary ')
    print('Ticker:', ticker)
    print('Num shares: ', num_shares)
    print('Total approx. cost: ', '${:,.2f}'.format(cost))
    print()

def buy_action(portfolio):
    while True:
        action = Constants.BUY_ACTION
        ticker = input('Please input the ticker you wish to trade: ')
        num_shares = input('Please input the number of shares you wish to purchase: ')
        order = TradeOrder(action, ticker, num_shares)
        if check_ticker(ticker) and validate_trade(order, portfolio):
            num_shares = np.float64(num_shares)
            price = get_price(ticker)
            cost = num_shares * price
            print_order_summary(ticker, num_shares, cost)
            while True:
                execute = input('Input 1 to execute, 2 to clear order, or 3 to return to menu (order will not execute): \n')
                # Execute order
                if execute == '1':
                    stock_to_buy = Stock(ticker, num_shares, cost/num_shares)
                    buy(stock_to_buy, cost, portfolio)
                    add_record(order.action, order.ticker, order.num_shares, price)
                    print('Order has been executed.\n')
                    return None
                # Clear order
                elif execute == '2':
                    pass
                # Return to main menu
                elif execute == '3':
                    return None
                else:
                    print('Your trade order was invalid. Please try again.')
        else:
            print('Your trade order was invalid. Please try again.')

def sell_action(portfolio):
    while True:
        action = Constants.SELL_ACTION
        ticker = input('Please input the ticker you wish to trade: ')
        num_shares = input('Please input the number of shares you wish to sell: ')
        order = TradeOrder(action, ticker, num_shares)
        if check_ticker(ticker) and validate_trade(order, portfolio):
            num_shares = np.float64(num_shares)
            price = get_price(ticker)
            cost = num_shares * price
            print_order_summary(ticker, num_shares, cost)
            condition = True
            while condition:
                execute = input('Input 1 to execute, 2 to clear order, or 3 to return to menu (order will not execute): \n')
                # Execute order
                if execute == '1':
                    stock_to_sell = Stock(ticker, num_shares, cost/num_shares)
                    sell(stock_to_sell, cost, portfolio)
                    add_record(order.action, order.ticker, order.num_shares, price)
                    print('Order has been executed.\n')
                    return None
                # Clear order
                elif execute == '2':
                    condition = False
                # Return to main menu
                elif execute == '3':
                    return None
                else:
                    print('Your trade order was invalid. Please try again.')
        else:
            print('Your trade order was invalid. Please try again.')

def prompt_ticker():
    while True:
        ticker = input('Enter a ticker you would like to examine.')
        if check_ticker(ticker):
            return ticker
        else:
            print('There was an error finding this ticker, please try a different one.\n')

def get_total_return(portfolio):
    return (((stock_portfolio_value(portfolio.stock_portfolio) + portfolio.cash_balance) - Constants.INITIAL_CASH_BALANCE)/Constants.INITIAL_CASH_BALANCE) * 100

if __name__=="__main__":
    print('Welcome to Usu, a monetary-free stock trading platform.')
    my_portfolio = build_portfolio(Portfolio())
    while True:
        action = prompt_action()
        #Trade
        if action == '1':
            print_portfolio(my_portfolio)
            trade_action = prompt_trade_action()
            if trade_action == '1':
                buy_action(my_portfolio)
            if trade_action == '2':
                sell_action(my_portfolio)
        #View performance
        if action == '2':
            print_portfolio(my_portfolio)
            print('Total Return: ', "{:.2f}".format(get_total_return(my_portfolio)), '%')
            print()
            input("Press Enter to continue...")
            print(Constants.SPACER)
        #3 Observe a stock quote
        if action == '3':
            ticker = prompt_ticker()
        if action == '4':
            print('Thank you for using Usu. Your transactions are saved.')
            break
        os.system('cls' if os.name == 'nt' else 'clear')