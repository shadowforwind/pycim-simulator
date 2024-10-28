##########Define some constants used here
import numpy as np
global c 
global deff
global eps0
c = 2.99792458e8  # light speed m/s
deff = 28e-12  # Quadratic nonlinear coefficient 单位m/V
eps0 = 8.854187817e-12  # Vacuum dielectric constant F/m
h_bar = 1.05457266e-34  # Reduced Planck constant J·s

# Variable parameters, if they are variables, they can be deleted
global n1
global n2
n1 = 2  # Refractive index
n2 = 2  # Refractive index

# Define coefficient matrix
def matrix_J(N):
    J=np.ones((N,N))
    for i in range(0,N):
        J[i][i]=0   
    return J  