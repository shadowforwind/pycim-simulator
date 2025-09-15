import numpy as np
import optuna
from scipy.integrate import solve_ivp
from ..utils import Ising


def get_optimized_fixed_pump(couple_matrix, eta):
    """
    Aim to provide the optimal static pump intensity value
    under the corresponding couple_matrix and eta

    Args:
        couple_matrix: couple matrix
        eta: static couple intensity value
    """

    def qiujie(J, fixed_pump, eta, t_end):
        N = J.shape[0]

        def p(t):
            return fixed_pump

        def f(t, u):
            z = np.dot(u, J)
            I = eta * z
            du = ((p(t) - 1) - (u**2)) * u + I
            return du

        u_init = np.random.uniform(-1e-4, 1e-4, size=N).astype(np.float64)
        sol = solve_ivp(
            f,
            [0, t_end],
            u_init,
            method='RK45',
            t_eval=np.arange(0, t_end + 1),
            first_step=1,
        )
        return sol

    def cim_envolve(J, fixed_pump, eta, t_end, iteration):
        N = J.shape[0]
        sum_ising_energy = 0
        for _ in range(iteration):
            sol_info = qiujie(J, fixed_pump, eta, t_end)
            sol = sol_info.y
            sign_value = np.sign(sol[0:N, -1])
            ising_energy = Ising(J, sign_value)
            sum_ising_energy += ising_energy
        ave_ising_energy = sum_ising_energy / iteration
        return ave_ising_energy

    def objective(trial, couple_matrix, eta):
        iteration = 20
        fixed_pump = trial.suggest_float("fixed_pump", 0.1, 1.5, step=0.1, log=False)
        t_end = int(100 / fixed_pump)
        ave_ising_energy = cim_envolve(couple_matrix, fixed_pump, eta, t_end, iteration)
        return ave_ising_energy

    optuna.logging.set_verbosity(optuna.logging.ERROR)
    study = optuna.create_study()
    study.optimize(lambda trial: objective(trial, couple_matrix, eta), n_trials=20)
    return study.best_params['fixed_pump']


def get_optimized_eta(couple_matrix, fixed_pump):
    """
    Aim to provide the optimal static couple intensity value
    under the corresponding couple_matrix and fixed pump
    Args:
        couple_matrix: couple matrix
        fixed_pump: fixed pump intensity value
    """

    def qiujie(J, fixed_pump, eta, t_end):
        N = J.shape[0]

        def p(t):
            return fixed_pump

        def f(t, u):
            z = np.dot(u, J)
            I = eta * z
            du = ((p(t) - 1) - (u**2)) * u + I
            return du

        u_init = np.random.uniform(-1e-4, 1e-4, size=N).astype(np.float64)
        sol = solve_ivp(
            f,
            [0, t_end],
            u_init,
            method='RK45',
            t_eval=np.arange(0, t_end + 1),
            first_step=1,
        )
        return sol

    def cim_envolve(J, fixed_pump, eta, t_end, iteration):
        N = J.shape[0]
        sum_ising_energy = 0
        for _ in range(iteration):
            sol_info = qiujie(J, fixed_pump, eta, t_end)
            sol = sol_info.y
            sign_value = np.sign(sol[0:N, -1])
            ising_energy = Ising(J, sign_value)
            sum_ising_energy += ising_energy
        ave_ising_energy = sum_ising_energy / iteration
        return ave_ising_energy

    def objective(trial, couple_matrix, fixed_pump):
        iteration = 20
        eta = trial.suggest_float("eta", 1e-3, 1, log=True)
        t_end = int(50 / np.sqrt(eta))
        ave_ising_energy = cim_envolve(couple_matrix, fixed_pump, eta, t_end, iteration)
        return ave_ising_energy

    optuna.logging.set_verbosity(optuna.logging.ERROR)
    study = optuna.create_study()
    study.optimize(
        lambda trial: objective(trial, couple_matrix, fixed_pump), n_trials=20
    )
    return study.best_params['eta']
