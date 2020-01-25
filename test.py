# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 13:10:45 2019

@author: yubin
"""

import numpy as np

class asset:
    __slots__=["name","category","quantity","cost","current_price","current_time",
               "operation_logs","price_history"]
    # operation_log is a list of logs, each of which are lists of numbers, 
    # representing three pieces of information of every operation in this asset: 
    # Time, Buy In Amount (negative if selling), and Price at the Time. 
    
    # price_history is a np.array of two rows, first one is time, second one is 
    # the price at 
    
    def __init__(self, name, category, price_history):
        self.name=name
        self.category=category
        self.price_history=price_history
        self.quantity=0
        self.cost=0
        self.current_price=price_history[1][-1]
        self.current_time=price_history[0][-1]
        self.operation_logs=[]
    
    def update(self,current_time,current_price): #update price history and current price and current time
        
        #update current_time and current_price
        self.current_price=current_price
        self.current_time=current_time
        
        #check if need to update price_history
        i=self.price_history[0,-1]
        j=current_time
        
        k=self.price_history[1,-1]
        w=current_price
        if(i!=j or k!=w):
            self.price_history=np.append(self.price_history,[[current_time],[current_price]],axis=1)
            return True
        else:
            return False
    
    def dollar_buy(self,available_fund): #buy the maximum amount with available fund
        
        #calculate the monetory cost and amount to buy in this operation
        n=int(available_fund/self.current_price) #buy in amount
        c=n*self.current_price #cost of this buy in operation
        residual_fund=available_fund-c
        
        #change the asset properties
        self.cost+=c
        self.quantity+=n
        
        #update the operation log
        log=[self.current_time,n,self.current_price]
        self.operation_logs.append(log)
        
        #check if need to update price_history
        asset.update(self,self.current_time,self.current_price)   

        return residual_fund
    
    def sell_all(self): #buy the maximum amount with available fund
        
        #calculate the net worth of the asset at current price
        net_worth=self.current_price*self.quantity
        
        #update the operation log
        log=[self.current_time,-self.quantity,self.current_price]
        self.operation_logs.append(log)
        
        #change the asset properties
        self.cost=0
        self.quantity=0
        
        #check if need to update price_history
        asset.update(self,self.current_time,self.current_price)              
        return net_worth
    
    def print_properties(self):
        print("Asset:",self.name)
        print("operation logs:",self.operation_logs)
        print("price history:")
        print(self.price_history)
        print("quantity:",self.quantity)
        print("cost:",self.cost)
        print("value:",self.evaluate())
        print("\n\n\n")
        return True
    
    def evaluate(self):
        value=self.current_price*self.quantity
        return value
    
    def stop_rising(self,w): #w is observation window
        
        margin=0 #threshold for considering it as rising price
        
        if(w<3):
            raise Exception("Cannot descide stop-rising if window is less than 3")
        
        flag=True 
        
        if(len(self.price_history[1])<w):
            flag=False
            return flag
        
        for i in range(2,w):
            if(self.price_history[1,-i]<self.price_history[1,-(i+1)]+margin):
                flag=False
            else:
                continue
        
        if(self.price_history[1,-1]+margin>self.price_history[1,-2]):
            flag=False
        
        return flag
        
        
    
    def stop_falling(self,w): #w is observation window
        
        margin=0
        
        if(w<3):
            raise Exception("Cannot descide stop-falling if window is less than 3")
        
        flag=True 
        
        if(len(self.price_history[1])<w):
            flag=False
            return flag
        
        for i in range(2,w):
            if(self.price_history[1,-i]+margin>self.price_history[1,-(i+1)]):
                flag=False
            else:
                continue
        
        if(self.price_history[1,-1]<self.price_history[1,-2]+margin):
            flag=False
        
        return flag
    
    def viz(self): #visualization
        position=0
        pl=[] #position list
        pointer=0
        l=len(self.operation_logs)-1 #last index of logs
        for i in range(len(self.price_history[0])):
            if(self.operation_logs[pointer][0]==i):
                position+=self.operation_logs[pointer][1]
                if(pointer<l):
                    pointer+=1
            pl.append(position)
            continue
        
        import matplotlib.pyplot as plt
        
        plt.plot(list(self.price_history[1]))
        plt.bar(range(len(pl)),pl,color='red',width=1)
        plt.ylabel("price/position")
        plt.xlabel("day")
        plt.show()
    
    
        

ph=np.array([[0],[253]])
Apple=asset("APPL","STOCK",ph)

Apple.update(1,254)
fund=100000
b=fund/2
fund=fund-b+Apple.dollar_buy(b)
print(fund)
Apple.print_properties()

Apple.update(2,255)
fund=fund-b+Apple.dollar_buy(b)
print(fund)
Apple.print_properties()

Apple.update(3,253)
fund+=Apple.sell_all()
print(fund)
Apple.print_properties()

Apple.viz()
















