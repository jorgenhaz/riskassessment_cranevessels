from datetime import datetime
from sympy import *
from model_generation.kinematics.transformations import*
import model_generation.cpp_write.cpp_write as cppw
import model_generation.models.M2.constant_cg.params as pm
from model_generation.models.M2.waves.wave_utils import jonswap_spectrum, dynamical_pressure_field, wave_accelerations
import yaml
import matplotlib.pyplot as plt
import numpy as np

startTimeTotal = datetime.now()
np.random.seed(42)

with open('model_generation/models/M2/waves/wave_model_input.yaml', 'r') as file:
    params = yaml.safe_load(file)

Hs              = params['wave_data']['Hs']
Tp              = params['wave_data']['Tp']
Gamma           = params['wave_data']['gamma']
N               = params['wave_data']['N']
f_min           = params['wave_data']['f_min']
f_max           = params['wave_data']['f_max']
sections_width  = params['boat_sections']['sections_width']
sections_length = params['boat_sections']['sections_length']

"""_____Panel-coordinates and vectors between CG and panels_____"""

# Generalized coordinates and time
phi, theta, psi = symbols('phi theta psi')
x_n, y_n, z_n = symbols('x y z')
t = symbols('t')
# Free variables for mass in ballast tanks
m_aft_ps, m_aft_stb, m_fp_ps, m_fp_stb = symbols('m_aft_ps m_aft_stb m_fp_ps m_fp_stb')

# Forward kinematics
T_n_b = simplify(trans_x(x_n) * trans_y(y_n) * trans_z(z_n) * rot_z(psi) * rot_y(theta) * rot_x(phi))
R_n_b = T_n_b[:3,:3]

# Variable vectors for C++-generation
all_vars = Matrix([x_n, y_n, z_n, phi, theta, psi, t])
cog_vars = Matrix([m_fp_stb, m_fp_ps, m_aft_stb, m_aft_ps])

# Calculate sections
total_sections = sections_width * sections_length
section_length = pm.BoatParams.length/sections_length
section_width = pm.BoatParams.width/sections_width
area_section = section_length*section_width

body_frame_points = []
r_k_vectors       = []

# Heights of tanks
h_aft_ps = m_aft_ps / (pm.BoatParams.rho * pm.TanksAftPortside.length * pm.TanksAftPortside.width)
h_aft_stb = m_aft_stb / (pm.BoatParams.rho * pm.TanksAftStarboard.length * pm.TanksAftStarboard.width)
h_fp_ps = m_fp_ps / (pm.BoatParams.rho * pm.TanksForepeakPortside.length * pm.TanksForepeakPortside.width)
h_fp_stb = m_fp_stb / (pm.BoatParams.rho * pm.TanksForepeakStarboard.length * pm.TanksForepeakStarboard.width)
# CG vectors of tanks (from origo of body)
r_tank_aft_ps = (pm.TanksAftPortside.r + Matrix([0, 0, 2 - h_aft_ps/2])).subs(m_aft_ps, 1500)
r_tank_aft_stb = (pm.TanksAftStarboard.r + Matrix([0, 0, 2 - h_aft_stb/2])).subs(m_aft_stb, 1500)
r_tank_fp_ps = (pm.TanksForepeakPortside.r + Matrix([0, 0, 2 - h_fp_ps/2])).subs(m_fp_ps, 1500)
r_tank_fp_stb = (pm.TanksForepeakStarboard.r + Matrix([0, 0, 2 - h_fp_stb/2])).subs(m_fp_stb, 1500)

# Total CG of boat
mass_boat = pm.BoatParams.mass + 1500 + 1500 + 1500 + 1500
r_CO_CG = (
    pm.BoatParams.mass * pm.BoatParams.r
    + 1500 * r_tank_aft_ps
    + 1500 * r_tank_aft_stb
    + 1500 * r_tank_fp_ps
    + 1500 * r_tank_fp_stb
) / mass_boat

# Calculating panel-positions and vector between position and CG (CG -> panel)
for i in range(sections_length):
    for j in range(sections_width):
        offset = Matrix([-pm.BoatParams.length/2 + section_length*(i) + section_length/2,
                         -pm.BoatParams.width/2 + section_width*(j) + section_width/2,
                         pm.BoatParams.height])
        body_frame_points.append(offset-Matrix([0, 0, pm.BoatParams.height])) # Have to substract the height to get correct position in global
        r_k_vectors.append(offset-r_CO_CG)

body_frame_points = Matrix.hstack(*body_frame_points)
body_frame_points = body_frame_points.col_join(ones(1,(body_frame_points.cols)))
r_k_vectors = Matrix.hstack(*r_k_vectors) # Vectors CG -> panel

world_frame_points = T_n_b * body_frame_points
world_frame_points = (world_frame_points[:3,:]) # World-frame coordinates of panels

# Generating transformation-matrix and vectors
filepath_cpp = "../code/cpp_sim_testing/M2_wave/src"
filepath_h = "../code/cpp_sim_testing/M2_wave/include"
cppw.generate_cpp_files(world_frame_points, 'worldframepoints', all_vars, filepath_cpp, filepath_h)
cppw.generate_cpp_files(r_k_vectors, "vectors_cog",cog_vars, filepath_cpp, filepath_h)
cppw.generate_cpp_files(R_n_b, "R_n_b", all_vars, filepath_cpp, filepath_h)

"""_____Dynamic pressure and accelerations_____"""

x, y, z, t, wave_angle = symbols('x y z t, wave_angle')
pd_vars = Matrix([x, y,  z, t, wave_angle])
p_D, S_omega, omega, a, epsilons = (dynamical_pressure_field(Hs=Hs, Tp=Tp, gamma=Gamma, N=N, f_min=f_min, f_max=f_max))
p_D = area_section * p_D
wave_acc = (1/(total_sections)) * wave_accelerations(omega, a, epsilons)

cppw.generate_cpp_files(p_D, 'dynamic_pressure', pd_vars, filepath_cpp, filepath_h)
cppw.generate_cpp_files(wave_acc, 'wave_accelerations', pd_vars, filepath_cpp, filepath_h)

print("Accumulated total time: ", datetime.now()-startTimeTotal)