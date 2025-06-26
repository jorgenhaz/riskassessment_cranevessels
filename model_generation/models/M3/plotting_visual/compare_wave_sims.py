import pandas as pd
import matplotlib.pyplot as plt

# Filnavn og antall seksjoner
files = {
    "model_generation/models/model_1/1_sections_yaw_1.csv": 1,
    "model_generation/models/model_1/5_sections_yaw_1.csv": 5,
    "model_generation/models/model_1/10_sections_yaw_1.csv": 10,
    "model_generation/models/model_1/40_sections_yaw_1.csv": 40,
    "model_generation/models/model_1/90_sections_yaw_1.csv": 90,
    "model_generation/models/model_1/160_sections_yaw_1.csv": 160,
    "model_generation/models/model_1/400_sections_yaw_1.csv": 400,
    "model_generation/models/model_1/960_sections_yaw_1.csv": 960,
    "model_generation/models/model_1/2000_sections_yaw_1.csv": 2000
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
        plt.plot(df['time'], df[angle_col], label=f"{sections} sections")
    plt.xlabel("Time [s]")
    plt.ylabel(f"{angle_label} [rad]")
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


# Plot kranleddet q1 i egen figur
plt.figure()
for filename, sections in files.items():
    df = pd.read_csv(filename)
    plt.plot(df['time'], df['q1'], label=f"{sections} sections")
plt.xlabel("Time [s]")
plt.ylabel("Cranejoint (q1) [rad]")
plt.title("Cranejoint (q1) over time - Model using quasi-velocities")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("kranledd_q1_quasi.png")
plt.show()
