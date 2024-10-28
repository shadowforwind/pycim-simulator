# Calculate Ising energy
def Ising(J, sign_value):
    col,row = J.shape
    e = 0
    for c in range(col):
        for r in range(row):
            e += - 0.5*J[c][r]*sign_value[c]*sign_value[r]
    return e