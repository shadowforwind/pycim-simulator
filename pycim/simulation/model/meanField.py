from .. import solver


def RK45meanField(phyInput, applInput):

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

    sol_info = solver.RK45(t_end, phyInput, applInput)

    return sol_info
