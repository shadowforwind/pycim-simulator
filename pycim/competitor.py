import random
import numpy as np
from pycim.utils.getIsingEnergy import Ising
from matplotlib import pyplot as plt
import numpy as np
from pycim.utils.getIsingEnergy import Ising
from pycim.simulation import setup
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
from functools import singledispatch 
import scipy 
from scipy.integrate import solve_ivp
def e_J(J):
    return np.sqrt(np.sum(J * J))
def esing(J, s):
    col,row = J.shape
    e = 0
    for c in range(col):
        for r in range(row):
            e = e - 0.5*J[c][r]*s[0][c]*s[0][r]
    return e
#P (i) is a (t), which increases from 0 to 1 after going through steps
def p(s:int):
    return s*0.005
def dsb(J):
    size = J.shape[0]
    det_t = 0.5  # time step 
    step = 200 # Evolution steps of KPO
    det = 1 # a0 Positive constant
    ksi0 = 0.5 * np.sqrt(size - 1) / e_J(J)  # c0 Positive constant defined based on random matrix theory
    # a0 c0 all can be parameters to be optimized.
    x = np.zeros([1,size],dtype=np.float64)
    y = np.array(np.random.uniform(-0.1,0.1,size=(1,x.size)),dtype=np.float64)
    for i in range(step+1):
        y = y + det_t * (ksi0 * np.dot(np.sign(x),J) -(det - p(i)) * x)
        x = x + det * det_t * y
        y = np.where(np.abs(x) > 1, 0, y)
        x = np.where(np.abs(x) > 1, np.sign(x), x)
    return np.sign(x)

# Simulated Annealing Algorithm
## Refer to 《Massively Simulating Adiabatic Bifurcations with FPGA to Solve Combinatorial Optimization》
def SA(J):

    size = J.shape[0]
    T = 1000 # initial temperature 
    r = 0.99 # step
    T_min = 0.001 # Final temperature
    s = np.ones([1,size],dtype=np.int32) # Initial state all 1, initial spin all 1
    i=0
    while(T > T_min):
        select_num = random.randint(0,size-1) # Randomly select an integer between 0 and size-1
        dE = 2 * s[0][select_num] * np.sum(J[select_num] * s[0]) # △E The energy change caused by flipping a spin
        if(np.exp( -(dE/T) ) > random.uniform( 0 , 1 )): # Add noise based on temperature to break out of the local minimum Metropolis rule: accept new states with probability
            #Flip s
            s[0][select_num] = -s[0][select_num]
        else:
            pass
        T = r * T
        i += 1
    cut_value = -0.5*esing(J, s)-0.25*np.sum(J)

    return cut_value
# Simulated bifurcation algorithm
## Refer to《High-performance combinatorial optimization based on classical mechanics》
def SB(J,step):

    i=0
    max_cut_value_sb=0
    while(i<step):
        s = dsb(J)
        if( (-0.5*esing(J, s)-0.25*np.sum(J)) > max_cut_value_sb):
            max_cut_value_sb = -0.5*esing(J, s)-0.25*np.sum(J)
        i+=1
    # print("s:",s)#The spin configuration of the solution is this matrix
    return max_cut_value_sb
# Fixed Greedy Algorithm with Polynomial Time Complexity
def SG(J):
    J = -J
    def weight_all(i,S):
        weight = 0
        for j in S:
            weight += J[i][j]
        return weight
    cut_value = float('-inf')
    N = len(J[0])
    V_ = np.linspace(0,N-1,N) # V`=V
    # Find the edge with the highest weight in J
    max_weight = J[0][1]
    row=0
    col=1
    for r in range(0,N-1):
        for c in range(r+1,N):
            if(J[r][c] > max_weight):
                max_weight = J[r][c]
                row=r
                col=c
    cut_value = max_weight
    V_ = np.delete(V_,np.where(V_ == row))
    V_ = np.delete(V_,np.where(V_ == col))
    S1 = np.array([row])
    S2 = np.array([col])
    score = [float('-inf')]*N

    for j in range(1,N-1):

        for i in V_:
            i = int(i)
            score[i] = max(weight_all(i,S1),weight_all(i,S2))
        i_ = score.index(max(score))

        if(weight_all(i_,S1) > weight_all(i_,S2)):
            S2 = np.append(S2,i_)
        else:
            S1 = np.append(S1,i_)

        V_ = np.delete(V_,np.where(V_ == i_))
        score[i_] = float("-inf")
        cut_value = cut_value + max(weight_all(i_,S1),weight_all(i_,S2))

    return cut_value
# Heuristic algorithm that can guarantee at least xx approximation ratio
def GW_SDP():
    return