## Refer to《Traveling-wave model of coherent Ising machine based on fiber loop with
## pulse-pumped phase-sensitive amplifier》

import numpy as np
from .. import device
from .. import setup
from .. import solver
from ...utils import const
from ...utils.file_J import read_J
from ...utils.getIsingEnergy import Ising

def RK45Discrete(device , setup):
    
    # Physical layer input
    L = device.L_ppln
    eta = device.loss
    kappa = device.kappa
    tao = device.tao
    t_end = 1 * tao # Travel time in PSA

    # Application layer input
    J = setup.couple_matrix
    N = J.shape[0]
    lunshu = setup.round_number
    intensity = setup.intensity
    init_Ep = setup.pump_schedule
    
    # Return parameters
    gain = np.zeros((N,lunshu)) # Used to represent the gain obtained throughout the entire process of a round (including losses, coupling, and noise effects)响）
    c = np.zeros((N,lunshu)) # The in-phase component, Es is c

    # Temporary parameters
    sign_value = np.zeros((N,lunshu-1)) # Sign value of in-phase component
    sqrt_G_I = np.zeros((N,lunshu)) # Gain of in-phase component
    N_I = np.zeros((N,lunshu)) # Noise of in-phase component
    noise_size = 2e-6  # The magnitude of noise level

    # The default signal light phase here is 0/π
    N_I[:N,0] = noise_size * np.random.normal(0, 0.5, N) # The initial value comes from vacuum fluctuations
    u = np.zeros(2*N,) # 0~N-1 are Es, and the last N are Ep
    c[0:N,0] = N_I[0:N,0]

    
    for k in range(0,lunshu-1): 
        u[0:N] = c[0:N,k]
        u[N:2*N] = init_Ep[k]
        sol_info = solver.RK45(u,t_end,kappa)
        if(sol_info.success == False):
            print("False!")
        Es = sol_info.y[0:N]
        
        ################## Debug processing after the occurrence of gain 0 in the discrete model####################
        for i in range(len(Es[:N,-1])):
            if(Es[i,-1] == 0):
                tmp_sign = np.sign(Es[i,0])
                Es[i,-1] = tmp_sign * noise_size * abs( np.random.normal(0, 0.5, 1) )
        ##################                                          ####################        
        
        sqrt_G_I[:N,k] = Es[:N,-1] / Es[:N,0]  # The gain obtained by PSA for the in-phase component in this round
        
        ################## Debug processing after the occurrence of gain 0 in the discrete model####################
        for i in range(len(sqrt_G_I[:N,k])):
            if(sqrt_G_I[i,k] == 0):
                sqrt_G_I[i,k] = sqrt_G_I[i,k-1]
        ##################                                          #################### 
        
        N_I[:N,k] = noise_size * np.random.normal(0, 1, N) * np.sqrt(0.25*(2-eta)*(sqrt_G_I[:N,k]**2))
        c[:N,k+1] = sqrt_G_I[:N,k] * np.sqrt(eta) * c[:N,k] \
            + sqrt_G_I[:N,k] * intensity[k] * np.dot(c[:,k],J) + N_I[0:N,k]
        gain[:N,k] = c[:N,k+1] / c[:N,k]
    return c,sqrt_G_I

def RK4Discrete(device , setup):

    return 

def eulerDiscrete(device , setup):
    
    return 