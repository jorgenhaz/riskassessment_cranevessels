from sympy import *
from sympy.physics.mechanics import*
from model_generation.kinematics.transformations import*
import numpy as np
from model_generation.plotting.plotting_3d import plot_3dframes, numpify, evaluate_frames, draw_frame_line, plot_point, draw_prism, draw_text_in_frame
import model_generation.models.model_2.quasi_variable_cog.params as pm
import plotly.graph_objects as go
import model_generation.utils.utils as util

# Euler angles of boat
phi, theta, psi = symbols('phi theta psi')
# Positions of boat
x_n, y_n, z_n = symbols('x y n')
# Crane joints
q1, q2, q3, q4, q1_p, q2_p = symbols('q1 q2 q3 q4 q1_p q2_p')

q = Matrix([x_n, y_n, z_n, phi, theta, psi, q1, q2, q3, q4, q1_p, q2_p])
q_vals = [10, 10, 0.0, 0.0, -0.0, 0, -1, 1.0, -0.2, 9, 0.5,0.0]


T_world_frame = eye(4)
T_NED_frame = T_world_frame * trans_z(0) * trans_x(1) * trans_y(1) * rot_x(np.pi)
T_n_b = T_NED_frame * trans_x(x_n) * trans_y(y_n) * trans_z(z_n) * rot_z(psi) * rot_y(theta) * rot_x(phi)
T_n_cb = T_n_b * trans_x(pm.CraneBase.x) * trans_y(pm.CraneBase.y) * trans_z(-pm.CraneBase.height)
T_n_q1 = T_n_cb * rot_z(q1) * trans_z(-pm.Joint1Params.length)
T_n_q2 = T_n_q1 * rot_y(q2) * trans_x(pm.Joint2Params.length)
T_n_q3 = T_n_q2 * rot_y(q3) * trans_x(pm.Joint3Params.length)
T_n_q4 = T_n_q3 * trans_x(q4 + pm.Joint4Params.length)
T_n_payload = T_n_q4 * rot_x(q1_p) * rot_y(q2_p) * trans_z(2)

frame_list = [T_world_frame, T_NED_frame, T_n_b, T_n_cb, T_n_q1, T_n_q2, T_n_q3, T_n_q4, T_n_payload]
frame_list_numpy = numpify(frame_list, q)
frame_list_numpy_numbers = evaluate_frames(frame_list_numpy, q_vals)

fig = go.Figure()

plot_3dframes(fig, frame_list_numpy_numbers, 0.3)
draw_prism(fig, frame_list_numpy_numbers[2], pm.BoatParams.length, pm.BoatParams.width, pm.BoatParams.height, opacity=0.1, offset=np.array([0, 0, pm.BoatParams.height/2]))

draw_prism(fig, util.add_point_se3(frame_list_numpy_numbers[2], (pm.TanksAftPortside.r+Matrix([0, 0, pm.TanksAftPortside.height/2]))), 
           pm.TanksAftPortside.length, pm.TanksAftPortside.width, pm.TanksAftPortside.height, opacity=0.1, color='red')
draw_prism(fig, util.add_point_se3(frame_list_numpy_numbers[2],(pm.TanksAftStarboard.r+Matrix([0, 0, pm.TanksAftStarboard.height/2]))), 
           pm.TanksAftStarboard.length, pm.TanksAftStarboard.width, pm.TanksAftStarboard.height, opacity=0.1, color='red')
draw_prism(fig, util.add_point_se3(frame_list_numpy_numbers[2], (pm.TanksForepeakPortside.r+Matrix([0, 0, pm.TanksForepeakPortside.height/2]))), 
           pm.TanksForepeakPortside.length, pm.TanksForepeakPortside.width, pm.TanksForepeakPortside.height, opacity=0.1, color='red')
draw_prism(fig, util.add_point_se3(frame_list_numpy_numbers[2], (pm.TanksForepeakStarboard.r+Matrix([0, 0, pm.TanksForepeakStarboard.height/2]))), 
           pm.TanksForepeakStarboard.length, pm.TanksForepeakStarboard.width, pm.TanksForepeakStarboard.height, opacity=0.1, color='red')

draw_frame_line(fig, frame_list_numpy_numbers[3], [0, 0, 0], [0, 0, pm.CraneBase.height], thickness=15)
draw_frame_line(fig, frame_list_numpy_numbers[4], [0, 0, 0], [0, 0, pm.Joint1Params.length], color='#4B0082')
draw_frame_line(fig, frame_list_numpy_numbers[5], [0, 0, 0], [-pm.Joint2Params.length, 0, 0], color="#F17D10")
draw_frame_line(fig, frame_list_numpy_numbers[6], [0, 0, 0], [-pm.Joint3Params.length, 0, 0], color="#10A329")
draw_frame_line(fig, frame_list_numpy_numbers[7], [0, 0, 0], [-(pm.Joint4Params.length+q_vals[9]), 0, 0], color="#C459B5")
draw_frame_line(fig, frame_list_numpy_numbers[8], [0, 0, 0], [0, 0, -2], color="#09DEFA")
draw_text_in_frame(fig, frame_list_numpy_numbers[0], [-0.1, -0.1, 0], 'origin')
draw_text_in_frame(fig, frame_list_numpy_numbers[1], [-0.1, -0.1, 0], 'NED')
draw_text_in_frame(fig, frame_list_numpy_numbers[2], [-0.1, -0.1, 0], 'body-fixed')
draw_text_in_frame(fig, frame_list_numpy_numbers[3], [-0.5, -0.1, 0.3] ,'crane-base', color='purple')
draw_text_in_frame(fig, frame_list_numpy_numbers[3], [-0.1, -0.1, -0.01] ,'q1', color='green')
draw_text_in_frame(fig, frame_list_numpy_numbers[4], [-0.1, -0.1, -0.01] ,'q2', color='green')
draw_text_in_frame(fig, frame_list_numpy_numbers[5], [-0.1, -0.1, -0.01] ,'q3', color='green')
draw_text_in_frame(fig, frame_list_numpy_numbers[6], [-0.1, -0.1, -0.01] ,'q4', color='green')
draw_text_in_frame(fig, frame_list_numpy_numbers[2], np.array(pm.TanksAftPortside.r).astype(float), 'ballast AFT portside')
draw_text_in_frame(fig, frame_list_numpy_numbers[2], np.array(pm.TanksAftStarboard.r).astype(float), 'ballast AFT starboard')
draw_text_in_frame(fig, frame_list_numpy_numbers[2], np.array(pm.TanksForepeakPortside.r).astype(float), 'ballast FP portside')
draw_text_in_frame(fig, frame_list_numpy_numbers[2], np.array(pm.TanksForepeakStarboard.r).astype(float), 'ballast FP starboard')

draw_frame_line(fig, frame_list_numpy_numbers[2], [pm.BoatParams.length/2,pm.BoatParams.width/2,0],[-pm.BoatParams.length/2,pm.BoatParams.width/2,0])
draw_frame_line(fig, frame_list_numpy_numbers[2], [pm.BoatParams.length/2,-pm.BoatParams.width/2,0],[-pm.BoatParams.length/2,-pm.BoatParams.width/2,0])
draw_frame_line(fig, frame_list_numpy_numbers[2], [pm.BoatParams.length/2,pm.BoatParams.width/2,0],[pm.BoatParams.length/2,-pm.BoatParams.width/2,0])
draw_frame_line(fig, frame_list_numpy_numbers[2], [-pm.BoatParams.length/2,pm.BoatParams.width/2,0],[-pm.BoatParams.length/2,-pm.BoatParams.width/2,0])

draw_frame_line(fig, frame_list_numpy_numbers[2], [pm.BoatParams.length/2,-pm.BoatParams.width/2,0],[pm.BoatParams.length/2,-pm.BoatParams.width/2,pm.BoatParams.height])
draw_frame_line(fig, frame_list_numpy_numbers[2], [pm.BoatParams.length/2,pm.BoatParams.width/2,0],[pm.BoatParams.length/2,pm.BoatParams.width/2,pm.BoatParams.height])
draw_frame_line(fig, frame_list_numpy_numbers[2], [-pm.BoatParams.length/2,pm.BoatParams.width/2,0],[-pm.BoatParams.length/2,pm.BoatParams.width/2,pm.BoatParams.height])
draw_frame_line(fig, frame_list_numpy_numbers[2], [-pm.BoatParams.length/2,-pm.BoatParams.width/2,0],[-pm.BoatParams.length/2,-pm.BoatParams.width/2,pm.BoatParams.height])

# Equal scale on all axes
fig.update_layout(
    scene=dict(
        aspectmode='data' 
    )
)

fig.show()