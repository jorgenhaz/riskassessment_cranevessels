import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("model_generation/models/model_4/plotting_visual/csv_files/model_4.csv", index_col=False)
df_wave = pd.read_csv("model_generation/models/model_4/plotting_visual/csv_files/wave_model_4.csv", index_col=False)


plt.figure()

plt.plot(df["time"], (df["z"]), label="z")
plt.plot(df["time"], (df["x"]), label = 'x')
plt.plot(df["time"], (df["y"]), label = 'y')
plt.plot(df_wave["time"], (df_wave["z"]), label="z wave")
plt.plot(df_wave["time"], (df_wave["x"]), label = 'x wave')
plt.plot(df_wave["time"], (df_wave["y"]), label = 'y wave')
plt.xlabel('Time (s)')
plt.title("Boat (6 dof) with crane and pendulum")
plt.legend()
plt.grid()
plt.show()


plt.plot(df["time"], np.rad2deg(df["phi"]), label="phi")
plt.plot(df["time"], np.rad2deg(df["theta"]), label = 'theta')
plt.plot(df_wave["time"], np.rad2deg(df_wave["phi"]), label="phi wave")
plt.plot(df_wave["time"], np.rad2deg(df_wave["theta"]), label = 'theta wave')
plt.xlabel('Time (s)')
plt.title("Boat (6 dof) with crane and pendulum")
plt.legend()
plt.grid()
plt.show()

plt.plot(df["time"], np.rad2deg(df["psi"]), label = 'psi')
plt.plot(df_wave["time"], np.rad2deg(df_wave["psi"]), label = 'psi wave')
plt.xlabel('Time (s)')
plt.title("Boat (6 dof) with crane and pendulum")
plt.legend()
plt.grid()
plt.show()

plt.plot(df["time"], np.rad2deg(df["q1_p"]), label = 'pendulum q1')
plt.plot(df["time"], np.rad2deg(df["q2_p"]), label = 'pendulum q2')
plt.plot(df_wave["time"], np.rad2deg(df_wave["q1_p"]), label = 'pendulum q1 wave')
plt.plot(df_wave["time"], np.rad2deg(df_wave["q2_p"]), label = 'pendulum q2 wave')
plt.xlabel('Time (s)')
plt.title("Boat (6 dof) with crane and pendulum")
plt.legend()
plt.grid()
plt.show()

plt.plot(df["time"], np.rad2deg(df["q1"]), label = 'q1')
plt.plot(df["time"], np.rad2deg(df["q2"]), label = 'q2')
plt.plot(df["time"], np.rad2deg(df["q3"]), label = 'q3')
plt.plot(df["time"], (df["q4"]), label = 'q4')
plt.plot(df_wave["time"], np.rad2deg(df_wave["q1"]), label = 'q1 wave')
plt.plot(df_wave["time"], np.rad2deg(df_wave["q2"]), label = 'q2 wave')
plt.plot(df_wave["time"], np.rad2deg(df_wave["q3"]), label = 'q3 wave')
plt.plot(df_wave["time"], (df_wave["q4"]), label = 'q4 wave')
plt.xlabel('Time (s)')
plt.title("Boat (6 dof) with crane and pendulum")
plt.legend()
plt.grid()
plt.show()
