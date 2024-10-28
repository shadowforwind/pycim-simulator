import numpy as np

class setup:
    
    def __init__(self):
        
        def pump_schedule(t):
            return np.sqrt( (1/760) * t )
        
        # Set the couple matrix
        # self.couple_matrix = - np.array([
        #         [0, 1, 0, 1, 1, 0, 0, 1, 1, 0],
        #         [1, 0, 1, 0, 0, 1, 1, 1, 0, 0],
        #         [0, 1, 0, 1, 1, 0, 0, 0, 1, 0],
        #         [1, 0, 1, 0, 0, 1, 1, 0 ,1, 0],
        #         [1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
        #         [0, 1, 0, 1, 1, 0, 0, 0, 1, 1],
        #         [0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        #         [1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
        #         [1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
        #         [0, 0, 0, 0, 1, 1, 1, 0, 1, 0]])
        # The number of OPOs in the cavity
        self.N = 10
        # # Set the couple matrix
        self.couple_matrix = - np.zeros((self.N,self.N))
        # Round trip number
        self.round_number = 1500
        # Set the coupling intensity
        self.intensity = 0.03 * np.ones(self.round_number,)
        # Set the pump of the CIM system, normal:W
        self.pump_schedule = np.sqrt( 5e-5 * np.linspace(1,self.round_number,self.round_number) )
        # Normalized pump power for c-number and meanFiled models
        self.p = pump_schedule
        