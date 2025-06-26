import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

"""Comparing models"""

test_folder = 'test1'
out_dir = '../bilder/results/'
specific_folder = 'del3/test1_2'
dir = out_dir+specific_folder
testname = 'part3_test1_2'
file_type = 'pdf'
start = 0
end = 100
print(dir)
print(start)
print(end)

files = [
    # ("M1", f"model_generation/comparing_models/waves/{test_folder}/M1.csv"),
    # ("M2", f"model_generation/comparing_models/waves/{test_folder}/M2.csv"),
    (r"Attack angle: $70^{\circ}$", f"model_generation/comparing_models/lifting_operation/test1/M5.csv"),
    # ("M4 (crane)", f"model_generation/comparing_models/waves/{test_folder}/M4.csv"),
    (r"Attack angle: $10^{\circ}$", f"model_generation/comparing_models/lifting_operation/test2/M5.csv"),
]

data = [(label, pd.read_csv(path)) for label, path in files]

"""Plot surge"""
plt.figure()
for label, df in data:
    plt.plot(df['time'], (df['x']), label=label)
plt.grid(True)
plt.xlim(start, end)
plt.legend(fontsize=14, ncol=3, loc='upper center',
           bbox_to_anchor=(0.5, -0.15), frameon=False)
plt.title(r"Surge $x^{n}$", fontsize=20, fontweight='bold', pad=32)
plt.savefig(f"{dir}/surge{testname}.{file_type}", dpi=300, bbox_inches='tight'); plt.close()
#plt.show()

"""Plot theta (Pitch)"""
plt.figure()
for label, df in data:
    plt.plot(df['time'], np.rad2deg(df['theta']), label=label, linewidth=1.8)
plt.grid(True)
plt.xlim(start, end)
plt.legend(fontsize=14, ncol=3, loc='upper center',
           bbox_to_anchor=(0.5, -0.15), frameon=False)
plt.title(r"Pitch $\theta$ (deg)", fontsize=20, fontweight='bold', pad=32)
plt.savefig(f"{dir}/pitch{testname}.{file_type}", dpi=300, bbox_inches='tight'); plt.close()
#plt.show()

"""Plot sway"""
plt.figure()
for label, df in data:
    plt.plot(df['time'], (df['y']), label=label)
plt.grid(True)
plt.xlim(start, end)
plt.legend(fontsize=14, ncol=3, loc='upper center',
           bbox_to_anchor=(0.5, -0.15), frameon=False)
plt.title(r"Sway $y^{n}$", fontsize=20, fontweight='bold', pad=32)
plt.savefig(f"{dir}/sway{testname}.{file_type}", dpi=300, bbox_inches='tight'); plt.close()
#plt.show()



"""Plot phi (Roll)"""
plt.figure()
for label, df in data:
    plt.plot(df['time'], np.rad2deg(df['phi']), label=label, linewidth=1.8)
plt.grid(True)
plt.xlim(start, end)
plt.legend(fontsize=14, ncol=3, loc='upper center',
           bbox_to_anchor=(0.5, -0.15), frameon=False)
plt.title(r"Roll $\phi$ (deg)", fontsize=20, fontweight='bold', pad=32)
plt.savefig(f"{dir}/roll{testname}.{file_type}", dpi=300, bbox_inches='tight'); plt.close()
#plt.show()

"""Plot z (Heave)"""
plt.figure(figsize=(12,5))
for label, df in data:
    plt.plot(df['time'], df['z'], label=label, linewidth=1.8)
plt.grid(True)
plt.xlim(start, end)
plt.legend(fontsize=14, ncol=3, loc='upper center',
           bbox_to_anchor=(0.5, -0.15), frameon=False)
plt.title(r"Heave $z^{n}$", fontsize=20, fontweight='bold', pad=32)
plt.savefig(f"{dir}/heave{testname}.{file_type}", dpi=300, bbox_inches='tight'); plt.close()
#plt.show()

"""Plot psi (yaw)"""
plt.figure()
for label, df in data:
    plt.plot(df['time'], df['psi'], label=label, linewidth=1.8)
plt.grid(True)
plt.xlim(start, end)
plt.legend(fontsize=14, ncol=3, loc='upper center',
           bbox_to_anchor=(0.5, -0.15), frameon=False)
plt.title(r"Yaw $\psi$", fontsize=20, fontweight='bold', pad=32)
plt.savefig(f"{dir}/yaw{testname}.{file_type}", dpi=300, bbox_inches='tight'); plt.close()
#plt.show()


"""Plot pendulum"""
plt.figure()
for label, df in data:
    plt.plot(df['time'], np.rad2deg(df['q1_p']), label=label + r" $q_{1p}$")
    plt.plot(df['time'], np.rad2deg(df['q2_p']), label=label + r" $q_{2p}$")
plt.grid(True)
plt.xlim(start, end)
plt.legend(fontsize=14, ncol=3, loc='upper center',
           bbox_to_anchor=(0.5, -0.15), frameon=False)
plt.title(r"Crane pendulum (deg)", fontsize=20, fontweight='bold', pad=32)
plt.savefig(f"{dir}/pendulum{testname}.{file_type}", dpi=300, bbox_inches='tight'); plt.close()
#plt.show()

"""Plot q1"""
plt.figure(figsize=(12,5))
for label, df in data:
    plt.plot(df['time'], np.rad2deg(df['q1']), label=label)
plt.axvline(x=50, color='red', linestyle='--', linewidth=1.5)
plt.axvline(x=80, color='red', linestyle='--', linewidth=1.5)
plt.grid(True)
plt.xlim(start, end)
plt.legend(fontsize=14, ncol=3, loc='upper center',
           bbox_to_anchor=(0.5, -0.15), frameon=False)
plt.title(r"Crane $q_{1}$ (deg)", fontsize=20, fontweight='bold', pad=32)
plt.savefig(f"{dir}/q1{testname}.{file_type}", dpi=300, bbox_inches='tight'); plt.close()
#plt.show()

"""Plot q2"""
plt.figure()
for label, df in data:
    plt.plot(df['time'], np.rad2deg(df['q2']), label=label)
plt.grid(True)
plt.xlim(start, end)
plt.legend(fontsize=14, ncol=3, loc='upper center',
           bbox_to_anchor=(0.5, -0.15), frameon=False)
plt.title(r"Crane $q_{2}$ (deg)", fontsize=20, fontweight='bold', pad=32)
plt.savefig(f"{dir}/q2{testname}.{file_type}", dpi=300, bbox_inches='tight'); plt.close()
#plt.show()

"""Plot q3"""
plt.figure()
for label, df in data:
    plt.plot(df['time'], np.rad2deg(df['q3']), label=label)
plt.grid(True)
plt.xlim(start, end)
plt.legend(fontsize=14, ncol=3, loc='upper center',
           bbox_to_anchor=(0.5, -0.15), frameon=False)
plt.title(r"Crane $q_{3}$ (deg)", fontsize=20, fontweight='bold', pad=32)
plt.savefig(f"{dir}/q3{testname}.{file_type}", dpi=300, bbox_inches='tight'); plt.close()
#plt.show()

"""Plot q4"""
plt.figure()
for label, df in data:
    plt.plot(df['time'], (df['q4']), label=label)
plt.grid(True)
plt.xlim(start, end)
plt.legend(fontsize=14, ncol=3, loc='upper center',
           bbox_to_anchor=(0.5, -0.15), frameon=False)
plt.title(r"Crane $q_{4}$ (deg)", fontsize=20, fontweight='bold', pad=32)
plt.savefig(f"{dir}/q4{testname}.{file_type}", dpi=300, bbox_inches='tight'); plt.close()
#plt.show()

"""___special plot_____"""
fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()

# Plot q1 fra første datasett (grønn linje)
label_q1, df_q1 = data[0]
line_q1, = ax1.plot(df_q1['time'], np.rad2deg(df_q1['q1']),
                    color='tab:green', linestyle='-', linewidth=1.8,
                    label=r"$q_1$")

# Fargekart for phi
phi_colors = {
    r"Attack angle: $70^{\circ}$": "tab:blue",
    r"Attack angle: $10^{\circ}$": "tab:orange",
}

# Plott phi og horisontale max-linjer (ingen label på max-linjer)
phi_lines = []
phi_labels = []

for label, df in data:
    phi_deg = np.rad2deg(df['phi'])
    c = phi_colors[label]

    line_phi, = ax2.plot(df['time'], phi_deg,
                         color=c, linestyle='--', linewidth=1.8)
    phi_lines.append(line_phi)
    phi_labels.append(label + r"  $\varphi$")

    max_phi = np.max(np.abs(phi_deg))
    ax2.axhline(y=max_phi, color='red', linestyle=':', linewidth=1.2)
    ax2.text(df['time'].iloc[-1] + 3, max_phi,
             f"max roll: {max_phi:.2f}°",
             color='red', fontsize=10, va='bottom')

# Akser og styling
ax1.set_xlim(start, end)
ax1.set_xlabel("Time [s]")
ax1.set_ylabel(r"$q_1$ [deg]")
ax2.set_ylabel(r"Roll $\varphi$ [deg]")
ax1.grid(True)

# Legend (kun q1 og phi-kurver)
legend_lines = [line_q1] + phi_lines
legend_labels = [r"$q_1$"] + phi_labels
ax1.legend(legend_lines, legend_labels, fontsize=14, ncol=3,
           loc='upper center', bbox_to_anchor=(0.5, -0.15), frameon=False)

plt.title(r"Crane $q_{1}$ and Roll $\varphi$", fontsize=20,
          fontweight='bold', pad=32)
plt.tight_layout()
plt.savefig(f"{dir}/q1_phi_{testname}.{file_type}", dpi=300, bbox_inches='tight')
plt.close()
