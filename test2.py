# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 13:09:13 2020

@author: yubin
"""

import numpy as np

import matplotlib.pyplot as plt
        
pl=[1,2,3,4]

plt.bar(range(len(pl)),pl,color='red',width=1)
plt.ylabel("price/position")
plt.xlabel("day")
plt.show()