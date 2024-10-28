import random
from scipy.integrate import solve_ivp
import numpy as np
import sys
from .. import device
from .. import setup
from .. import solver
from ...utils import const
from ...utils.file_J import read_J
from ...utils.getIsingEnergy import Ising

def RK45meanFiled(phyInput , applInput):

    # Physical layer input
    # PPLN length： m
    L_ppln = phyInput.L_ppln 
    # Pump light wavelength： m
    lambda_in = phyInput.lambda_in

    # Application layer input
    intensity = applInput.intensity
    round_number = applInput.round_number
    J = applInput.couple_matrix

    N = J.shape[0]
    t_end = round_number

    sol_info = solver.RK45(t_end , phyInput , applInput)

    return sol_info