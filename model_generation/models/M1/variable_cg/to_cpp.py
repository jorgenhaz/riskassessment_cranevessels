"""
Quasi-Lagrange formulated model
6 DoF boat
4 DoF crane (3 rotational and 1 prismatic joint)
2 DoF pendulum (spherical pendulum)
"""

from datetime import datetime
from sympy import *
from sympy.physics.mechanics import*
from model_generation.kinematics.transformations import*
from model_generation.kinematics.joint_type import JointType
from model_generation.kinematics.jacobian import jacobian
import model_generation.cpp_write.cpp_write as cppw
from model_generation.utils.utils import pad_matrix, inverse_se3
import model_generation.models.M1.variable_cg.params as pm

startTimeTotal = datetime.now()

g_vec = Matrix([0, 0, pm.Gravity.g])

# Euler angles
phi, theta, psi = symbols('phi theta psi')
# Position variables
x_n, y_n, z_n = symbols('x y z')

# Body-fixed velocities
uq, vq, wq, pq, qq, rq = symbols('u v w p q r')

# State-vectors
q = Matrix([x_n, y_n, z_n, phi, theta, psi])
omega = Matrix([uq, vq, wq, pq, qq, rq])

# External forces
tau_xn, tau_yn, tau_zn, tau_phi, tau_theta, tau_psi = symbols('tau_xn tau_yn tau_zn tau_phi tau_theta tau_psi')

# Mass in ballast tanks - variables
m_fp_stb, m_fp_ps, m_aft_stb, m_aft_ps = symbols('m_fp_stb m_fp_ps m_aft_stb m_aft_ps')
ballast_array = Matrix([m_fp_stb, m_fp_ps, m_aft_stb, m_aft_ps])

# All variables for cpp-code
all_vars = Matrix([x_n, y_n, z_n, phi, theta, psi,
                   uq, vq, wq, pq, qq, rq, 
                   tau_xn, tau_yn, tau_zn, tau_phi, tau_theta, tau_psi, 
                   m_fp_stb, m_fp_ps, m_aft_stb, m_aft_ps])

"""_____Kinematics_____"""
# From NED to body-fixed frame
T_n_xn = trans_x(x_n)
T_n_yn = simplify(T_n_xn * trans_y(y_n))
T_n_zn = simplify(T_n_yn * trans_z(z_n))
T_n_psi = simplify(T_n_zn * rot_z(psi))
T_n_theta = simplify(T_n_psi * rot_y(theta))
T_n_b = simplify(trans_x(x_n) * trans_y(y_n) * trans_z(z_n) * rot_z(psi) * rot_y(theta) * rot_x(phi))
R_n_b = T_n_b[:3,:3]

"""_____betta, alpha_T, betta_T and gamma_____"""
R_0_B = simplify(T_n_b[:3,:3])

T_B_0 = inverse_se3(T_n_b)
T_B_0_rot = simplify(T_B_0 * trans_z(z_n) * trans_y(y_n) * trans_x(x_n)) # Removing the translational DoF's
T_B_psi = simplify(T_B_0_rot * rot_z(psi))
T_B_theta = simplify(T_B_psi * rot_y(theta))

transformList = [T_B_theta, T_B_psi, T_B_0_rot]
rotAxList = [
    pm.UnitVectors.i,
    pm.UnitVectors.j,
    pm.UnitVectors.k
]
jointTypeList = [
    JointType.REVOLUTE,
    JointType.REVOLUTE,
    JointType.REVOLUTE
]
jointVec = Matrix([phi, theta, psi])
alpha_T_rot = simplify(jacobian(transformList, rotAxList, jointTypeList, jointVec))[3:,:3]

betta_rot_part = simplify(alpha_T_rot.inv())
betta = diag(R_0_B, betta_rot_part)
betta_T = betta.T
alpha_T = (betta.inv())
alpha = alpha_T.T

n = len(q)
gamma1 = zeros(n)
gamma2 = zeros(n)

for i in range(n):
    gamma2[i,:] = omega.T * betta_T * (alpha.diff(q[i]))

for i in range(n):
    for j in range(n):
        gamma1[i,j] = omega.T * betta_T * (alpha[i,j].diff(q))

gamma_mat = (gamma1 - gamma2)

"""_____Jacobians_____"""
# Boat
J_b_b = pm.UnitVectors.i_jac_v.row_join(pm.UnitVectors.j_jac_v).row_join(pm.UnitVectors.k_jac_v) # Linear velocities
J_b_b = J_b_b.row_join(pm.UnitVectors.i_jac_w).row_join(pm.UnitVectors.j_jac_w).row_join(pm.UnitVectors.k_jac_w)

"""_____Inertia tensors_____"""

# Inertia tensor for rectangular prism about its own COG (standard formula)
def box_inertia_tensor(m, l, w, h):
    return m * (1/12) * Matrix([
        [w**2 + h**2, 0, 0],
        [0, l**2 + h**2, 0],
        [0, 0, l**2 + w**2]
    ])

# Boat
I_boat_local = box_inertia_tensor(
    pm.BoatParams.mass,
    pm.BoatParams.length,
    pm.BoatParams.width,
    pm.BoatParams.height
)

# Heights of tanks
h_aft_ps = m_aft_ps / (pm.BoatParams.rho * pm.TanksAftPortside.length * pm.TanksAftPortside.width)
h_aft_stb = m_aft_stb / (pm.BoatParams.rho * pm.TanksAftStarboard.length * pm.TanksAftStarboard.width)
h_fp_ps = m_fp_ps / (pm.BoatParams.rho * pm.TanksForepeakPortside.length * pm.TanksForepeakPortside.width)
h_fp_stb = m_fp_stb / (pm.BoatParams.rho * pm.TanksForepeakStarboard.length * pm.TanksForepeakStarboard.width)

# Local inertia tensors
I_aft_ps_local = box_inertia_tensor(m_aft_ps, pm.TanksAftPortside.length, pm.TanksAftPortside.width, h_aft_ps)
I_aft_stb_local = box_inertia_tensor(m_aft_stb, pm.TanksAftStarboard.length, pm.TanksAftStarboard.width, h_aft_stb)
I_fp_ps_local = box_inertia_tensor(m_fp_ps, pm.TanksForepeakPortside.length, pm.TanksForepeakPortside.width, h_fp_ps)
I_fp_stb_local = box_inertia_tensor(m_fp_stb, pm.TanksForepeakStarboard.length, pm.TanksForepeakStarboard.width, h_fp_stb)

# CG vectors of tanks (from origo of body)
r_tank_aft_ps = pm.TanksAftPortside.r + Matrix([0, 0, 2 - h_aft_ps/2])
r_tank_aft_stb = pm.TanksAftStarboard.r + Matrix([0, 0, 2 - h_aft_stb/2])
r_tank_fp_ps = pm.TanksForepeakPortside.r + Matrix([0, 0, 2 - h_fp_ps/2])
r_tank_fp_stb = pm.TanksForepeakStarboard.r + Matrix([0, 0, 2 - h_fp_stb/2])

# Total CG of boat
mass_boat = pm.BoatParams.mass + m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb
r_boat_cog = (
    pm.BoatParams.mass * pm.BoatParams.r
    + m_aft_ps * r_tank_aft_ps
    + m_aft_stb * r_tank_aft_stb
    + m_fp_ps * r_tank_fp_ps
    + m_fp_stb * r_tank_fp_stb
) / mass_boat


# Vectors from tank-CG to total CG (p.a.t.)
def parallel_axis(I_local, m, r):
    r_outer = r * r.T
    r_squared = (r.T * r)[0]
    return I_local + m * (r_squared * eye(3) - r_outer)

dr_boat = lambda r: r_boat_cog - r # r is the vector from CO to CG

I_boat = parallel_axis(I_boat_local, pm.BoatParams.mass, dr_boat(pm.BoatParams.r))
I_aft_ps = parallel_axis(I_aft_ps_local, m_aft_ps, dr_boat(r_tank_aft_ps))
I_aft_stb = parallel_axis(I_aft_stb_local, m_aft_stb, dr_boat(r_tank_aft_stb))
I_fp_ps = parallel_axis(I_fp_ps_local, m_fp_ps, dr_boat(r_tank_fp_ps))
I_fp_stb = parallel_axis(I_fp_stb_local, m_fp_stb, dr_boat(r_tank_fp_stb))

# Total inertia tensor about CG of boat
I_total_boat = I_boat + I_aft_ps + I_aft_stb + I_fp_ps + I_fp_stb

"""Mass matrices"""
# Boat
# skew-symmetric matrix
S = lambda r: Matrix([[   0, -r[2],  r[1]],
                      [ r[2],    0, -r[0]],
                      [-r[1], r[0],    0]])

I_spat = Matrix.vstack(
            Matrix.hstack(mass_boat*eye(3), -mass_boat*S(r_boat_cog)),
            Matrix.hstack( mass_boat*S(r_boat_cog), I_total_boat - mass_boat*S(r_boat_cog)*S(r_boat_cog) )
        )
B_boat = J_b_b.T * I_spat * J_b_b
B_boat = pad_matrix(B_boat, len(q), len(q))

B_local = B_boat
B = betta.T * B_local * betta

"""Kinetic energy and partial derivatives of this"""
T = (0.5 * omega.T * B * omega)[0,0]
T_diff_q = T.diff(q)
T_diff_omega = T.diff(omega)

"""Added mass"""
# Calculated from table A-2 in DNV-RP-H103
"""A_ij = rho * C_A * V_R      V_R: volume reference (3.2.5.1)
A11 = rho V Ca,1
A22 = rho V Ca,2
A33 = rho V Ca,3
A44 = rho V Ca,44 b²
A55 = rho V Ca,55 l²
A66 = rho V Ca,66 (l² + b²)
"""
A11 = 1.4e4
A22 = 2.57e4
A33 = 6.34e5
A44 = 1.15e6
A55 = 3.37e6
A66 = 3.53e6
# 6x6 added mass
B_A_6 = diag(A11, A22, A33, A44, A55, A66)

B_A = B_A_6
B_A_11 = diag(A11, A22, A33)
B_A_22 = diag(A44, A55, A66)
B_A_12 = B_A_21 = 0*eye(3)

v_body = Matrix([uq, vq, wq])
omega_body = Matrix([pq, qq, rq])

C_A_6 = Matrix([[0*eye(3) , -S(B_A_11*v_body)],
              [-S(B_A_11*v_body), -S(B_A_22*omega_body)]])

C_A = C_A_6

"""_____Potential energy_____"""

# Hydrostatics 
rho = pm.BoatParams.rho
g   = pm.Gravity.g
L_l   = pm.BoatParams.length
B_w   = pm.BoatParams.width

# total mass
m_tot = pm.BoatParams.mass + m_fp_ps + m_fp_stb + m_aft_ps + m_aft_stb

# Free surface effects (for GM_T, that is width is cubed)
moment_tanks = (1/12) * pm.TanksAftPortside.length * pm.TanksAftPortside.width**3
FSC = 0
for i in range(len(ballast_array)):
    FSC += (rho/m_tot) * moment_tanks

Disp  = m_tot / rho

# waterplane area and draft
A_wp = L_l*B_w
T_draft = Disp / A_wp # draft

# Moments about x and y
I_wp_x = B_w**3 * L_l / 12
I_wp_y = L_l**3 * B_w / 12
BM_T   = I_wp_x / Disp
BM_L   = I_wp_y / Disp

# z coordinates in body frame (down is positive)
z_G_deck = r_boat_cog[2]
z_B_deck = -T_draft/2
BG = z_G_deck - z_B_deck
GM_T = BM_T - BG - FSC
GM_L = BM_L - BG

C_phi   = rho * g * Disp * GM_T
C_theta = rho * g * Disp * GM_L
C_z     = rho * g * A_wp

# Restoring force matrix K
K6 = zeros(6)
K6[2,2] =  C_z         # heave
K6[3,3] =  C_phi       # roll
K6[4,4] =  C_theta     # pitch

restoring_forces = K6 * q

# Gravitational
z_G_ned = (T_n_b * r_boat_cog.col_join(Matrix([1])))[2, 0]   
P_g = -m_tot * g * z_G_ned   

# Potensional energy
P = P_g 
P_diff_q = P.diff(q)

"""_____D(q)_____"""
Dv = diag(pm.BoatParams.d_x,
          pm.BoatParams.d_y,
          pm.BoatParams.d_z)
Dw = diag(pm.BoatParams.d_roll,
          pm.BoatParams.d_pitch,
          pm.BoatParams.d_yaw)

S = lambda v: Matrix([[    0, -v[2],  v[1]],
                      [ v[2],     0, -v[0]],
                      [-v[1],  v[0],     0]])

D_boat = diag(Dv, Dw)

H = Matrix([[eye(3), (S(r_boat_cog).T)],
            [0*eye(3), eye(3)]])

D = H.T * D_boat * H

"""_____External forces_____"""
tau = Matrix([
    tau_xn,
    tau_yn,
    tau_zn,
    tau_phi,
    tau_theta,
    tau_psi,
])

"""_____Final equations_____"""
gamma_T_diff_omega = gamma_mat * T_diff_omega
D_omega = D * omega

# Filepaths
filepath_cpp_wave = "../code/cpp_sim_testing/M1_wave/src"
filepath_h_wave   = "../code/cpp_sim_testing/M1_wave/include"
filepath_cpp = "../code/cpp_sim_testing/M1/src"
filepath_h   = "../code/cpp_sim_testing/M1/include"

# Functions and names
functions_and_names = [
    (B, 'mass_inertia'),
    (betta, 'beta'),
    (gamma_T_diff_omega, 'gamma_T_diff_omega'),
    (T_diff_q, 'T_diff_q'),
    (P_diff_q, 'P_diff_q'),
    (D_omega, 'D_q_dot'),
    (restoring_forces, 'restoring'),
    (B_A, 'B_added_mass'),
    (C_A, 'C_added_mass')
]

# Wave-dir
for func, name in functions_and_names:
    cppw.generate_cpp_files(func, name, all_vars, filepath_cpp_wave, filepath_h_wave)
# No-wave-dir
for func, name in functions_and_names:
    cppw.generate_cpp_files(func, name, all_vars, filepath_cpp, filepath_h)

print("Accumulated total time: ", datetime.now()-startTimeTotal)