from datetime import datetime
from sympy import *
from sympy.physics.mechanics import*
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
import dill
import pandas as pd

def compute_difference(var_index, vals_euler, vals_quasi):

    from scipy.interpolate import interp1d

    t_euler = vals_euler[:, 0]
    t_quasi = vals_quasi[:, 0]
    quasi_interp_func = interp1d(t_quasi, vals_quasi[:, var_index], kind='linear', fill_value='extrapolate')
    quasi_interp_vals = quasi_interp_func(t_euler)

    diff_rad = vals_euler[:, var_index] - quasi_interp_vals
    return t_euler, (diff_rad)  # Returner i grader

def plot_multiple_named(var_names, df_euler, df_quasi):
    """
    Plotter valgte variabler i 3 side-by-side figurer.
    var_names: liste med 3 kolonnenavn, f.eks. ['phi', 'theta', 'psi']
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    for i, var in enumerate(var_names):
        axes[i].plot(df_euler["time"], np.rad2deg(df_euler[var]) if 'phi' in var or 'theta' in var or 'psi' in var else df_euler[var], label='euler')
        axes[i].plot(df_quasi["time"], np.rad2deg(df_quasi[var]) if 'phi' in var or 'theta' in var or 'psi' in var else df_quasi[var], label='quasi')
        axes[i].set_title(var)
        axes[i].set_xlabel("Time (s)")
        axes[i].set_ylabel("Degrees" if 'phi' in var or 'theta' in var or 'psi' in var else "Value")
        axes[i].legend()
        axes[i].grid()

    plt.tight_layout()
    plt.show()


df_euler = pd.read_csv("model_generation/models/model_3/plotting_visual/csv_files/without_p_g_1000_init_ballast.csv")
df_quasi = pd.read_csv("model_generation/models/model_3/plotting_visual/csv_files/with_p_g_1000_init_ballast.csv")

# Creating an empty matrix for the csv-values
vals_euler = np.zeros((len(df_euler), 26))
vals_quasi = np.zeros((len(df_quasi), 33))

# Extracting CSV-values 
vals_euler[:, 0] = df_euler["time"]
vals_euler[:, 1] = df_euler["x"]       
vals_euler[:, 2] = df_euler["y"]     
vals_euler[:, 3] = df_euler["z"]       
vals_euler[:, 4] = df_euler["phi"] 
vals_euler[:, 5] = df_euler["theta"]
vals_euler[:, 6] = df_euler["psi"]
vals_euler[:, 7] = df_euler["q1"]
vals_euler[:, 8] = df_euler["phidot"]

vals_quasi[:, 0] = df_quasi["time"]
vals_quasi[:, 1] = df_quasi["x"]       
vals_quasi[:, 2] = df_quasi["y"]     
vals_quasi[:, 3] = df_quasi["z"]       
vals_quasi[:, 4] = df_quasi["phi"] 
vals_quasi[:, 5] = df_quasi["theta"]
vals_quasi[:, 6] = df_quasi["psi"]
vals_quasi[:, 7] = df_quasi["q1"]
quasi_phi_dot = diff(df_quasi["phi"])


t_phi, phi_diff = compute_difference(4, vals_euler, vals_quasi)
t_theta, theta_diff = compute_difference(5, vals_euler, vals_quasi)
t_psi, psi_diff = compute_difference(6, vals_euler, vals_quasi)

plot_multiple_named(["phi", "theta", "psi"], df_euler, df_quasi)
plot_multiple_named(["x", "y", "z"], df_euler, df_quasi)

# Plot results
plt.figure()
# plt.plot(t_phi,np.rad2deg(phi_diff), label='phi - diff')
plt.plot(df_euler['time'], np.rad2deg(df_euler["q1"]), label='q1 - euler')
plt.plot(df_quasi['time'], np.rad2deg(df_quasi["q1"]), label='q1 - quasi')


plt.xlabel('Time (s)')
plt.ylabel('Angle (degrees)')
plt.title("Figure")
plt.legend()
plt.grid()
plt.show()