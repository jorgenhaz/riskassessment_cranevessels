from sympy import *
from sympy.physics.mechanics import*
from model_generation.kinematics.transformations import*
import numpy as np
from model_generation.plotting.plotting_3d import plot_3dframes, numpify, evaluate_frames, draw_frame_line, plot_point, draw_prism, draw_text_in_frame, draw_arrow
import model_generation.models.M3.variable_cg.params as pm
import plotly.graph_objects as go
import model_generation.utils.utils as util

# Euler angles of boat
phi, theta, psi = symbols('phi theta psi')
# Positions of boat
x_n, y_n, z_n = symbols('x y n')
# Crane joints
q1, q2, q3, q4, q1_p, q2_p = symbols('q1 q2 q3 q4 q1_p q2_p')




q = Matrix([x_n, y_n, z_n, phi, theta, psi, q1, q2, q3, q4, q1_p, q2_p])


T_world_frame = eye(4)
T_NED_frame = T_world_frame * trans_x(1) * trans_y(1) * rot_x(np.pi)
T_n_b = T_NED_frame * trans_x(x_n) * trans_y(y_n) * trans_z(z_n) * rot_z(psi) * rot_y(theta) * rot_x(phi)
T_n_cb = T_n_b * trans_x(pm.CraneBase.x) * trans_y(pm.CraneBase.y) * trans_z(-pm.CraneBase.height)
T_n_q1 = T_n_cb * rot_z(q1) * trans_z(-pm.Joint1Params.length)
T_n_q2 = T_n_q1 * rot_y(q2) * trans_x(pm.Joint2Params.length)
T_n_q3 = T_n_q2 * rot_y(q3) * trans_x(pm.Joint3Params.length)
T_n_q4 = T_n_q3 * trans_x(q4 + pm.Joint4Params.length)
T_n_payload = T_n_q4 * rot_x(q1_p) * rot_y(q2_p) * trans_z(3)

"""Align pendulum using base-to-tip transformation"""
subs_dict = {
    x_n: 0.0, y_n: -0.0, z_n: 0.524761,
    phi: -0.0, theta: -0.0, psi: 0.0,
    q1: -1.0, q2: 1.0, q3: -0.6, q4: 2.0,
    q1_p: 0.0, q2_p: -0.0
}

"""Finding straight down hanging pendulum"""
R_n_tip = (T_n_q4 * rot_x(q1_p) * rot_y(q2_p))[:3, :3]
R_tip_n = R_n_tip.T

g_n = Matrix([0, 0, -1])        
g_t = R_tip_n * g_n

gx, gy, gz = g_t.evalf(subs=subs_dict)

q1_p_init = float(atan2(gy, gz))
q2_p_init = float(atan2(gx, sqrt(gy**2 + gz**2)))

print(q1_p_init)
print(q2_p_init)



q_vals = [subs_dict[x_n], subs_dict[y_n], subs_dict[z_n], 
          subs_dict[phi], subs_dict[theta], subs_dict[psi], 
          subs_dict[q1], subs_dict[q2], subs_dict[q3], subs_dict[q4], 
          (q1_p_init),(q2_p_init)]

frame_list = [T_world_frame, T_NED_frame, T_n_b]
frame_list_numpy = numpify(frame_list, q)
frame_list_numpy_numbers = evaluate_frames(frame_list_numpy, q_vals)

fig = go.Figure()

plot_3dframes(fig, frame_list_numpy_numbers, 0.3)
draw_prism(fig, frame_list_numpy_numbers[2], pm.BoatParams.length, pm.BoatParams.width, pm.BoatParams.height, opacity=0.1, offset=np.array([0, 0, pm.BoatParams.height/2]))



draw_frame_line(fig, frame_list_numpy_numbers[2], [pm.BoatParams.length/2,pm.BoatParams.width/2,0],[-pm.BoatParams.length/2,pm.BoatParams.width/2,0])
draw_frame_line(fig, frame_list_numpy_numbers[2], [pm.BoatParams.length/2,-pm.BoatParams.width/2,0],[-pm.BoatParams.length/2,-pm.BoatParams.width/2,0])
draw_frame_line(fig, frame_list_numpy_numbers[2], [pm.BoatParams.length/2,pm.BoatParams.width/2,0],[pm.BoatParams.length/2,-pm.BoatParams.width/2,0])
draw_frame_line(fig, frame_list_numpy_numbers[2], [-pm.BoatParams.length/2,pm.BoatParams.width/2,0],[-pm.BoatParams.length/2,-pm.BoatParams.width/2,0])

draw_frame_line(fig, frame_list_numpy_numbers[2], [pm.BoatParams.length/2,-pm.BoatParams.width/2,0],[pm.BoatParams.length/2,-pm.BoatParams.width/2,pm.BoatParams.height])
draw_frame_line(fig, frame_list_numpy_numbers[2], [pm.BoatParams.length/2,pm.BoatParams.width/2,0],[pm.BoatParams.length/2,pm.BoatParams.width/2,pm.BoatParams.height])
draw_frame_line(fig, frame_list_numpy_numbers[2], [-pm.BoatParams.length/2,pm.BoatParams.width/2,0],[-pm.BoatParams.length/2,pm.BoatParams.width/2,pm.BoatParams.height])
draw_frame_line(fig, frame_list_numpy_numbers[2], [-pm.BoatParams.length/2,-pm.BoatParams.width/2,0],[-pm.BoatParams.length/2,-pm.BoatParams.width/2,pm.BoatParams.height])

angle_1 = np.deg2rad(70+180)  # simulation 1
angle_2 = np.deg2rad(10+180)  # simulation 2

length = 1.5  # lengde på pilen (valgfri)

# Enhetsvektorer for bølgeretningene
dir_1 = -length * np.array([np.cos(angle_1), np.sin(angle_1), 0])
dir_2 = -length * np.array([np.cos(angle_2), np.sin(angle_2), 0])

# Posisjon hvor pilene skal starte (utenfor båten)
origin_1 = np.array([2.0, 5.3, 0.0])  # juster hvis nødvendig
origin_2 = np.array([2.0, 5.3, 0.0])  # juster hvis nødvendig

draw_arrow(fig, frame_list_numpy_numbers[0], origin_1, 3*dir_1, color='red', shaft_width=8, head_length=0.4)
draw_arrow(fig, frame_list_numpy_numbers[0], origin_2, 3*dir_2, color='blue', shaft_width=8, head_length=0.4)

draw_text_in_frame(fig, frame_list_numpy_numbers[0], origin_1 + dir_1*1.05 + np.array([-0.3, 1.2, 0.1]), "70°", size=32, color='red')
draw_text_in_frame(fig, frame_list_numpy_numbers[0], origin_2 + dir_2*1.05 + np.array([0, 1, 0.1]), "10°", size=32, color='blue')


# Equal scale on all axes
fig.update_layout(
    scene=dict(
        aspectmode='data' 
    )
)

fig.update_layout(
    scene_camera=dict(
        eye=dict(x=0, y=0, z=2),     # Se rett ned langs z-aksen
        up=dict(x=-1, y=0, z=1),      # Oppretning langs z
        center=dict(x=0, y=0, z=0)   # Senter av scenen
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