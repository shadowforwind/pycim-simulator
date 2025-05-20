# Refer to《Coherent Ising machine based on degenerate optical parametric oscillators》
# 《A fully programmable 100-spin coherent Ising machine with all-to-all connections》
# 《A coherent Ising machine for 2000-node optimization problems》
import numpy as np
from .. import solver


def RK45c_number(device, setup):

    # Physical layer input
    r_s = device.r_s
    r_p = device.r_p
    k = device.k
    As = np.sqrt(r_s * r_p / (2 * k**2))

    # Application layer input
    intensity = setup.intensity
    round_number = setup.round_number
    J = setup.couple_matrix
    N = J.shape[0]

    t_end = round_number

    sol_info = solver.RK45(device, setup, t_end)

    return sol_info
