import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

files = [
    (r"$\mathbf{8}$: 2x4", "model_generation/models/model_5/plotting_visual/csv_files/wave_exp_6dof/w2_l4_45_deg.csv"),
    (r"$\mathbf{32}$: 4x8", "model_generation/models/model_5/plotting_visual/csv_files/wave_exp_6dof/w4_l8_45_deg.csv"),
    (r"$\mathbf{120}$: 8x15", "model_generation/models/model_5/plotting_visual/csv_files/wave_exp_6dof/w8_l15_45_deg.csv"),
    (r"$\mathbf{450}$: 15x30", "model_generation/models/model_5/plotting_visual/csv_files/wave_exp_6dof/w15_l30_45_deg.csv"),
    (r"$\mathbf{1035}$: 23x45", "model_generation/models/model_5/plotting_visual/csv_files/wave_exp_6dof/w23_l45_45_deg.csv"),
    (r"$\mathbf{1800}$: 30x60", "model_generation/models/model_5/plotting_visual/csv_files/wave_exp_6dof/w30_l60_45_deg.csv"),
]

data = [(label, pd.read_csv(path)) for label, path in files]

# fig, axes = plt.subplots(1, 2, figsize=(18, 5), sharex=True)

# for label, df in data:
#     axes[0].plot(df['time'], np.rad2deg(df['phi']), label=label)
# axes[0].set_xlim(40, 60)
# axes[0].set_xlabel('Time (s)')
# axes[0].set_ylabel('Roll φ (deg)')
# axes[0].set_title('Roll')
# axes[0].legend()
# axes[0].grid(True)

# for label, df in data:
#     axes[1].plot(df['time'], df['z'], label=label)
# axes[1].set_xlim(40, 60)
# axes[1].set_xlabel('Time (s)')
# axes[1].set_ylabel('Heave z (m)')
# axes[1].set_title('Heave')
# axes[1].legend()
# axes[1].grid(True)

# for label, df in data:
#     axes[2].plot(df['time'], np.rad2deg(df['theta']), label=label)
# axes[2].set_xlim(40, 60)
# axes[2].set_xlabel('Time (s)')
# axes[2].set_ylabel('Pitch θ (deg)')
# axes[2].set_title('Pitch')
# axes[2].legend()
# axes[2].grid(True)

# fig.suptitle("Boat (6 DOF) – N=100, Hp = 0.6 m, Tp = 4.0 s, attack angle = 45°", fontsize=16)

# plt.tight_layout(rect=[0, 0, 1, 0.95])
# plt.show()


# Plot phi (Pitch)
plt.figure()

for label, df in data:
    plt.plot(df['time'], np.rad2deg(df['phi']), label=label)

plt.grid(True)
plt.xlim(40, 60)
plt.ylim(-6, 6)
plt.legend(fontsize=14, loc='lower left')

# Bold hovedtittel + undertittel
plt.title("Pitch", fontsize=16, fontweight='bold', pad=25)
plt.text(0.5, 1.01, "Boat (6 DOF) – N=100, Hp = 0.6 m, Tp = 4.0 s, attack angle = 45°", 
         fontsize=14, ha='center', va='bottom', transform=plt.gca().transAxes)

plt.show()

# Plot z (Heave)
plt.figure()

for label, df in data:
    plt.plot(df['time'], df['z'], label=label)

plt.grid(True)
plt.xlim(40, 60)
plt.legend(fontsize=14, loc='lower left')

plt.title("Heave", fontsize=16, fontweight='bold', pad=25)
plt.text(0.5, 1.02, "Boat (6 DOF) – N=100, Hp = 0.6 m, Tp = 4.0 s, attack angle = 45°", 
         fontsize=14, ha='center', va='bottom', transform=plt.gca().transAxes)

plt.show()
