import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_m3 = pd.read_csv("model_generation/comparing_models/no_waves/test4/M3.csv")
df_m5 = pd.read_csv("model_generation/comparing_models/no_waves/test4/M5.csv")

time = df_m3['time'].values
phi_m5 = np.rad2deg(np.interp(time, df_m5['time'], df_m5['phi']))

mask   = time <= 50
time   = time[mask]
phi_m3 = np.rad2deg(df_m3['phi'].values[mask])
phi_m5 = phi_m5[mask]
q1     = np.rad2deg(df_m3['q2'].values[mask])
q2     = np.rad2deg(df_m3['q3'].values[mask])

dphi = phi_m3 - phi_m5
dq12 = (q1 + q2) - (q1[0] + q2[0])
rho  = np.corrcoef(dphi, dq12)[0, 1]

plt.figure(figsize=(11, 8))


ax_top = plt.subplot(2, 1, 1)
ax_top.plot(time, phi_m3, label='M3', linewidth=1.8)
ax_top.plot(time, phi_m5, '--', label='M5', linewidth=1.8)
ax_top.set_ylabel('Roll [deg]')
ax_top.set_xlim(0, 50)
ax_top.grid(True)
ax_top.legend(fontsize=14, ncol=2, loc='upper center',
              bbox_to_anchor=(0.5, -0.15), frameon=False)
ax_top.set_title(r"Roll $\phi$ (deg) – M3 vs M5 – 2 m boom extension",
                 fontsize=20, fontweight='bold', pad=32)

ax1 = plt.subplot(2, 1, 2)
line1, = ax1.plot(time, dphi, label=r'$\Delta\phi$', linewidth=1.8)
ax2 = ax1.twinx()
line2, = ax2.plot(time, dq12, 'k--', label=r'$\Delta(q_2+q_3)$', linewidth=1.8)

ax1.set_ylabel(r'$\Delta\phi$ [deg]')
ax2.set_ylabel(r'$\Delta(q_2+q_3)$ [deg]')
ax1.set_xlim(0, 50)
ax1.grid(True)

ax1.set_title(r'Deviation: $\Delta\phi$ vs $\Delta(q_2+q_3)$   (ρ = %.3f)' % rho,
              fontsize=18, fontweight='bold', pad=20)
ax1.set_xlabel('Time [s]')

lines  = [line1, line2]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, fontsize=14, ncol=2, loc='upper center',
           bbox_to_anchor=(0.5, -0.25), frameon=False)

plt.tight_layout()
plt.show()