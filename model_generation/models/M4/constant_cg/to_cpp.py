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
import model_generation.models.M4.constant_cg.params as pm

startTimeTotal = datetime.now()

g_vec = Matrix([0, 0, pm.Gravity.g])

# Euler angles
phi, theta, psi = symbols('phi theta psi')
# Position variables
x_n, y_n, z_n = symbols('x y z')
# Crane joints
q1, q2, q3, q4 = symbols('q1 q2 q3 q4')
# Pendulum angles
q1_p, q2_p = symbols('q1_p q2_p')
q1_0, q2_0, q3_0, q4_0 = symbols('q1_0 q2_0 q3_0 q4_0')
q1_dot, q2_dot, q3_dot, q4_dot = symbols('q1_dot q2_dot q3_dot q4_dot')
q1_pdot, q2_pdot = symbols('q1_pdot q2_pdot')

# Body-fixed velocities
uq, vq, wq, pq, qq, rq = symbols('u v w p q r')

# State-vectors
q = Matrix([x_n, y_n, z_n, phi, theta, psi, q1, q2, q3, q4, q1_p, q2_p])
omega = Matrix([uq, vq, wq, pq, qq, rq, q1_dot, q2_dot, q3_dot, q4_dot, q1_pdot, q2_pdot])

# External forces
tau_xn, tau_yn, tau_zn, tau_phi, tau_theta, tau_psi, tau_q1, tau_q2, tau_q3, tau_q4, tau_q1p, tau_q2p = symbols('tau_xn tau_yn tau_zn tau_phi tau_theta tau_psi tau_q1 tau_q2 tau_q3 tau_q4 tau_q1p tau_q2p')

# Mass in ballast tanks - variables
m_fp_stb, m_fp_ps, m_aft_stb, m_aft_ps = symbols('m_fp_stb m_fp_ps m_aft_stb m_aft_ps')

# Payload
m_payload, wire_length = symbols('m_payload wire_length')

# All variables for cpp-code
all_vars = Matrix([x_n, y_n, z_n, phi, theta, psi, q1, q2, q3, q4, q1_p, q2_p,
                   uq, vq, wq, pq, qq, rq, q1_dot, q2_dot, q3_dot, q4_dot, q1_pdot, q2_pdot,
                   tau_xn, tau_yn, tau_zn, tau_phi, tau_theta, tau_psi, tau_q1, tau_q2, tau_q3, tau_q4, tau_q1p, tau_q2p,
                   m_fp_stb, m_fp_ps, m_aft_stb, m_aft_ps,
                   q1_0, q2_0, q3_0, q4_0,
                   m_payload, wire_length])

"""_____Kinematics_____"""
# From NED to body-fixed frame
T_n_xn = trans_x(x_n)
T_n_yn = simplify(T_n_xn * trans_y(y_n))
T_n_zn = simplify(T_n_yn * trans_z(z_n))
T_n_psi = simplify(T_n_zn * rot_z(psi))
T_n_theta = simplify(T_n_psi * rot_y(theta))
T_n_b = simplify(trans_x(x_n) * trans_y(y_n) * trans_z(z_n) * rot_z(psi) * rot_y(theta) * rot_x(phi))
R_n_b = T_n_b[:3,:3]
# From NED to crane-base
T_b_cb = simplify(trans_x(pm.CraneBase.x) * trans_y(pm.CraneBase.y) * trans_z(-pm.CraneBase.height))
T_b_q1 = simplify(T_b_cb * rot_z(q1) * trans_z(-pm.Joint1Params.length))
R_b_q1 = T_b_q1[:3,:3]
T_b_q1_cog = simplify(T_b_q1 * trans_z(pm.Joint1Params.length/2))
T_n_cb = simplify(T_n_b * T_b_cb)
T_b_q2 = T_b_q1 * rot_y(q2) * trans_x(pm.Joint2Params.length)
R_b_q2 = T_b_q2[:3,:3]
T_b_q2_cog = T_b_q2 * trans_x(-pm.Joint2Params.length/2)
T_b_q3 = T_b_q2 * rot_y(q3) * trans_x(pm.Joint3Params.length)
R_b_q3 = T_b_q3[:3,:3]
T_b_q3_cog = T_b_q3 * trans_x(-pm.Joint3Params.length/2)
T_b_q4 = simplify(T_b_q3 * trans_x(q4 + pm.Joint4Params.length))
R_b_q4 = simplify(T_b_q4[:3,:3])
T_b_q4_cog = simplify(T_b_q4 * trans_x(-(q4 + pm.Joint4Params.length)/2))
T_b_payload = simplify(T_b_q4 * rot_x(q1_p) * rot_y(q2_p) * trans_z(wire_length))
R_b_payload = T_b_payload[:3,:3]

# From NED to q1
T_n_q1 = simplify(T_n_cb * rot_x(q1) * trans_z(-pm.Joint1Params.length))
T_n_q2_cog = T_n_b * T_b_q2_cog
T_n_q3_cog = T_n_b * T_b_q3_cog
T_n_q4_cog = simplify(T_n_b * T_b_q4_cog)
R_n_q1 = T_n_q1[:3,:3]
# From NED to CoG of q1
T_n_q1_cog = simplify(T_n_q1 * trans_z(pm.Joint1Params.length/2))

"""_____betta, alpha_T, betta_T and gamma_____"""
# Transform om linear velocities in body-frame
R_0_B = simplify(T_n_b[:3,:3])
# Kinematics from body-frame to NED-frame
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
betta = pad_matrix(betta, 12, 12)
betta[6,6] = 1
betta[7,7] = 1
betta[8,8] = 1
betta[9,9] = 1
betta[10,10] = 1
betta[11, 11] = 1
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

# q1 in reference to body-fixed frame
transformList = [T_b_q1_cog]
rotAxList = [pm.UnitVectors.i]
jointTypeList = [JointType.REVOLUTE]
jointVec = Matrix([q1])

J_b_q1 = jacobian(transformList, rotAxList, jointTypeList, jointVec)
J_b_q1 = J_b_b.row_join(J_b_q1)

# q2 in reference to body-fixed frame
transformList = [T_b_q1, T_b_q2_cog]
rotAxList = [
    pm.UnitVectors.k,
    pm.UnitVectors.j
    ]
jointTypeList = [JointType.REVOLUTE,
                 JointType.REVOLUTE]
jointVec = Matrix([q1, q2])
J_b_q2 = jacobian(transformList, rotAxList, jointTypeList, jointVec)
J_b_q2 = J_b_b.row_join(J_b_q2)

# q3 in reference to body-fixed frame
transformList = [T_b_q1, T_b_q2, T_b_q3_cog]
rotAxList = [
    pm.UnitVectors.k,
    pm.UnitVectors.j,
    pm.UnitVectors.j
]
jointTypeList = [JointType.REVOLUTE,
                 JointType.REVOLUTE,
                 JointType.REVOLUTE]
jointVec = Matrix([q1, q2, q3])
J_b_q3 = jacobian(transformList, rotAxList, jointTypeList, jointVec)
J_b_q3 = J_b_b.row_join(J_b_q3)

# q4 in reference to body-fixed frame
transformList = [T_b_q1, T_b_q2, T_b_q3, T_b_q4_cog]
rotAxList = [
    pm.UnitVectors.k,
    pm.UnitVectors.j,
    pm.UnitVectors.j,
    pm.UnitVectors.i
]
jointTypeList = [JointType.REVOLUTE,
                 JointType.REVOLUTE,
                 JointType.REVOLUTE,
                 JointType.PRISMATIC]
jointVec = Matrix([q1, q2, q3, q4])
J_b_q4 = jacobian(transformList, rotAxList, jointTypeList, jointVec)
J_b_q4 = J_b_b.row_join(J_b_q4)

# payload in reference to body-frame
transformList = [T_b_q1, T_b_q2, T_b_q3, T_b_q4, T_b_q4*rot_x(q1_p), T_b_payload]
rotAxList = [
    pm.UnitVectors.k,
    pm.UnitVectors.j,
    pm.UnitVectors.j,
    pm.UnitVectors.i,
    pm.UnitVectors.i,
    pm.UnitVectors.j
]
jointTypeList = [JointType.REVOLUTE,
                 JointType.REVOLUTE,
                 JointType.REVOLUTE,
                 JointType.PRISMATIC,
                 JointType.REVOLUTE,
                 JointType.REVOLUTE]
jointVec = Matrix([q1, q2, q3, q4, q1_p, q2_p])
J_b_payload = jacobian(transformList, rotAxList, jointTypeList, jointVec)
J_b_payload = J_b_b.row_join(J_b_payload)

print("JACOBIANS DONE")

"""_____Inertia tensors_____"""
# ______boat and ballast tanks_____

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
r_tank_aft_ps = (pm.TanksAftPortside.r + Matrix([0, 0, 2 - h_aft_ps/2])).subs(m_aft_ps, 1500)
r_tank_aft_stb = (pm.TanksAftStarboard.r + Matrix([0, 0, 2 - h_aft_stb/2])).subs(m_aft_stb, 1500)
r_tank_fp_ps = (pm.TanksForepeakPortside.r + Matrix([0, 0, 2 - h_fp_ps/2])).subs(m_fp_ps, 1500)
r_tank_fp_stb = (pm.TanksForepeakStarboard.r + Matrix([0, 0, 2 - h_fp_stb/2])).subs(m_fp_stb, 1500)

# Total CG of boat
mass_boat = pm.BoatParams.mass + 1500 + 1500 + 1500 + 1500
r_boat_cog = (
    pm.BoatParams.mass * pm.BoatParams.r
    + 1500 * r_tank_aft_ps
    + 1500 * r_tank_aft_stb
    + 1500 * r_tank_fp_ps
    + 1500 * r_tank_fp_stb
) / mass_boat
mass_boat = pm.BoatParams.mass + m_aft_stb + m_aft_ps + m_fp_ps + m_fp_stb

# Vektorer fra tank-CG til total COG (for parallellakseteoremet)
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

# q1
I_q1_local = pm.Joint1Params.mass * Matrix([
    [(1/12)*(pm.Joint1Params.length**2 + 3*pm.Joint1Params.radius**2), 0, 0],
    [0, (1/12)*(pm.Joint1Params.length**2 + 3*pm.Joint1Params.radius**2), 0],
    [0, 0, (1/2)*pm.Joint1Params.radius**2]
    ])
I_q1_ref = R_b_q1 * I_q1_local * R_b_q1.T

# q2
I_q2_local = pm.Joint2Params.mass * Matrix([
    [(1/2)*pm.Joint2Params.radius**2, 0, 0],
    [0, (1/12)*(pm.Joint2Params.length**2 + 3*pm.Joint2Params.radius**2), 0],
    [0, 0, (1/12)*(pm.Joint2Params.length**2 + 3*pm.Joint2Params.radius**2)]
    ])
I_q2_ref = R_b_q2 * I_q2_local * R_b_q2.T

# q3
I_q3_local = pm.Joint3Params.mass * Matrix([
    [(1/2)*pm.Joint3Params.radius**2, 0, 0],
    [0, (1/12)*(pm.Joint3Params.length**2 + 3*pm.Joint3Params.radius**2), 0],
    [0, 0, (1/12)*(pm.Joint3Params.length**2 + 3*pm.Joint3Params.radius**2)]
    ])
I_q3_ref = R_b_q3 * I_q3_local * R_b_q3.T

# q4
I_q4_local = pm.Joint4Params.mass * Matrix([
    [(1/2)*pm.Joint4Params.radius**2, 0, 0],
    [0, (1/12)*(pm.Joint4Params.length**2 + 3*pm.Joint4Params.radius**2), 0],
    [0, 0, (1/12)*(pm.Joint4Params.length**2 + 3*pm.Joint4Params.radius**2)]
    ])
I_q4_ref = R_b_q4 * I_q4_local * R_b_q4.T

# payload
I_payload_local = (m_payload/6)*(1**2) * eye(3)
I_payload_ref = R_b_payload * I_payload_local * R_b_payload.T

print("INERTIA TENSORS DONE")

"""Mass matrices"""
# Boat
S = lambda r: Matrix([[   0, -r[2],  r[1]],
                      [ r[2],    0, -r[0]],
                      [-r[1], r[0],    0]])

I_spat = Matrix.vstack(
            Matrix.hstack(mass_boat*eye(3), -mass_boat*S(r_boat_cog)),
            Matrix.hstack( mass_boat*S(r_boat_cog), I_total_boat - mass_boat*S(r_boat_cog)*S(r_boat_cog) )
        )
B_boat = J_b_b.T * I_spat * J_b_b
B_boat = pad_matrix(B_boat, len(q), len(q))

# q1
B_q1 = J_b_q1.T * Matrix([
    [pm.Joint1Params.mass * eye(3), 0*eye(3)],
    [0*eye(3), I_q1_ref]
]) * J_b_q1
B_q1 = pad_matrix(B_q1, len(q), len(q))

# q2 
B_q2 = J_b_q2.T * Matrix([
    [pm.Joint2Params.mass * eye(3), 0*eye(3)],
    [0*eye(3), I_q2_ref]
]) * J_b_q2

B_q2 = pad_matrix(B_q2, len(q), len(q))

# q3
B_q3 = J_b_q3.T * Matrix([
    [pm.Joint3Params.mass * eye(3), 0*eye(3)],
    [0*eye(3), I_q3_ref]
]) * J_b_q3
B_q3 = pad_matrix(B_q3, len(q), len(q))

# q4
B_q4 = J_b_q4.T * Matrix([
    [pm.Joint4Params.mass * eye(3), 0*eye(3)],
    [0*eye(3), I_q4_ref]
]) * J_b_q4
B_q4 = pad_matrix(B_q4, len(q), len(q))

# payload
B_payload = J_b_payload.T * Matrix([
    [m_payload*eye(3), 0*eye(3)],
    [0*eye(3), I_payload_ref]
]) * J_b_payload
B_payload = pad_matrix(B_payload, len(q), len(q))

B_local = B_boat + B_q1 + B_q2 + B_q3 + B_q4 + B_payload
B = betta.T * B_local * betta

print("MASS MATRICE DONE")

"""Kinetic energy and partial derivatives of this"""
T = (0.5 * omega.T * B * omega)[0,0]
T_diff_q = T.diff(q)
T_diff_omega = T.diff(omega)

print("Kinetic energy differentiated")

"""Added mass"""
# Calculated from table A-2 in DNV-RP-H103
A11 = 1.4e4
A22 = 2.57e4
A33 = 6.34e5
A44 = 1.15e6
A55 = 3.37e6
A66 = 3.53e6
# 6x6 added mass
B_A_6 = diag(A11, A22, A33, A44, A55, A66)

B_A = zeros(12,12)
B_A[:6,:6] = B_A_6
B_A_11 = diag(A11, A22, A33)
B_A_22 = diag(A44, A55, A66)
B_A_12 = B_A_21 = 0*eye(3)

v_body = Matrix([uq, vq, wq])
omega_body = Matrix([pq, qq, rq])

C_A_6 = Matrix([[0*eye(3) , -S(B_A_11*v_body)],
              [-S(B_A_11*v_body), -S(B_A_22*omega_body)]])

C_A = zeros(12,12)
C_A[:6, :6] = C_A_6

"""_____Potential energy_____"""
# Hydrostatics 
rho = pm.BoatParams.rho
g   = pm.Gravity.g
L_l   = pm.BoatParams.length
B_w   = pm.BoatParams.width

# total mass and deplacement
m_tot = (pm.BoatParams.mass + m_fp_ps + m_fp_stb + m_aft_ps + m_aft_stb +
         pm.Joint1Params.mass + pm.Joint2Params.mass + pm.Joint3Params.mass + pm.Joint4Params.mass
         + m_payload)

# Free surface effects (for GM_T, that is width is cubed)
ballast_array = Matrix([m_fp_stb, m_fp_ps, m_aft_stb, m_aft_ps])
moment_tanks = (1/12) * pm.TanksAftPortside.length * pm.TanksAftPortside.width**3
FSC = 0
for i in range(len(ballast_array)):
    FSC += (rho/m_tot) * moment_tanks

FSC_Payload = -wire_length * (m_payload/m_tot)

Disp  = m_tot / rho

A_wp = L_l*B_w
T_draft = Disp / A_wp 

I_wp_x = B_w**3 * L_l / 12
I_wp_y = L_l**3 * B_w / 12
BM_T   = I_wp_x / Disp
BM_L   = I_wp_y / Disp

# Restoring CG
r_cog_system = r_boat_cog

z_G_deck = r_cog_system[2]
z_B_deck = -T_draft/2
BG = z_G_deck - z_B_deck

GM_T = BM_T - BG - FSC - FSC_Payload
GM_L = BM_L - BG

C_phi   = rho * g * Disp * GM_T
C_theta = rho * g * (Disp * GM_L)
C_z     = rho * g * A_wp

K6 = zeros(12)
K6[2,2] =  C_z        
K6[3,3] =  C_phi      
K6[4,4] =  C_theta    

restoring_forces = K6 * q

z_G_ned = (T_n_b * r_boat_cog.col_join(Matrix([1])))[2, 0]  

P_g = -mass_boat * g * z_G_ned  

P_q1 = -pm.Joint1Params.mass * g_vec.T * T_n_q1_cog[0:3,3]
P_q2 = -pm.Joint2Params.mass * g_vec.T * T_n_q2_cog[0:3,3]
P_q3 = -pm.Joint3Params.mass * g_vec.T * T_n_q3_cog[0:3,3]
P_q4 = -pm.Joint4Params.mass * g_vec.T * T_n_q4_cog[0:3,3]
P_payload = -m_payload * g_vec.T * (T_n_b*T_b_payload)[0:3,3]

P = P_g + P_q1[0] + P_q2[0] + P_q3[0] + P_q4[0] + P_payload[0]
P_diff_q = P.diff(q)

print("POTENTIAL ENERGY DONE")

"""_____D(q)_____  (spatial) """
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

H = Matrix([[eye(3), (S(r_cog_system).T)],
            [0*eye(3), eye(3)]])

D_boat = H.T * D_boat * H

zeta_d = 0.5 # relative damping
D = pad_matrix(D_boat, len(q), len(q))
D[6,6] = pm.Joint1Params.d
D[7,7] = pm.Joint2Params.d
D[8,8] = pm.Joint3Params.d
D[9,9] = pm.Joint4Params.d
D[10,10] = 2*zeta_d*sqrt(m_payload * ((m_payload*g)/wire_length))
D[11,11] = 2*zeta_d*sqrt(m_payload * ((m_payload*g)/wire_length))

print("DAMPING DONE")

"""_____External forces_____"""
tau = Matrix([
    tau_xn,
    tau_yn,
    tau_zn,
    tau_phi,
    tau_theta,
    tau_psi,
    tau_q1,
    tau_q2,
    tau_q3,
    tau_q4,
    tau_q1p,
    tau_q2p
])

"""_____Final equation_____"""
gamma_T_diff_omega = gamma_mat * T_diff_omega
D_omega = D * omega

print("FINAL EQUATION DONE")

# We also need B and beta

"""Generating C++-code"""
# Filepaths
filepath_cpp_wave = "../code/cpp_sim_testing/M4_wave/src"
filepath_h_wave   = "../code/cpp_sim_testing/M4_wave/include"
filepath_cpp = "../code/cpp_sim_testing/M4/src"
filepath_h   = "../code/cpp_sim_testing/M4/include"

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

# with open ("../code/cpp_sim_testing/M4_wave/files/init.yaml", "w") as f:
#     for var in all_vars:
#         f.write(f"{var}: 0.0 \n")