from matplotlib import pyplot as plt
import numpy as np
from pycim.utils.getIsingEnergy import Ising
from pycim.simulation import setup
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
from functools import singledispatch 
import scipy 
from scipy.integrate import solve_ivp
# The time to first find the optimal solution (discrete model)
@singledispatch 
def getSolutionTime(sol_info: np.ndarray,setup):

    sign_value = np.sign(sol_info[:,:setup.round_number - 1])
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    find_max_time = np.argmax(cut_value)
    return find_max_time
# The time to first find the optimal solution (c-number model)
@getSolutionTime.register 
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):
    c = sol_info.y
    x = sol_info.t
    sign_value = np.sign(c[:,:setup.round_number - 1])
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    find_max_time = np.argmax(cut_value)
    return x[find_max_time]
# Classification configuration of optimal solution (discrete model)
@singledispatch  
def getSolution(sol_info: np.ndarray,setup):
    
    sign_value = np.sign(sol_info[:,:setup.round_number - 1])
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    find_max_time = np.argmax(cut_value)
    opt_sol = sign_value[:,find_max_time]
    return opt_sol
# Classification configuration of optimal solution (c-number model)
@getSolution.register 
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):
    c = sol_info.y
    x = sol_info.t
    sign_value = np.sign(c)
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    find_max_time = np.argmax(cut_value)
    opt_sol = sign_value[find_max_time]
    return opt_sol
# The accuracy of max_cut and based_cut obtained through simulation (discrete model)
@singledispatch   
def getAccuracy(sol_info: np.ndarray,setup,based_cut):

    sign_value = np.sign(sol_info[:,:setup.round_number - 1])
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    max_cut = max(cut_value)
    accuracy = max_cut / based_cut
    return accuracy
# The accuracy of max_cut and based_cut obtained through simulation (c-number model)
@getAccuracy.register
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup,based_cut):
    c = sol_info.y
    x = sol_info.t
    sign_value = np.sign(c[:,:setup.round_number - 1])
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    max_cut = max(cut_value)
    accuracy = max_cut / based_cut
    return accuracy
# The maximum cut value of the optimal solution (discrete model)
@singledispatch   
def getCutValue(sol_info: np.ndarray,setup):
    
    sign_value = np.sign(sol_info[:,:setup.round_number - 1])
    
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    max_cut = max(cut_value)
    return max_cut
# The maximum cut value of the optimal solution (c-number model)
@getCutValue.register
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):
    c = sol_info.y
    x = sol_info.t
    sign_value = np.sign(c[:,:setup.round_number - 1])
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    max_cut = max(cut_value)
    return max_cut
# Draw the evolution diagram of cut-value values (discrete model)
@singledispatch  
def cutvalue_graph(sol_info: np.ndarray,setup):

    t = np.linspace(0,setup.round_number - 1,setup.round_number)
    x = t[:-1]
    sign_value = np.sign(sol_info[:,:setup.round_number - 1])
    ising_energy = Ising(setup.couple_matrix , sign_value)
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    y1 = cut_value
    y2 = ising_energy
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.9)
    par1 = host.twinx()
    offset = 100
    par1.axis["right"].toggle(all=True)
    host.set_xlabel("round number")
    host.set_ylabel("cut value")
    par1.set_ylabel("ising energ")
    p1 = host.plot(x, y1,color = 'blue')
    p2 = par1.plot(x, y2)
    par1.invert_yaxis()
    plt.show()
# Draw the evolution diagram of cut_ralue value (c-number model)
@cutvalue_graph.register
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):
    c = sol_info.y
    x = sol_info.t
    sign_value = np.sign(c[:,:setup.round_number - 1])
    ising_energy = Ising(setup.couple_matrix , sign_value)
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    y1 = cut_value
    y2 = ising_energy
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.9)
    par1 = host.twinx()
    offset = 100
    par1.axis["right"].toggle(all=True)
    host.set_xlabel("round number")
    host.set_ylabel("cut value")
    par1.set_ylabel("ising energ")
    p1 = host.plot(x, y1,color = 'blue')
    p2 = par1.plot(x, y2)
    par1.invert_yaxis()
    plt.show()

# success rate
def getSuccessRate(cut_list,based_cut):

    p = sum(i >= based_cut for i in cut_list)
    SuccessRate = p / len(cut_list)
    return SuccessRate
# average cut
def getAveCutValue(cut_list,step):

    ave_cut = sum(cut_list) / step
    return ave_cut
# # Stable time to find the optimal solution
# def steadSolutionTime(c,setup):

#     sign_value = np.sign(c[:,:setup.round_number - 1])
#     cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
#     MaxCutValueTime = GainDownTime + np.argmax(cut_value[GainDownTime:]) # 稳定找到最大割值的时间点
#     return MaxCutValueTime