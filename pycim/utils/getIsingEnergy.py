# Calculate Ising energy
import numpy as np


def Ising(J, sign_value):
    diag = np.diag(J)
    col, row = J.shape
    e = 0
    for c in range(col):
        for r in range(c + 1, row):
            e += -J[c][r] * sign_value[c] * sign_value[r]
    return e - np.dot(diag, sign_value)
