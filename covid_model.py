# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 20:33:10 2020

@author: lando
"""


import numpy as np

# healthy, presymptomatic, asymptomatic, sick, recovered, dead
trans = np.ndarray((6,6),dtype=float)
X = np.ndarray((6,),dtype=float)

X[0] = 8000000000; X[1] = 2; X[2]=0; X[3]=0; X[4]=0; X[5]=0
HEALTHY,PRE,A,SICK,REC,DEAD = (0,1,2,3,4,5)
#trans[0,0]  1 - sum(trans[1:6])
trans[0,1]=0;trans[0,2]=0;trans[0,3]=0;trans[0,4]=0;trans[0,5]=0; #healthy is an unrecoverable status
#trans[1,0]  proportional to the product of sick and healthy people
trans[1,1] = 5./6. # presymptomatics take six days to show symptoms
trans[1,2] = 0; trans[1,3] = 0; trans[1,4] = 0; trans[1,5] = 0 # You cannot be presymptomatic a second time
#trans[2,0]  proportional to the product of sick and healthy people
trans[2,1]=0;trans[2,2]=1;trans[2,3]=0;trans[2,4]=0;trans[2,5]=0 # Once you are asymptomatic, you stay asymptomatic
trans[3,0] = 0 # you must be presymptomatic before you can be sick
trans[3,1] = 1./6. # it take 6 days to show symptoms
trans[3,2] = 0; trans[3,3] = 20/21; trans[3,4] = 0; trans[3,5] = 0; # once you are sick, you cannot be sick again
trans[4,0] = 0; trans[4,1] = 0; trans[4,2] = 0
trans[4,3] = .98/21 # 98 percent of people recover after three weeks
trans[4,4] = 1 # once recovered, always recovered
trans[4,5] = 0;
trans[5,0] = 0; trans[5,1] = 0; trans[5,2] = 0; trans[5,3] = .02/21 # 2% of cases die within 21 days
trans[5,4] = 0; trans[5,5] = 1

#We will assume 20% of infected people are asymptomatic
#We also assume presymptomatic people come into contact with 20 people a day
#and spread the virus to 10% of those people they come into contact with
#but the more infected people there are, the less possible transmissions
#so the transition coefficients should look something like this
coef = .1
trans[PRE,HEALTHY] = coef*.8*(X[PRE]/sum(X[:-1]))
trans[A,HEALTHY]   = coef*.2*(X[PRE]/sum(X[:-1]))
trans[HEALTHY,HEALTHY] = 1-sum(trans[1:,HEALTHY])

vector = X
q = ''
day = 0
while (q!='q'):
    vector = trans.dot(vector)
    trans[PRE,HEALTHY] = coef*.8*(vector[PRE]+vector[SICK])/sum(vector[:-1])
    trans[A,HEALTHY]   = coef*.2*(vector[PRE]+vector[SICK])/sum(vector[:-1])
    trans[HEALTHY,HEALTHY] = 1-sum(trans[1:,HEALTHY])
    line = f'Day {day}: '
    for i in vector:
        line = line + str(int(i))+','
    print(line)
    q = input()
    day += 1