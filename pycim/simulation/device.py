import numpy as np

from pycim.utils import const

class device:
    def __init__(self):
        ##### Parameters required in the discrete (traveling wave) model
        # light speed m/s
        self.c  = 2.99792458e8  
        # Cavity length noraml: m
        self.L_cavity = 100 
        # Set the loss of the cavity, normal : dB
        self.loss = 10**(-11/10)
        # Set the gain coefficient of the PPLN crystals, normal: W^(-1/2)
        self.kappa = 130 * self.c 
        # Set the length of PPLN crystals, normal : m
        self.L_ppln = 0.05 
        # round trip time
        self.T_rt = self.L_cavity / self.c
        # Travel time in PPLN
        self.tao = self.L_ppln / self.c

        ##### Parameters required in the c-number model
        #Signal light, photon attenuation rate
        self.r_s = 1
        #Pump light, photon attenuation rate
        self.r_p = 10264
        # PPLN crystal gain coefficient
        self.k = 130 
        # Threshold pump amplitude
        self.F_th = (self.r_s*np.sqrt(self.r_p))/(4*self.k)
        self.As = np.sqrt(self.r_s*self.r_p/(2*self.k**2))
        self.g2 = 1/self.As

        ##### Parameters required in meanFiled model
        # Pump light wavelength 780nm
        self.lambda_in = 780e-9
        # Pump light frequency
        self.w1 = const.c / self.lambda_in
        # The coefficients of the coupled wave equation terms
        self.eps = 130  # equal to κ  
        # Refractive index    0.7179
        self.n = self.w1*2*const.deff/(self.eps * const.c)
        # Gain coefficient
        self.G0 = np.e**(2 * self.eps * self.L_ppln * np.sqrt(0.03796) ) ###自定义的  
        # Uncoupled threshold power
        self.b0 = np.log(self.G0)/(2 * self.eps * self.L_ppln)  
        # Saturation parameter
        self.beta = (self.G0-1-np.log(self.G0))/(4*(self.b0**2)*np.log(self.G0)) 
