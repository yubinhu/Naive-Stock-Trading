# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 12:22:17 2019

@author: yubin
"""

import pandas as pd
import numpy as np

import HarveyToolbar_financial as htf

#data handling: importing useful info into price_history nparray
APPL=pd.read_csv('BA.csv')
adjusted_closing_price=APPL["Adj Close"]
SL=len(adjusted_closing_price) #\u days, simulasion length
time_series=list(range(SL))
price_history=np.zeros((2,SL))
price_history[0]=time_series
price_history[1]=adjusted_closing_price

SPH=price_history[:,:1] #simulation price history

Apple=htf.asset("APPL","STOCK",SPH)

#parameters
wb=6 #buying observation window
ws=6 #selling observation window

#simulation

cash=100000

#buy with all cash in the beginning
remaining_cash=Apple.dollar_buy(cash)
cash=remaining_cash

for i in range(1,SL):
    Apple.update(price_history[0,i], price_history[1,i])
    if(i+1<min([wb,ws])):
        #wait
        continue
    
    #wait if not profitable
    if(Apple.cost>Apple.evaluate()):
        #wait
        continue
    
    #sell if stop rising
    if(Apple.stop_rising(ws)==True):
        gross_profit=Apple.sell_all()
        cash+=gross_profit
    
    #buy if stop falling
    if(Apple.stop_falling(wb)==True):
        remaining_cash=Apple.dollar_buy(cash)
        cash=remaining_cash
cash+=Apple.sell_all()
print(cash)
print("\n\n\n")
Apple.print_properties()
Apple.viz()

    
    
    
    
    
    
    
    
    