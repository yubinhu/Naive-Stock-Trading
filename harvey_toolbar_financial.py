# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 13:10:45 2019

@author: yubin
"""

import numpy as np
print("test 1")
def test(a,b,c):
    a=0
    b=[0,0]
    c="0"
    return a,b,c

i=10
j=np.array([2,2])
k="test"

print(test(i,j,k))
print(i,j,k)


print("\n\n\n\n")
print("test 2")
w=np.zeros((2,2))
w[:]=2
print(w)