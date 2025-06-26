from sympy import *
from sympy.physics.mechanics import*
from model_generation.kinematics.transformations import*
import numpy as np
from model_generation.plotting.plotting_3d import plot_3dframes, numpify, evaluate_frames, draw_frame_line, plot_point, draw_prism, draw_text_in_frame
import model_generation.models.M5.variable_cg.params as pm
import plotly.graph_objects as go
import model_generation.utils.utils as util

# Euler angles of boat
phi, theta, psi = symbols('phi theta psi')
# Positions of boat
x_n, y_n, z_n = symbols('x y n')
# Crane joints
q1, q2, q3, q4 = symbols('q1 q2 q3 q4')

q = Matrix([x_n, y_n, z_n, phi, theta, psi, q1, q2, q3, q4])
q_vals = [15, 15, 0, 0.0, 0.0, 0.0, 
          -2.8, 1.0, -0.5, 4.0]

T_world_frame = eye(4)
T_NED_frame = T_world_frame * trans_z(0) * trans_x(1) * trans_y(1) * rot_x(np.pi)
T_n_b = T_NED_frame * trans_x(x_n) * trans_y(y_n) * trans_z(z_n) * rot_z(psi) * rot_y(theta) * rot_x(phi)
T_n_cb = T_n_b * trans_x(pm.CraneBase.x) * trans_y(pm.CraneBase.y) * trans_z(-pm.CraneBase.height)
T_n_q1 = T_n_cb * rot_z(q1) * trans_z(-pm.Joint1Params.length)
T_n_q2 = T_n_q1 * rot_y(q2) * trans_x(pm.Joint2Params.length)
T_n_q3 = T_n_q2 * rot_y(q3) * trans_x(pm.Joint3Params.length)
T_n_q4 = T_n_q3 * trans_x(q4 + pm.Joint4Params.length)

frame_list = [T_world_frame, T_NED_frame, T_n_b, T_n_cb, T_n_q1, T_n_q2, T_n_q3, T_n_q4]
frame_list_numpy = numpify(frame_list, q)
frame_list_numpy_numbers = evaluate_frames(frame_list_numpy, q_vals)

fig = go.Figure()

width_sections = 4
length_sections = 10
total_sections = width_sections * length_sections
section_length = pm.BoatParams.length/length_sections
section_width = pm.BoatParams.width/width_sections

plot_3dframes(fig, frame_list_numpy_numbers, 0.3)
# draw boat
draw_prism(fig, frame_list_numpy_numbers[2], pm.BoatParams.length, pm.BoatParams.width, pm.BoatParams.height, opacity=0.1, offset=np.array([0, 0, pm.BoatParams.height/2]))

body_frame_points = []
point_cog_b = np.array([0.5, 1.0, 2.0])

r_k_vectors = []
plot_point(fig, frame_list_numpy_numbers[2], point_cog_b.tolist(), color='red', size=4, name="")
draw_text_in_frame(fig, frame_list_numpy_numbers[2], (point_cog_b+np.array([0, 0, 1.0])).tolist(), text='CG')
plot_point(fig, frame_list_numpy_numbers[2], [0, 0, pm.BoatParams.height/2], color='yellow', size=4, name="")
plot_point(fig, frame_list_numpy_numbers[2],[float(pm.TanksAftPortside.r[0]), 
                 float(pm.TanksAftPortside.r[1]), 
                 pm.TanksAftPortside.height/2], color='yellow', size=4, name="")
plot_point(fig, frame_list_numpy_numbers[2],[float(pm.TanksAftStarboard.r[0]), 
                 float(pm.TanksAftStarboard.r[1]), 
                 pm.TanksAftStarboard.height/2], color='yellow', size=4, name="")
plot_point(fig, frame_list_numpy_numbers[2],[float(pm.TanksForepeakPortside.r[0]), 
                 float(pm.TanksForepeakPortside.r[1]), 
                 pm.TanksForepeakPortside.height/2],  color='yellow', size=4, name="")
plot_point(fig, frame_list_numpy_numbers[2],[float(pm.TanksForepeakStarboard.r[0]), 
                 float(pm.TanksForepeakStarboard.r[1]), 
                 pm.TanksForepeakStarboard.height/2],  color='yellow', size=4, name="")


draw_prism(fig, util.add_point_se3(frame_list_numpy_numbers[2], (pm.TanksAftPortside.r+Matrix([0, 0, pm.TanksAftPortside.height/2]))), 
           pm.TanksAftPortside.length, pm.TanksAftPortside.width, pm.TanksAftPortside.height, opacity=0.1, color='red')
draw_prism(fig, util.add_point_se3(frame_list_numpy_numbers[2],(pm.TanksAftStarboard.r+Matrix([0, 0, pm.TanksAftStarboard.height/2]))), 
           pm.TanksAftStarboard.length, pm.TanksAftStarboard.width, pm.TanksAftStarboard.height, opacity=0.1, color='red')
draw_prism(fig, util.add_point_se3(frame_list_numpy_numbers[2], (pm.TanksForepeakPortside.r+Matrix([0, 0, pm.TanksForepeakPortside.height/2]))), 
           pm.TanksForepeakPortside.length, pm.TanksForepeakPortside.width, pm.TanksForepeakPortside.height, opacity=0.1, color='red')
draw_prism(fig, util.add_point_se3(frame_list_numpy_numbers[2], (pm.TanksForepeakStarboard.r+Matrix([0, 0, pm.TanksForepeakStarboard.height/2]))), 
           pm.TanksForepeakStarboard.length, pm.TanksForepeakStarboard.width, pm.TanksForepeakStarboard.height, opacity=0.1, color='red')

draw_frame_line(fig, frame_list_numpy_numbers[3], [0, 0, 0], [0, 0, pm.CraneBase.height], thickness=15)
draw_frame_line(fig, frame_list_numpy_numbers[4], [0, 0, 0], [0, 0, pm.Joint1Params.length], color='black', thickness=8)
draw_frame_line(fig, frame_list_numpy_numbers[5], [0, 0, 0], [-pm.Joint2Params.length, 0, 0], color="black", thickness=8)
draw_frame_line(fig, frame_list_numpy_numbers[6], [0, 0, 0], [-pm.Joint3Params.length, 0, 0], color="black", thickness=8)
draw_frame_line(fig, frame_list_numpy_numbers[7], [0, 0, 0], [-(pm.Joint4Params.length+q_vals[9]), 0, 0], color="black", thickness=8)

draw_frame_line(fig, frame_list_numpy_numbers[2], point_cog_b.tolist(), 
                [float(pm.TanksAftPortside.r[0]), 
                 float(pm.TanksAftPortside.r[1]), 
                 pm.TanksAftPortside.height/2], 
                color='purple', thickness=4)
draw_frame_line(fig, frame_list_numpy_numbers[2], point_cog_b.tolist(), 
                [float(pm.TanksAftStarboard.r[0]), 
                 float(pm.TanksAftStarboard.r[1]), 
                 pm.TanksAftStarboard.height/2], 
                color='purple', thickness=4)
draw_frame_line(fig, frame_list_numpy_numbers[2], point_cog_b.tolist(), 
                [float(pm.TanksForepeakPortside.r[0]), 
                 float(pm.TanksForepeakPortside.r[1]), 
                 pm.TanksForepeakPortside.height/2], 
                color='purple', thickness=4)
draw_frame_line(fig, frame_list_numpy_numbers[2], point_cog_b.tolist(), 
                [float(pm.TanksForepeakStarboard.r[0]), 
                 float(pm.TanksForepeakStarboard.r[1]), 
                 pm.TanksForepeakStarboard.height/2], 
                color='purple', thickness=4)
draw_frame_line(fig, frame_list_numpy_numbers[2],
                [0, 0, pm.BoatParams.height/2],
                point_cog_b.tolist(),
                color='purple', thickness=4)

point_cog_b = np.array([0.5, 1.0, 2.0, 1])
plot_point(fig, frame_list_numpy_numbers[7], [-(q_vals[9]+pm.Joint4Params.length)/2, 0, 0], color='yellow')
plot_point(fig, frame_list_numpy_numbers[6], [-(pm.Joint3Params.length)/2, 0, 0], color='yellow')
plot_point(fig, frame_list_numpy_numbers[5], [-(pm.Joint2Params.length)/2, 0, 0], color='yellow')
plot_point(fig, frame_list_numpy_numbers[4], [0, 0, pm.Joint1Params.length/2], color='yellow')
draw_frame_line(fig, frame_list_numpy_numbers[0],
                (frame_list_numpy_numbers[7]) @ [-(q_vals[9]+pm.Joint4Params.length)/2, 0, 0, 1],
                frame_list_numpy_numbers[2] @ point_cog_b,
                color='purple', thickness=4)
draw_frame_line(fig, frame_list_numpy_numbers[0],
                (frame_list_numpy_numbers[6]) @ [-(pm.Joint3Params.length)/2, 0, 0, 1],
                frame_list_numpy_numbers[2] @ point_cog_b,
                color='purple', thickness=4)
draw_frame_line(fig, frame_list_numpy_numbers[0],
                (frame_list_numpy_numbers[5]) @ [-(pm.Joint2Params.length)/2, 0, 0,1],
                frame_list_numpy_numbers[2] @ point_cog_b,
                color='purple', thickness=4)
draw_frame_line(fig, frame_list_numpy_numbers[0],
                (frame_list_numpy_numbers[4]) @ [0, 0, pm.Joint1Params.length/2, 1],
                frame_list_numpy_numbers[2] @ point_cog_b,
                color='purple', thickness=4)

        
draw_frame_line(fig, frame_list_numpy_numbers[2], [pm.BoatParams.length/2,pm.BoatParams.width/2,0],[-pm.BoatParams.length/2,pm.BoatParams.width/2,0])
draw_frame_line(fig, frame_list_numpy_numbers[2], [pm.BoatParams.length/2,-pm.BoatParams.width/2,0],[-pm.BoatParams.length/2,-pm.BoatParams.width/2,0])
draw_frame_line(fig, frame_list_numpy_numbers[2], [pm.BoatParams.length/2,pm.BoatParams.width/2,0],[pm.BoatParams.length/2,-pm.BoatParams.width/2,0])
draw_frame_line(fig, frame_list_numpy_numbers[2], [-pm.BoatParams.length/2,pm.BoatParams.width/2,0],[-pm.BoatParams.length/2,-pm.BoatParams.width/2,0])

draw_frame_line(fig, frame_list_numpy_numbers[2], [pm.BoatParams.length/2,-pm.BoatParams.width/2,0],[pm.BoatParams.length/2,-pm.BoatParams.width/2,pm.BoatParams.height])
draw_frame_line(fig, frame_list_numpy_numbers[2], [pm.BoatParams.length/2,pm.BoatParams.width/2,0],[pm.BoatParams.length/2,pm.BoatParams.width/2,pm.BoatParams.height])
draw_frame_line(fig, frame_list_numpy_numbers[2], [-pm.BoatParams.length/2,pm.BoatParams.width/2,0],[-pm.BoatParams.length/2,pm.BoatParams.width/2,pm.BoatParams.height])
draw_frame_line(fig, frame_list_numpy_numbers[2], [-pm.BoatParams.length/2,-pm.BoatParams.width/2,0],[-pm.BoatParams.length/2,-pm.BoatParams.width/2,pm.BoatParams.height])
# draw_text_in_frame(fig, frame_list_numpy_numbers[0], [-0.1, -0.1, 0], 'origin')
draw_text_in_frame(fig, frame_list_numpy_numbers[1], [-0.1, -0.1, 0], 'NED')
draw_text_in_frame(fig, frame_list_numpy_numbers[2], [-0.1, -0.1, 0], 'b')

# Equal scale on all axes
fig.update_layout(
    scene=dict(
        aspectmode='data' 
    )
)

fig.update_layout(
    paper_bgcolor='white',       # hele figur­området
    plot_bgcolor='white',        # selve “canvaset”
    scene=dict(
        bgcolor='white',         # 3-D-scenen
        xaxis=dict(showbackground=False,
                   showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showbackground=False,
                   showgrid=False, zeroline=False, visible=False),
        zaxis=dict(showbackground=False,
                   showgrid=False, zeroline=False, visible=False),
        aspectmode='data'
    ),
    margin=dict(l=0, r=0, b=0, t=0)  # fjern ramme
)


fig.update_layout(showlegend=False)

fig.show()