# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 12:22:17 2019

@author: yubin
"""

import pandas as pd
import numpy as np

portfolio=np.zeros((2,10))  #first row is share number, second row is buy-in-price

#data handling

APPL=pd.read_csv('AAPL.csv')

price_history=APPL["Adj Close"]

#naive procedure
def Naive_procedure(portfolio,available_fund,current_price,buying_stepsize):
    
    #zero: pre-check the empty entry position in the portfolio
    ep=11 #empty position
    for i in range(10):
        if(portfolio[0][i]==0):
            ep=i
            break
        else:
            continue
    
    #first: calculate total cost of current portfolio
    cost=0
    tsn=0   #total share number
    
    Nportfolio=np.copy(portfolio)
    Navailable_fund=available_fund
    
    
    
    for i in range(10):
        sn=portfolio[0][i]
        bip=portfolio[1][i]
        cost+=sn*bip
        tsn+=sn
    #second: calculate effective buy in price
    effective_buy_in_price=cost/tsn
        
    #thrid: compare effective buy in price and current price
    if(current_price>effective_buy_in_price):
        #sell
        Nportfolio[:]=0
        Navailable_fund+=tsn*current_price
        
        
    elif(current_price<=effective_buy_in_price):
        #buy
        
        #   check if you are out of money
        if(available_fund<=0):
            #wait and see
            return Nportfolio,Navailable_fund
        
        #   check if you are out of empty entries
        if(ep==11):
            #wait and see
            return Nportfolio,Navailable_fund
        
        #   if you can buy
        #       conduct buy in
        bisn=int(buying_stepsize/current_price) #buy in share number
        Nportfolio[0][ep]=bisn
        Nportfolio[1][ep]=current_price
        Navailable_fund-=bisn*current_price        
    else:
        #not reachable
        raise ERROR
    
    #forth: return
    return Nportfolio,Navailable_fund

"""
#test
portfolio[0][0]=5
portfolio[1][0]=5

print(Naive_procedure(portfolio,225,6,25))
"""

def BuyIn_triger(past_10day_prices,current_price):
    #naive buy in strategy
    
    
    
    if(past_10day_prices[-1]<past_10day_prices[-2]):
        return True
    else:
        return False
    
tdp=np.zeros((10)) #ten day price

SL=len(price_history) #simulation length

portfolio[0][0]=650
portfolio[1][0]=price_history[0]
fund=10**6-portfolio[0][0]*portfolio[1][0]

sharenumber_history=[]

for i in range(SL):
    
    cp=price_history[i] #current price
    tdp=np.roll(tdp,-1)
    tdp[-1]=cp
    if(portfolio[0][0]!=0):
        portfolio,fund=Naive_procedure(portfolio, fund, cp, 10**5)
    if(portfolio[0][0]==0 and BuyIn_triger(tdp, cp)==True):
        #buy in
        bisn=int(10**5/cp) #buy in share number
        portfolio[0][0]=bisn
        portfolio[1][0]=cp
        fund-=bisn*cp
    tsn=0   #total share number
    for i in range(10):
        sn=portfolio[0][i]
        tsn+=sn
    sharenumber_history.append(tsn)
    
    
#calculate ending value
tsn=0   #total share number
for i in range(10):
    sn=portfolio[0][i]
    tsn+=sn
ending_value=tsn*cp+fund
#print("ending value:",ending_value)
print("profit rate:",ending_value/10**6*100,"%")
    
"""
right now it's a loosing strategy
need to change buyin triger and naive procedure
could include trend, if an upward trend turns down then sell,
if a downward trend turns up then buy

this was my strategy when playing monopoly on Peiyufei's cell phone with Yanghaichuan
"""
    

#visualization
    
import matplotlib.pyplot as plt

for i in range(len(sharenumber_history)):
    sharenumber_history[i]=sharenumber_history[i]/15

plt.plot(list(price_history))
plt.bar(range(len(sharenumber_history)),sharenumber_history,color='red',width=1)
plt.ylabel("price")
plt.xlabel("day")
plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    