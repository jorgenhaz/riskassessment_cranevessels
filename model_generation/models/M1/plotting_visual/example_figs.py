from sympy import *
from sympy.physics.mechanics import*
from model_generation.kinematics.transformations import*
import numpy as np
from model_generation.plotting.plotting_3d import plot_3dframes, numpify, evaluate_frames, draw_frame_line, plot_point, draw_prism, draw_text_in_frame, draw_arrow, draw_curved_arrow
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
q_vals = [0.3, 0.3, 0.3, np.pi/3, -0.00090023, 0, -0.509349, 0.56633,-0.920672, 9, -0.00259331,0.353552]


T_world_frame = eye(4)
T_w_1 = T_world_frame * trans_x(x_n) * trans_y(y_n) * trans_z(z_n) * rot_x(phi) * rot_y(theta) 


frame_list = [T_world_frame, T_w_1]
frame_list_numpy = numpify(frame_list, q)
frame_list_numpy_numbers = evaluate_frames(frame_list_numpy, q_vals)

fig = go.Figure()

plot_3dframes(fig, frame_list_numpy_numbers, 0.3)

plot_point(fig, frame_list_numpy_numbers[1], [0.1, 0.1, 0.1], name='')
draw_text_in_frame(fig, frame_list_numpy_numbers[1], [0.1, 0.1, 0.1], text='b', color='black', size=16)

draw_frame_line(fig, frame_list_numpy_numbers[1], [0, 0, 0], [0.1, 0.1, 0.1], color='black', thickness=2)
draw_text_in_frame(fig, frame_list_numpy_numbers[1], [0.05, 0.05, 0.05], text='r<sub>b/i</sub>', size=14)
draw_text_in_frame(fig, frame_list_numpy_numbers[0], [0, 0, 0.3], text='frame n', size=16)
draw_text_in_frame(fig, frame_list_numpy_numbers[1], [0, 0, 0.3], text='frame i', size=16)
draw_text_in_frame(fig, frame_list_numpy_numbers[1], [-0.04, -0.04, -0.04], text='O', size=16)


# draw_arrow(fig, frame_list_numpy_numbers[1], [0,0,0], [-q_vals[0], 0, 0])


# draw_text_in_frame(fig, frame_list_numpy_numbers[0], [0, 0, 0.3], 'Frame i', size=16)
# plot_point(fig, frame_list_numpy_numbers[4], [0.0, 0.1, 0.1], name='')




# Equal scale on all axes
fig.update_layout(
    scene=dict(
        aspectmode='data' 
    )
)
fig.update_layout(
    scene=dict(
        aspectmode='data',
        xaxis=dict(range=[-1, 2], visible=False),
        yaxis=dict(range=[-1, 2], visible=False),
        zaxis=dict(range=[-1, 2], visible=False)
    )
)


fig.update_layout(showlegend=False)




fig.show()

# from sympy import *
# from sympy.physics.mechanics import*
# from model_generation.kinematics.transformations import*
# import numpy as np
# from model_generation.plotting.plotting_3d import plot_3dframes, numpify, evaluate_frames, draw_frame_line, plot_point, draw_prism, draw_text_in_frame, draw_arrow, draw_curved_arrow
# import model_generation.models.model_2.quasi_variable_cog.params as pm
# import plotly.graph_objects as go
# import model_generation.utils.utils as util

# # Euler angles of boat
# phi, theta, psi = symbols('phi theta psi')
# # Positions of boat
# x_n, y_n, z_n = symbols('x y n')
# # Crane joints
# q1, q2, q3, q4, q1_p, q2_p = symbols('q1 q2 q3 q4 q1_p q2_p')

# q = Matrix([x_n, y_n, z_n, phi, theta, psi, q1, q2, q3, q4, q1_p, q2_p])
# q_vals = [0.7, 0.7, 0.7, np.pi/3, -0.00090023, 0, -0.509349, 0.56633,-0.920672, 9, -0.00259331,0.353552]


# T_world_frame = eye(4)
# T_w_1 = T_world_frame * trans_x(x_n)
# T_w_2 = T_w_1 * trans_y(y_n)
# T_w_3 = T_w_2 * trans_z(z_n)
# T_w_4 = T_w_3 * rot_x(phi)


# frame_list = [T_world_frame, T_w_1, T_w_2, T_w_3, T_w_4]
# frame_list_numpy = numpify(frame_list, q)
# frame_list_numpy_numbers = evaluate_frames(frame_list_numpy, q_vals)

# fig = go.Figure()

# plot_3dframes(fig, frame_list_numpy_numbers, 0.3)

# draw_arrow(fig, frame_list_numpy_numbers[1], [0,0,0], [-q_vals[0], 0, 0])
# draw_arrow(fig, frame_list_numpy_numbers[2], [0,0,0], [0, -q_vals[1], 0])
# draw_arrow(fig, frame_list_numpy_numbers[3], [0,0,0], [0, 0, -q_vals[2]])
# draw_curved_arrow(fig, frame_list_numpy_numbers[3], frame_list_numpy_numbers[4])


# draw_text_in_frame(fig, frame_list_numpy_numbers[0], [0, 0, 0.3], 'Frame i', size=16)
# draw_text_in_frame(fig, frame_list_numpy_numbers[1], [0, 0, 0.3], 'Frame i+1', size=16)
# draw_text_in_frame(fig, frame_list_numpy_numbers[2], [0, 0, 0.3], 'Frame i+2', size=16)
# draw_text_in_frame(fig, frame_list_numpy_numbers[3], [0, 0, 0.3], 'Frame i+3', size=16)
# draw_text_in_frame(fig, frame_list_numpy_numbers[4], [0, -0.1, 0.3], 'Frame n', size=16)
# draw_text_in_frame(fig, frame_list_numpy_numbers[0], [-0.02, 0, 0.2], 'Z', size=16, color='blue')
# draw_text_in_frame(fig, frame_list_numpy_numbers[0], [0.2, 0, 0.02], 'X', size=16, color='red')
# draw_text_in_frame(fig, frame_list_numpy_numbers[0], [0.02, 0.2, 0.0], 'Y', size=16, color='green')
# plot_point(fig, frame_list_numpy_numbers[4], [0.0, 0.1, 0.1], name='')
# draw_text_in_frame(fig, frame_list_numpy_numbers[4], [0.0, 0.08, 0.12], text='p<sub>n</sub>', size=16)



# # Equal scale on all axes
# fig.update_layout(
#     scene=dict(
#         aspectmode='data' 
#     )
# )
# fig.update_layout(
#     scene=dict(
#         aspectmode='data',
#         xaxis=dict(range=[-1, 2], visible=False),
#         yaxis=dict(range=[-1, 2], visible=False),
#         zaxis=dict(range=[-1, 2], visible=False)
#     )
# )


# fig.update_layout(showlegend=False)




# fig.show()