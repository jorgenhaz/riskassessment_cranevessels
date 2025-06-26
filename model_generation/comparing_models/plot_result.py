import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

"""Comparing models"""

files = [
    # ("M1", "model_generation/comparing_models/csv_files/M1.csv"),
    # ("M1 - new damping",  "model_generation/comparing_models/csv_files/M1_new_damping.csv"),
    # #("M2", "model_generation/comparing_models/csv_files/M2.csv"),
    # ("M3", "model_generation/comparing_models/csv_files/M3.csv"),
    # ("M4", "model_generation/comparing_models/csv_files/M4.csv"),
    # ("M5", "model_generation/comparing_models/csv_files/M5.csv"),
    ("M5nonopt ", "model_generation/comparing_models/csv_files/M5_non_optimized.csv"),
    ("M3opt",  "model_generation/comparing_models/csv_files/M5_optimized.csv"),
    # ("M5", "model_generation/comparing_models/csv_files/M5.csv"),
    # ("M5 - new damping",  "model_generation/comparing_models/csv_files/M5_new_damping.csv"),
]

data = [(label, pd.read_csv(path)) for label, path in files]



plt.figure()
for label, df in data:
    plt.plot(df['time'], np.rad2deg(df['q1']), label=label + 'q1')
    plt.plot(df['time'], np.rad2deg(df['q2']), label=label + 'q2')
    plt.plot(df['time'], np.rad2deg(df['q3']), label=label + 'q3')
    plt.plot(df['time'], (df['q4']), label=label + 'q4')
plt.grid(True)
plt.legend()
plt.show()

plt.figure()
for label, df in data:
    plt.plot(df['time'], (df['x']), label=label + 'x')
    plt.plot(df['time'], (df['y']), label=label + 'y')
plt.grid(True)
plt.legend()
plt.show()


# Plot phi (roll)
plt.figure()

for label, df in data:
    plt.plot(df['time'], np.rad2deg(df['phi']), label=label + 'phi', linewidth=1.8)

plt.grid(True)
plt.xlim(0, 100)
plt.legend(fontsize=18, loc='lower left')

plt.title("Roll", fontsize=20, fontweight='bold', pad=32)
plt.text(0.5, 1.01, "Boat (6 DOF) – N=100, Hp = 0.6 m, Tp = 4.0 s, attack angle = 45°", 
         fontsize=18, ha='center', va='bottom', transform=plt.gca().transAxes,fontweight='bold')

plt.show()

# Plot pitch (Pitch)
plt.figure()

for label, df in data:
    plt.plot(df['time'], np.rad2deg(df['theta']), label=label + 'theta', linewidth=1.8)

plt.grid(True)
plt.xlim(0, 100)
plt.legend(fontsize=18, loc='lower left')

plt.title("Pitch", fontsize=20, fontweight='bold', pad=32)
plt.text(0.5, 1.01, "Boat (6 DOF) – N=100, Hp = 0.6 m, Tp = 4.0 s, attack angle = 45°", 
         fontsize=18, ha='center', va='bottom', transform=plt.gca().transAxes,fontweight='bold')

plt.show()

# Plot z (Heave)
plt.figure()

for label, df in data:
    plt.plot(df['time'], df['z'], label=label + 'z', linewidth=1.8)

plt.grid(True)
plt.xlim(0, 100)
plt.legend(fontsize=18, loc='lower left')

plt.show()


plt.figure()
for label, df in data:
    plt.plot(df['time'], np.rad2deg(df['q1_p']), label=label + 'pendulum')
    plt.plot(df['time'], np.rad2deg(df['q2_p']), label=label + 'pendulum')

plt.grid(True)
plt.legend()
plt.show()

