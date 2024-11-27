from matplotlib import pyplot as plt
import numpy as np
# from utils.getIsingEnergy import Ising
from pycim.simulation import setup
from functools import singledispatch 
import scipy 
from scipy.integrate import solve_ivp
# Calculate Ising energy
def Ising(J, sign_value):
    col,row = J.shape
    e = 0
    for c in range(col):
        for r in range(row):
            e += - 0.5*J[c][r]*sign_value[c]*sign_value[r]
    return e
# Fork time point
# def findfenchatime(sol,x):
#     for ti in range(0,len(x)):
#         if(abs(sol[0][ti]) > abs((0.1*sol[0][-1]))):
#             return x[ti]
  
#Reverse search aims to find the time point at which 
# max-cut_malue is reached in steady state (discrete model)
def findSteadyTime(c,setup):

    x = np.linspace(0,setup.round_number - 1,setup.round_number)
    sign_value = np.sign(c[:,:setup.round_number - 1])
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    for ti in range(len(cut_value)-1,-1,-1):
        if(cut_value[ti] < max(cut_value)):
            return x[ti+1]
# Return the minimum Ising energy (discrete model) 
@singledispatch   
def getMinEnergy(sol_info: np.ndarray,setup):

    sign_value = np.sign(sol_info[:,:setup.round_number - 1])
    ising_energy = Ising(setup.couple_matrix , sign_value)
    mim_IsingEnergy = min(ising_energy)
    return mim_IsingEnergy
# Return the minimum Ising energy (c-number model) 
@getMinEnergy.register 
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):
    c = sol_info.y
    sign_value = np.sign(c[:,:setup.round_number - 1])
    ising_energy = Ising(setup.couple_matrix , sign_value)
    mim_IsingEnergy = min(ising_energy)
    return mim_IsingEnergy
# The first time to find the minimum Ising energy (discrete model)
@singledispatch 
def getMinEnergyTime(sol_info: np.ndarray,setup):
    
    sign_value = np.sign(sol_info[:,:setup.round_number - 1])
    ising_energy = Ising(setup.couple_matrix , sign_value)
    mim_IsingEnergy_time = np.argmin(ising_energy)
    return mim_IsingEnergy_time
# The first time to find the minimum Ising energy (c-number model)
@getMinEnergyTime.register 
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):
    c = sol_info.y
    x = sol_info.t
    sign_value = np.sign(c[:,:setup.round_number - 1])
    ising_energy = Ising(setup.couple_matrix , sign_value)
    mim_IsingEnergy_time = np.argmin(ising_energy)
    return x[mim_IsingEnergy_time]
# Find the bifurcation time point in this model, assuming that the saturation 
# and bifurcation time points are the same (discrete model) 
# Note: This method is only available under gradual pump settings, 
# and other schemes may obtain incorrect values 
@singledispatch   
def findSaturationTime(Gain: np.ndarray,setup):
    Gain = Gain[0]
    x = np.linspace(0,setup.round_number - 1,setup.round_number)
    for ti in range(1,len(x)-1):
        if(Gain[ti] - Gain[ti-1] < 0 ):
            return int(x[ti])
# Find the bifurcation time point in this model, assuming that the saturation 
# and bifurcation time points are the same (c-number model) 
# Note: This method is only available under gradual pump settings, 
# and other schemes may obtain incorrect values    
@findSaturationTime.register 
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):
    sol = sol_info.y
    x = sol_info.t
    for ti in range(0,len(x)):
        if(abs(sol[0][ti]) > abs((0.1*sol[0][-1]))):
            return x[ti]
        
# OPO amplitude at saturation (discrete model)
def getSaturationAmplitude(Gain,sol_info,setup):

    SaturationTime = findSaturationTime(Gain,setup)
    SaturationAmplitude = abs(sol_info[0][int(SaturationTime)])
    return SaturationAmplitude
# Pump power at saturation (discrete model)
def getSaturationPower(Gain,setup):

    SaturationTime = findSaturationTime(Gain,setup)
    SaturationPower = setup.pump_schedule[int(SaturationTime)]
    return SaturationPower
# Draw the evolution diagram of OPO in-phase component (discrete model)
@singledispatch 
def inPhase_graph(sol_info: np.ndarray,setup):

    N = len(sol_info[0:])
    round_number = setup.round_number
    t = np.linspace(0,round_number - 1,round_number)
    for i in range(N):
        plt.plot(t,sol_info[i,:],label=f"{i+1}")
    plt.legend(loc="upper left",ncol=2)
    plt.xlabel('round number')
    plt.ylabel('in-phase amplitude')
    plt.show()
# Draw the evolution diagram of OPO in-phase component (c-number model)
@inPhase_graph.register 
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):

    sol = sol_info.y
    x = sol_info.t
    a_sat = abs(sol[:,-1])#The amplitude at saturation, used for normalization
    N = len(setup.couple_matrix[0])
    for i in range(0,N):
        plt.plot(x, sol[i,:]/a_sat[i],label=f"{i+1}")
    plt.legend(loc="upper left",ncol=2)
    plt.xlabel('round  number')
    plt.ylabel('in-phase amplitude')
    plt.show()
# Draw the evolution diagram of Ising energy (discrete model)
@singledispatch 
def energy_graph(sol_info: np.ndarray,setup):

    t = np.linspace(0,setup.round_number - 1,setup.round_number)
    x = t[:-1]
    sign_value = np.sign(sol_info[:,:setup.round_number - 1])
    ising_energy = Ising(setup.couple_matrix , sign_value)
    plt.plot(x,ising_energy)
    plt.xlabel('round number')
    plt.ylabel('Ising energy')
    plt.show()

# Draw the evolution diagram of Ising energy (c-number model)
@energy_graph.register
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):
    
    x = sol_info.t
    c = sol_info.y
    sign_value = np.sign(c)
    ising_energy = Ising(setup.couple_matrix , sign_value)
    plt.plot(x,ising_energy)
    plt.xlabel('round number')
    plt.ylabel('Ising energy')
    plt.show()
    
# Draw the evolution diagram of gain (discrete model)
def gain_graph(gain,setup):
    sqrt_G_I = gain
    t = np.linspace(0,setup.round_number - 1,setup.round_number)
    plt.plot( t[:-1] , 10*np.log10((sqrt_G_I[0][:-1]**2)) )
    plt.xlabel('round number')
    plt.ylabel('gain(dB)')
    plt.show()
    return

