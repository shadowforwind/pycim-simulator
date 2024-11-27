import numpy as np
from . import device
from . import setup
from scipy.integrate import solve_ivp
from functools import singledispatch 
import scipy 

# discrete model
@singledispatch
def RK45( u : np.ndarray, t_end , kappa):
    def f(t,u):
        a = u 
        N = int( len(a)/2 )
        b = np.zeros((2*N,))
        # This equation is the coupled wave equation 
        # with a default pump light phase of - π/2 and a signal light phase of 0/π
        b[:N] = kappa * a[N:] * a[:N]   #dEs/dz = kappa * Ap * Es
        b[N:] = - kappa * (a[:N]**2)   # dAp/dz = - kappa * Es²
        return b
    sol_info = solve_ivp(f,[0,t_end],u,method='RK45')
    return sol_info

# c-number model
@RK45.register 
def _( device: device , setup , t_end ):

    J = setup.couple_matrix
    # g2 = device.g2
    N = J.shape[0]
    pump_shcedule = setup.p
    g2 = 5e-3
    # noi_s = noise_size * np.random.randn(N)
    # noi_p = noise_size * np.random.randn(N)
    noi_s = g2 * np.random.choice((-1,1), N)
    noi_p = g2 * np.random.choice((-1,1), N)
    intensity = setup.intensity
    def f(t,u):
        a = u # The first N are in-phase components, and the last N are quadrature components
        b = np.zeros_like(a)
        z = np.dot(a[0:N],J)
        b[:N] = (pump_shcedule(t)-1-((a[:N]**2+a[N:]**2)))*a[:N] + intensity(t) * z \
                + g2 * np.sqrt((a[:N]**2)+(a[N:]**2)+0.5) * noi_s[:]  #dcidt,
        b[N:] = (-pump_shcedule(t)-1-((a[:N]**2+a[N:]**2)))*a[N:] \
            + g2 * np.sqrt((a[:N]**2)+(a[N:]**2)+0.5) * noi_p[:] #dsidt
        return b

    u = np.zeros((2*N,))
    sol_info = solve_ivp(f,[0,t_end],u,method='RK45',first_step=1,t_eval=np.linspace(0,t_end,t_end+1))
    return sol_info

# meanField model
@RK45.register 
def _(t_end : int , device , setup):

    J = setup.couple_matrix
    N = len(J[0])
    pump_shcedule = setup.p
    # g2 = device.g2
    # noi_s = 1e-7 * np.random.randn(N)

    g2 = 1e-5
    noi_s = g2 * np.random.choice((-1,1), N)
    intensity = setup.intensity
    def f(t,u):
        a = u #The first N are in-phase components, and the last N are quadrature components
        b = np.zeros_like(a)
        z = np.dot(a[0:N],J)
        b[:] = ( pump_shcedule(t)-1 - (a[:]**2) ) * a[:] + intensity(t) * z 
        return b

    u = np.array(np.random.uniform(-g2,g2,size=N),dtype=np.float64)
    sol_info = solve_ivp(f,[0,t_end],u,method='RK45',first_step=1,t_eval=np.linspace(0,t_end,t_end+1))
    return sol_info

def RK4():
    return 
def eulerMethod():
    return