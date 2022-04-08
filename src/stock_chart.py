from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import matplotlib as plt
import yfinance as yf

root = Tk()
root.title = 'Stock chart'
ticker = 'AAPL'

def graph(ticker):
    data = yf.download(tickers=ticker, period='1d', interval='1m')
    plt.plot(data)

my_button = Button(root, text = 'Chart', command = graph(ticker))
my_button.pack()

root.mainloop()
