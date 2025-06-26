import numpy as np
import plotly.graph_objects as go
from model_generation.kinematics.transformations import*
from sympy import *
from sympy.physics.mechanics import *
import model_generation.plotting.plotting_3d as plt3d
import pandas as pd
import model_generation.models.model_1.params as pm
import model_generation.utils.utils as util

frames_folder = "frames"

# Euler angles of boat
phi, theta, psi = symbols('phi theta psi')
# Positions of boat
x_n, y_n, z_n = symbols('x y n')
# Crane joints
q1 = symbols('q1')

q = Matrix([x_n, y_n, z_n, psi, theta, phi, q1])

T_world_frame = eye(4)
T_NED_frame = T_world_frame * trans_z(0) * trans_x(1) * trans_y(1) * rot_x(np.pi)
T_n_b = T_NED_frame * trans_x(x_n) * trans_y(y_n) * trans_z(z_n) * rot_z(psi) * rot_y(theta) * rot_x(phi)
T_n_cb = T_n_b * trans_x(pm.CraneBase.x) * trans_y(pm.CraneBase.y) * trans_z(-pm.CraneBase.height)
T_n_q1 = T_n_cb * rot_x(q1) * trans_z(-pm.Joint1Params.length)

frame_list = [T_world_frame, T_NED_frame, T_n_b, T_n_cb, T_n_q1]
frame_list_numpy = plt3d.numpify(frame_list, q)


"""_____Animation______"""

fig = go.Figure()
df = pd.read_csv("model_generation/models/model_4/plotting_visual/csv_files/model_4.csv")
vals = np.zeros((len(df), 7))

times = df["time"].to_numpy()


"""Time-handling"""
dt_max = np.max(np.diff(times))
if dt_max < 0.05:
    fps = 20
else:
    fps = int(1/dt_max)

dt_target = 1/fps
new_times = np.arange(times[0], times[-1], dt_target)
new_df = pd.DataFrame()

for col in df.columns:
    new_df[col] = np.interp(new_times, times, df[col])
new_df.to_csv("model_generation/models/model_1/test_resampled.csv", index=False)

df = pd.read_csv("model_generation/models/model_1/test_resampled.csv")
vals = np.zeros((len(df), 7))
vals[:, 0] = df["x"]      
vals[:, 1] = df["y"]    
vals[:, 2] = df["z"]       
vals[:, 3] = df["psi"]  
vals[:, 4] = df["theta"]
vals[:, 5] = df["phi"]
vals[:, 6] = df["q1"]

frame_list_numpy_numbers = plt3d.evaluate_frames(frame_list_numpy, vals[0, :])

fig_data = plt3d.plot_3dframes_data(frame_list_numpy_numbers, 0.1)
fig_data.append(plt3d.draw_prism_data(frame_list_numpy_numbers[2], pm.BoatParams.length, pm.BoatParams.width, pm.BoatParams.height, opacity=0.1))
fig_data.append(plt3d.draw_frame_line_data(frame_list_numpy_numbers[3], [0, 0, 0], [0, 0, pm.CraneBase.height]))
fig_data.append(plt3d.draw_frame_line_data(frame_list_numpy_numbers[4], [0, 0, 0], [0, 0, pm.Joint1Params.length]))

# Ballast tanks
fig_data.append(plt3d.draw_prism_data(util.add_point_se3(frame_list_numpy_numbers[2], pm.TanksAftPortside.r),
                pm.TanksAftPortside.length, pm.TanksAftPortside.length, pm.TanksAftPortside.length, opacity=0.4, color='red'))
fig_data.append(plt3d.draw_prism_data(util.add_point_se3(frame_list_numpy_numbers[2], pm.TanksAftStarboard.r),
                pm.TanksAftStarboard.length, pm.TanksAftStarboard.length, pm.TanksAftStarboard.length, opacity=0.4, color='red'))
fig_data.append(plt3d.draw_prism_data(util.add_point_se3(frame_list_numpy_numbers[2], pm.TanksForepeakPortside.r),
                pm.TanksForepeakPortside.length, pm.TanksForepeakPortside.length, pm.TanksForepeakPortside.length, opacity=0.4, color='red'))
fig_data.append(plt3d.draw_prism_data(util.add_point_se3(frame_list_numpy_numbers[2], pm.TanksForepeakStarboard.r),
                pm.TanksForepeakStarboard.length, pm.TanksForepeakStarboard.length, pm.TanksForepeakStarboard.length, opacity=0.4, color='red'))


fig.add_traces(fig_data)

frames = []

for i in range(len(vals) - 1):
    frame_list_numpy_numbers = plt3d.evaluate_frames(frame_list_numpy, (vals[i,:]))

    frame_data = plt3d.plot_3dframes_data(frame_list_numpy_numbers, 0.1)
    frame_data.append(plt3d.draw_prism_data(frame_list_numpy_numbers[2], pm.BoatParams.length, pm.BoatParams.width, pm.BoatParams.height, opacity=1))
    frame_data.append(plt3d.draw_frame_line_data(frame_list_numpy_numbers[3], [0, 0, 0], [0, 0, pm.CraneBase.height]))
    frame_data.append(plt3d.draw_frame_line_data(frame_list_numpy_numbers[4], [0, 0, 0], [0, 0, pm.Joint1Params.length]))
    frame_data.append(plt3d.draw_prism_data(util.add_point_se3(frame_list_numpy_numbers[2], pm.TanksAftPortside.r),
                pm.TanksAftPortside.length, pm.TanksAftPortside.length, pm.TanksAftPortside.length, opacity=0.4, color='red'))
    frame_data.append(plt3d.draw_prism_data(util.add_point_se3(frame_list_numpy_numbers[2], pm.TanksAftStarboard.r),
                pm.TanksAftStarboard.length, pm.TanksAftStarboard.length, pm.TanksAftStarboard.length, opacity=0.4, color='red'))
    frame_data.append(plt3d.draw_prism_data(util.add_point_se3(frame_list_numpy_numbers[2], pm.TanksForepeakPortside.r),
                pm.TanksForepeakPortside.length, pm.TanksForepeakPortside.length, pm.TanksForepeakPortside.length, opacity=0.4, color='red'))
    frame_data.append(plt3d.draw_prism_data(util.add_point_se3(frame_list_numpy_numbers[2], pm.TanksForepeakStarboard.r),
                pm.TanksForepeakStarboard.length, pm.TanksForepeakStarboard.length, pm.TanksForepeakStarboard.length, opacity=0.4, color='red'))



    frame = go.Frame(
        data = frame_data,
        name = str(i)
    )

    frames.append(frame)

fig.frames = frames

fig.update_layout(
    updatemenus=[{
        "buttons": [
            {
                "args": [None, {"frame": {"duration": fps, "redraw": True}, "fromcurrent": True}],
                "label": "▶ Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                "label": "⏸ Pause",
                "method": "animate"
            }
        ]
    }],
    sliders=[{
        "steps": [
            {
                "args": [[str(i)], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                "label": str(i),
                "method": "animate"
            } for i in range(len(frames))
        ],
        "active": 0,
        "y": 0,
        "x": 0.1,
        "currentvalue": {"prefix": "Frame: "}
    }],
    scene=dict(
        aspectmode="manual",
        aspectratio=dict(x=1, y=1, z=1),
        camera=dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=1.5, y=1.5, z=1.5)
        ),
        xaxis=dict(range=[-10, 10]),  # 🔹 Låser X-aksen
        yaxis=dict(range=[-10, 10]),  # 🔹 Låser Y-aksen
        zaxis=dict(range=[-10, 10])   # 🔹 Låser Z-aksen
    )
)


fig.show()
