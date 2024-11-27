import numpy as np

from pycim import sampler
from .model.meanField import RK45meanField
from .model.c_number import RK45c_number
from .model.discrete import RK45Discrete
def singleSimulation(  device , setup , model = "discrete" , solver = "RK45" ):
    if( model == "discrete"):
        if(solver == "RK45"):
            # What is returned here are the in-phase component c and the gain np. sqrt (gain)
            sol_info = RK45Discrete(device , setup)
            return sol_info
        
    if( model == "c-number"):
        if(solver == "RK45"):
            # What is returned here is the in-phase component c
            sol_info = RK45c_number(device , setup)
            return sol_info
        
    if( model == "meanField"):
        if(solver == "RK45"):
            # What is returned here is the in-phase component c
            sol_info = RK45meanField(device , setup)
            return sol_info


# Run multiple times and return a list of cut values
def multiSimulation(  device , setup , step = 100,model = "discrete" , solver = "RK45" , ):

    if( model == "discrete"):
        if(solver == "RK45"):
            cut_list = np.zeros(step,)
            for i in range(step):
                sol_info = singleSimulation(device , setup , model = "discrete" , solver = "RK45" )
                cut = sampler.getCutValue(sol_info[0] , setup)
                cut_list[i] = cut
        return cut_list
    
    if( model == "c-number"):
        if(solver == "RK45"):
            cut_list = np.zeros(step,)
            for i in range(step):
                sol_info = singleSimulation(device , setup , model = "c-number" , solver = "RK45" )
                cut = sampler.getCutValue(sol_info.y , setup)
                cut_list[i] = cut
        return cut_list
    
    if( model == "meanField"):
        if(solver == "RK45"):
            cut_list = np.zeros(step,)
            for i in range(step):
                sol_info = singleSimulation(device , setup , model = "meanField" , solver = "RK45" )
                cut = sampler.getCutValue(sol_info.y , setup)
                cut_list[i] = cut
        return cut_list