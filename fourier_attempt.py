# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 10:38:59 2021

@author: lando

Does a simple Fourier analysis have predictive power with stock prices?
"""

from sklearn.linear_model import LinearRegression
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Import stock data
    # a. Split the data into train and test data
    # b. Determine the period of the data you want to examine
# 2. Build a wave to fit the training data
    # a. Pass in a depth and a period with the training data
    # b. Plot the wave with the data to make sure I'm not crazy
# 3. Extrapolate the next few periods of the wave and test the wave's effectiveness
    # a. Test the
    # b. Plot both with the test data
# 4. Repeat with different stocks, periods, depths, frequencies, and recency
# 5. Consider using reinforcement machine learning to do the repetitions

def import_stock(ticker='AAPL',freq='monthly',wd='') -> pd.DataFrame:
    assert freq in ['daily','weekly','monthly'], "Invalid frequency"
    return pd.read_csv(wd+f"{ticker}_{freq}.csv")

def get_returns(data):
    # start_date = data.iloc[0]['Date']
    price = data['Adj Close'].values
    returns = np.log(price[1:])-np.log(price[:-1])
    return returns

def split_data(data,a=.7):
    split = math.floor(len(data)*a)
    return data[:split], data[split:]

### Here t is an array-like object
def build_wave(timeline, period:int, depth:int = 10) -> np.ndarray:
    a = np.sqrt(2.)
    li = [.5/(np.pi)*period]
    for i in range(1,depth): li.append(li[-1]*a)
    arr = np.array(li)
    cosines = np.vstack([np.cos(arr*t) for t in timeline])
    return cosines

# def plot_wave(wave_coefs,t_0,t_end,period,depth,step=.01,**kwargs):
#     timeline = np.array([t_0+t*step for t in range(int(t_0/step),int(t_end/step))])
#     print(kwargs)
#     wave = build_wave(int(t_0/step),int(t_end/step),period,depth)
#     y = (wave*wave_coefs).sum(axis=1)
#     plt.plot(
#         timeline,y
#         )

def train_test_fourier(ticker='AAPL',freq='monthly',period=15,depth=5):
    
    data = import_stock(ticker,freq)
    returns = get_returns(data)
    train,test = split_data(returns)
    train_wave = build_wave(np.arange(len(train)),period=period,depth=depth)
    test_wave = build_wave(np.arange(len(train),len(train)+len(test)),period=period,depth=depth)
    
    frr = LinearRegression()
    frr.fit(train_wave,train)
    
    print(f"{ticker} {freq.capitalize()} data, Depth of {depth}")
    print(f'Train R-squared: {frr.score(train_wave,train):.06f}')
    print(f'Test R-squared: {frr.score(test_wave,test):.06f}\n')
    
    plt.plot(
        np.arange(0,len(train),.01),
        frr.predict(
            build_wave(
                np.arange(0,len(train),.01),
                period=period,
                depth=depth
                )
            ),
        color='y',
        label='Trained Wave')
    plt.plot(
        np.arange(len(train),len(train)+len(test),.01),
        frr.predict(
            build_wave(
                np.arange(len(train),len(train)+len(test),.01),
                period=period,
                depth=depth
                )
            ),
        color='r',
        label='Trained Wave')
    plt.scatter(range(len(train)),train,color='b',label='Trained Data')
    plt.scatter(range(len(train),len(train)+len(test)),test,color='g',label='Test Data')
    plt.vlines(len(train),-.21,.21,colors='black',linestyles='dashed',label='End of training')
    # plt.ylim([-.1,.1])
    # plt.xlim([0.,10])
    # plt.legend()
    plt.title(f"{ticker} {freq.capitalize()} data, Depth of {depth}")
    plt.show()

def summarize_results(ticker,freq='all'):
    # Results from daily data
    if freq == 'daily' or freq == 'all':
        train_test_fourier(ticker,'daily',period=252,depth=20)
        train_test_fourier(ticker,'daily',period=252,depth=50)
        train_test_fourier(ticker,'daily',period=252,depth=100)
        train_test_fourier(ticker,'daily',period=252,depth=200)
    
    # Results from weekly data
    if freq == 'weekly' or freq == 'all':
        train_test_fourier(ticker,'weekly',period=52)
        train_test_fourier(ticker,'weekly',period=52,depth = 10)
        train_test_fourier(ticker,'weekly',period=52,depth = 15)
        train_test_fourier(ticker,'weekly',period=52,depth = 20)
    
    # Results from monthly data
    if freq == 'monthly' or freq == 'all':
        train_test_fourier(ticker,'monthly',period=12,depth=3)
        train_test_fourier(ticker,'monthly',period=12)
        train_test_fourier(ticker,'monthly',period=12,depth=7)
        train_test_fourier(ticker,'monthly',period=12,depth=10)

# It would seem (from this one stock) that this form of Fourier analysis
# could be useful for predicting the movement of monthly stock prices.
# Perhaps I could obtain similar results with higher frequency data
# by using only more recent data.

# However, in some cases the model's predictions are dead wrong.
# Perhaps it would be better to test the usefulness of the model by how
# often the direction of the prediction for the very next month is correct.

# Just for funsies I'm including an example of the terrible predictive power
# of overfit models.

train_test_fourier('AAPL','daily',period=252*4,depth=250)
train_test_fourier('AAPL','daily',period=252*4,depth=300)
train_test_fourier('AAPL','daily',period=252*4,depth=500)
train_test_fourier('AAPL','daily',period=252*4,depth=750)
train_test_fourier('AAPL','daily',period=252*4,depth=1000)

# This is just a start but it would be interesting to try and implement this
# with machine learning.

def next_month(ticker:str='AAPL',period:int=12,depth:int=5) -> float:
    data = import_stock(ticker,'monthly')
    returns = get_returns(data)
    wave = build_wave(np.arange(len(returns)),period=period,depth=depth)
        
    frr = LinearRegression()
    frr.fit(wave,returns)
    projection = frr.predict(build_wave([len(returns)],period=period,depth=depth))[0]
    last_price = data.iloc[-1]['Adj Close']
    projected_price = last_price*(1+projection)
    
    print(f"Last month's price: ${last_price:.02f}")
    print(f"Projected return this month: {projection*100:.02f}%")
    print(f"Projected ending price: ${projected_price:.02f}")