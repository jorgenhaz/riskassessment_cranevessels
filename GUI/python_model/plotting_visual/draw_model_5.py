from sympy import *
from sympy.physics.mechanics import*
from model_generation.kinematics.transformations import*
import numpy as np
from model_generation.plotting.plotting_3d import plot_3dframes, numpify, evaluate_frames, draw_frame_line, plot_point, draw_prism, draw_text_in_frame
import model_generation.models.M5.variable_cg.params as pm
import plotly.graph_objects as go
import model_generation.utils.utils as util
import yaml

# Euler angles of boat
phi, theta, psi = symbols('phi theta psi')
# Positions of boat
x_n, y_n, z_n = symbols('x y n')

q = Matrix([x_n, y_n, z_n, phi, theta, psi])

with open('cpp_gui/files/init.yaml', 'r') as file:
    params = yaml.safe_load(file)

x_yaml              = params['x']
y_yaml              = params['y']
z_yaml              = params['z']
roll_yaml           = params['phi']
pitch_yaml          = params['theta']
yaw_yaml            = params['psi']



q_vals = [x_yaml, y_yaml, z_yaml, roll_yaml, pitch_yaml, yaw_yaml]


T_world_frame = eye(4)
T_NED_frame = T_world_frame * trans_z(0) * trans_x(1) * trans_y(1) * rot_x(np.pi)
T_n_b = T_NED_frame * trans_x(x_n) * trans_y(y_n) * trans_z(z_n) * rot_z(psi) * rot_y(theta) * rot_x(phi)


frame_list = [T_world_frame, T_NED_frame, T_n_b]
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

draw_text_in_frame(fig, frame_list_numpy_numbers[0], [-0.1, -0.1, 0], 'origin')
draw_text_in_frame(fig, frame_list_numpy_numbers[1], [-0.1, -0.1, 0], 'NED')
draw_text_in_frame(fig, frame_list_numpy_numbers[2], [-0.1, -0.1, 0], 'body-fixed')
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
fig.update_layout(
    paper_bgcolor='white',       
    plot_bgcolor='white',        
    scene=dict(
        bgcolor='white',       
        xaxis=dict(showbackground=False,
                   showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showbackground=False,
                   showgrid=False, zeroline=False, visible=False),
        zaxis=dict(showbackground=False,
                   showgrid=False, zeroline=False, visible=False),
        aspectmode='data'
    ),
    margin=dict(l=0, r=0, b=0, t=0)  
)


fig.update_layout(showlegend=False)
fig.show()