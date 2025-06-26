import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Filnavn og antall seksjoner
files = {
    "model_generation/models/model_3/plotting_visual/csv_files/without_p_g_0_init_ballast.csv": "without p_g",
    "model_generation/models/model_3/plotting_visual/csv_files/with_p_g_0_init_ballast.csv": "with p_g",
}

# Kolonnenavn for orientering og posisjon
angle_columns = {
    "Roll (phi)": "phi",
    "Pitch (theta)": "theta",
    "Yaw (psi)": "psi"
}

position_columns = {
    "X": "x",
    "Y": "y",
    "Z": "z"
}


# Funksjon for plotting
def plot_variables(columns, ylabel, title_suffix, save_name):
    plt.figure()
    for filename, sections in files.items():
        df = pd.read_csv(filename)
        time = df['time']
        for label, col in columns.items():
            if label not in plt.gca().get_legend_handles_labels()[1]:  # avoid duplicate legends
                plt.plot(time, df[col], label=f"{label} - {sections} sections")
            else:
                plt.plot(time, df[col])
    plt.xlabel("Time [s]")
    plt.ylabel(ylabel)
    plt.title(f"{ylabel} over time ({title_suffix}) - Model using quasi-velocities")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{save_name}.png")
    plt.show()

# Plot orienteringsvinkler (roll, pitch, yaw)
for angle_label, angle_col in angle_columns.items():
    plt.figure()
    for filename, sections in files.items():
        df = pd.read_csv(filename)
        plt.plot(df['time'], np.rad2deg(df[angle_col]), label=f"{sections} sections")
    plt.xlabel("Time [s]")
    plt.ylabel(f"{angle_label} [deg]")
    plt.title(f"{angle_label} over time - Model using quasi-velocities")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{angle_label.lower().replace(' ', '_')}_quasi.png")
    plt.show()

# Plot x, y og z i egne figurer
for label, col in position_columns.items():
    plt.figure()
    for filename, sections in files.items():
        df = pd.read_csv(filename)
        plt.plot(df['time'], df[col], label=f"{sections} sections")
    plt.xlabel("Tid [s]")
    plt.ylabel(f"{label} [m]")
    plt.title(f"{label} over time - Model using quasi-velocities")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"position_{label.lower()}_quasi.png")
    plt.show()


# # Plot kranleddet q1 i egen figur
# plt.figure()
# for filename, sections in files.items():
#     df = pd.read_csv(filename)
#     plt.plot(df['time'], np.rad2deg(df['q1']), label=f"{sections} sections")
# plt.xlabel("Time [s]")
# plt.ylabel("Cranejoint (q1) [deg]")
# plt.title("Cranejoint (q1) over time - Model using quasi-velocities")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.savefig("kranledd_q1_quasi.png")
# plt.show()
