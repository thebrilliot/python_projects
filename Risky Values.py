# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 12:12:14 2020

@author: lando
"""

def e(c1,c2,p):
    return c1*p+c2*(1-p)

def five_to_one(c,p):
    value = e(5,c,p)
    lower = 0
    upper = 1
    guess = 0.5
    guess_value = e(1,c,guess)
    diff = guess_value-value
    while (abs(diff) > .00001):
        if diff > 0: # If the guess is greater than the actual expected value, add more weight to the smaller value (raise the lower bound to increase p)
            lower = guess
        else:
            upper = guess
        guess = (upper + lower)/2
        guess_value = e(1,c,guess)
        diff = guess_value-value
        # print(value, guess_value, diff)
        # input()
    return guess

def risky_values(c1,c2,p):
    value = e(c1,c2,p)
    li = []
    for i in range(10):
        new_p = i/10
        new_c = value - c1*new_p/(1-new_p)
        li.append(new_c)
    return li

risky_values(5,10,.9)
e(5,10,.9)
five_to_one(10,.9)
risky_values(1,10.,.5)