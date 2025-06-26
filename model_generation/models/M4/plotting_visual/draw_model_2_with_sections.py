from sympy import *
from sympy.physics.mechanics import*
from model_generation.kinematics.transformations import*
import numpy as np
from model_generation.plotting.plotting_3d import plot_3dframes, numpify, evaluate_frames, draw_frame_line, plot_point, draw_prism, draw_text_in_frame
import model_generation.models.model_3.quasi_variable_cog.params as pm
import plotly.graph_objects as go
import model_generation.utils.utils as util

# Euler angles of boat
phi, theta, psi = symbols('phi theta psi')
# Positions of boat
x_n, y_n, z_n = symbols('x y n')
# Crane joints
q1 = symbols('q1')

q = Matrix([x_n, y_n, z_n, phi, theta, psi, q1])
q_vals = [15, 15, 0, 0.1, 0.1, 0.1, 0]

T_world_frame = eye(4)
T_NED_frame = T_world_frame * trans_z(0) * trans_x(1) * trans_y(1) * rot_x(np.pi)
T_n_b = T_NED_frame * trans_x(x_n) * trans_y(y_n) * trans_z(z_n) * rot_z(psi) * rot_y(theta) * rot_x(phi)
T_n_cb = T_n_b * trans_x(pm.CraneBase.x) * trans_y(pm.CraneBase.y) * trans_z(-pm.CraneBase.height)
T_n_q1 = T_n_cb * rot_x(q1) * trans_z(-pm.Joint1Params.length)

frame_list = [T_world_frame, T_NED_frame, T_n_b]
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
point_cog_b = np.array([0.5, 1.0, 1.0])

r_k_vectors = []
plot_point(fig, frame_list_numpy_numbers[2], point_cog_b.tolist(), color='red', size=4, name="CG")

for i in range(length_sections):
    for j in range(width_sections):
        offset = np.array([-pm.BoatParams.length/2+(i)*section_length + section_length/2, -pm.BoatParams.width/2+(j)*section_width+section_width/2, pm.BoatParams.height])
        body_frame_points.append(offset)
        if (i+j)%2==0:
            draw_prism(fig, frame_list_numpy_numbers[2], section_length, section_width, 0.1, 'yellow', opacity=0.3, offset=offset)
        else:
            draw_prism(fig, frame_list_numpy_numbers[2], section_length, section_width, 0.1, 'green', opacity=0.3, offset=offset)
        plot_point(fig, frame_list_numpy_numbers[2], offset.tolist(), color='cyan', size=2, name=f"{i+1},{j+1}")
        plot_point(fig, frame_list_numpy_numbers[2], offset.tolist(), color='cyan', size=2)
        draw_frame_line(fig, frame_list_numpy_numbers[2], point_cog_b.tolist(), offset.tolist(), color='purple', thickness=1)
        r_k_vectors.append(offset-point_cog_b)
        
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