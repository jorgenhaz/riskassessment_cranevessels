import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

"""Comparing models"""

test_folder = 'test2'
out_dir = '../bilder/results/'
specific_folder = 'del4/test2'
dir = out_dir+specific_folder
testname = 'part4_test2'
file_type = 'pdf'
start = 0
end = 100
print(dir)
print(start)
print(end)

files = [
    # ("M1", f"model_generation/comparing_models/waves/{test_folder}/M1.csv"),
    # ("M2", f"model_generation/comparing_models/waves/{test_folder}/M2.csv"),
    ("M3 (crane)", f"model_generation/comparing_models/payload_loss/{test_folder}/M3.csv"),
    #("M4 (crane)", f"model_generation/comparing_models/waves/{test_folder}/M4.csv"),
    ("M5 (crane)", f"model_generation/comparing_models/payload_loss/{test_folder}/M5.csv"),
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
    max_theta = np.rad2deg(np.max(np.abs(df['theta'])))
plt.grid(True)
plt.xlim(start, end)
plt.legend(fontsize=14, ncol=3, loc='upper center',
           bbox_to_anchor=(0.5, -0.15), frameon=False)
plt.axvline(x=50, color='red', linestyle='--', linewidth=1.5)
plt.title(r"Pitch $\theta$ (deg)", fontsize=20, fontweight='bold', pad=32)
plt.savefig(f"{dir}/pitch{testname}.{file_type}", dpi=300, bbox_inches='tight'); plt.close()
#plt.show()
print('max theta: ', max_theta)

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
    max_phi = np.rad2deg(np.max(np.abs(df['phi'])))
plt.grid(True)
plt.xlim(start, end)
plt.legend(fontsize=14, ncol=3, loc='upper center',
           bbox_to_anchor=(0.5, -0.15), frameon=False)
plt.axvline(x=50, color='red', linestyle='--', linewidth=1.5)
plt.title(r"Roll $\phi$ (deg)", fontsize=20, fontweight='bold', pad=32)
plt.savefig(f"{dir}/roll{testname}.{file_type}", dpi=300, bbox_inches='tight'); plt.close()
print("max phi: ", max_phi)
#plt.show()

"""Plot z (Heave)"""
plt.figure()
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
plt.figure()
for label, df in data:
    plt.plot(df['time'], np.rad2deg(df['q1']), label=label)
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