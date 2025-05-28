import numpy as np
from ..utils import Ising


def bias_for_aux_spin(couple_mat, h_vector, N_aux=1):
    assert (
        len(h_vector) == couple_mat.shape[0]
    ), "h_vector length must match the number of rows in couple_mat"
    N = len(h_vector)
    H_mat = np.zeros((N, N_aux))
    H_mat[:, :] = h_vector[:, np.newaxis] / N_aux
    top = np.hstack([couple_mat, H_mat])
    F_mat = np.ones((N_aux, N_aux)) - np.eye(N_aux)
    bottom = np.hstack([H_mat.T, F_mat])
    combined_matrix = np.vstack([top, bottom])
    return combined_matrix


def get_offset(N_aux):
    assert N_aux > 0, "N_aux must be a positive integer"
    return -(N_aux - 1) * N_aux / 2


def min_energy_for_aux_spin(sol_info: np.ndarray, setup, N_aux):
    c = sol_info.y
    N = setup.couple_matrix.shape[0]
    sign_value = np.sign(c[:N, :])
    ising_energy = Ising(setup.couple_matrix, sign_value)
    mim_IsingEnergy = min(ising_energy)
    return mim_IsingEnergy - get_offset(N_aux)


def bias_for_non_aux_spin(couple_mat, h_vector):
    assert (
        len(h_vector) == couple_mat.shape[0]
    ), "h_vector length must match the number of rows in couple_mat"
    np.fill_diagonal(couple_mat, h_vector)
    return couple_mat
