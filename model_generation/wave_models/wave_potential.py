from datetime import datetime
from sympy import *
from sympy.physics.mechanics import*
from model_generation.kinematics.transformations import*
from model_generation.kinematics.joint_type import JointType
from model_generation.kinematics.jacobian import jacobian
import model_generation.cpp_write.cpp_write as cppw
from model_generation.utils.utils import pad_matrix, coriolis_matrix_christoffel, inverse_se3
import model_generation.models.model_1.params as pm
import numpy as np

startTimeTotal = datetime.now()



# Euler angles of boat
phi, theta, psi = symbols('phi theta psi')
# Positions of boat
x_n, y_n, z_n = symbols('x y z')
# Time
t = symbols('t')

q = Matrix([x_n, y_n, z_n, phi, theta, psi])
q_vals = [5, 5, 0, 0.1, 0.1, 0.1, 0]

T_n_xn = trans_x(x_n)
T_n_yn = simplify(T_n_xn * trans_y(y_n))
T_n_zn = simplify(T_n_yn * trans_z(z_n))
T_n_psi = simplify(T_n_zn * rot_z(psi))
T_n_theta = simplify(T_n_psi * rot_y(theta))
T_n_b = simplify(trans_x(x_n) * trans_y(y_n) * trans_z(z_n) * rot_z(psi) * rot_y(theta) * rot_x(phi))

R_n_b = T_n_b[:3,:3]

all_vars = Matrix([x_n, y_n, z_n, phi, theta, psi, t])

sections_width = 20
sections_length =40
total_sections = sections_width * sections_length
section_length = pm.BoatParams.length/sections_length
section_width = pm.BoatParams.width/sections_width
area_section = section_length*section_width

body_frame_points = []
r_k_vectors       = []

point_cog_b       = pm.BoatParams.r

for i in range(sections_length):
    for j in range(sections_width):
        offset = Matrix([-pm.BoatParams.length/2 + section_length*(i) + section_length/2,
                         -pm.BoatParams.width/2 + section_width*(j) + section_width/2,
                         pm.BoatParams.height])
        body_frame_points.append(offset)
        r_k_vectors.append(offset-point_cog_b)

body_frame_points = Matrix.hstack(*body_frame_points)
body_frame_points = body_frame_points.col_join(ones(1,(body_frame_points.cols)))
r_k_vectors = Matrix.hstack(*r_k_vectors)

world_frame_points = T_n_b * body_frame_points
world_frame_points = (world_frame_points[:3,:])

unit_vectors = zeros(3,total_sections)
unit_vectors[2,:] = ones(1, total_sections)
unit_vectors = unit_vectors * area_section




filepath = "model_generation/wave_models/output"
cppw.generate_cpp_files(world_frame_points, 'worldframepoints', all_vars, filepath)
cppw.generate_cpp_files(r_k_vectors, "vectors_cog",Matrix([]), filepath)
cppw.generate_cpp_files(R_n_b, "R_n_b", all_vars, filepath)


# pressure-field with JONSWAP

def jonswap_spectrum(Hs, Tp, gamma=3.3, N=100, f_min=0.05, f_max=0.2):
    """
    Lager JONSWAP-spekter (amplituder og frekvenser).
    
    Parametere:
    - Hs: signifikant bølgehøyde (m)
    - Tp: peak periode (s)
    - gamma: toppskarpethetsfaktor (default 3.3)
    - N: antall frekvenser (komponentbølger)
    - f_min: laveste frekvens (Hz)
    - f_max: høyeste frekvens (Hz). Default: 2.5 / Tp
    
    Returnerer:
    - f: frekvensarray (Hz)
    - S: spekterverdier (m²/Hz)
    - a: amplituder (m)
    """
    g = 9.81
    fp = 1 / Tp
    if f_max is None:
        f_max = 2.5 * fp  # typisk cutoff
    f = np.linspace(f_min, f_max, N)
    df = f[1] - f[0]

    alpha = 0.076 * (Hs ** 2) / (Tp ** 4)
    sigma = np.where(f <= fp, 0.07, 0.09)

    r = np.exp(- ((f - fp) ** 2) / (2 * sigma ** 2 * fp ** 2))
    S = alpha * g ** 2 * f ** (-5) * np.exp(-1.25 * (fp / f) ** 4) * gamma ** r

    a = np.sqrt(2 * S * df)  # amplituder per komponent

    return f, S, a

def dynamical_pressure_field(Hs, Tp, gamma=3.3, N=100, f_min=0.05, f_max=0.3125, theta_deg = 45):
    f, S, a = jonswap_spectrum(Hs, Tp, gamma, N, f_min, f_max)

    x, y, z, t, wave_angle = symbols('x y z t wave_angle')

    p_D = 0
    g = 9.81
    rho = 1000.0
    delta_f = f[1]-f[0]
    theta_rad = np.deg2rad(theta_deg)

    epsilons = np.random.uniform(0, 2 * np.pi, N)

    for i in range(N):
        omega_i = 2*np.pi*f[i]
        k_i = (omega_i**2)/g
        zeta_i = sqrt(2*S[i]*delta_f)
        epsilon_i = epsilons[i]
        arg = -k_i * (x * cos(wave_angle) + y * sin(wave_angle)) + omega_i * t + epsilon_i
        p_D += (rho * g * zeta_i * exp(-k_i * z) * sin(arg))
    
    return Matrix([p_D])

x, y, z, t, wave_angle = symbols('x y z t, wave_angle')
pd_vars = Matrix([x, y,  z, t, wave_angle])
p_D = (dynamical_pressure_field(0.3, 8.5, N=100, f_min=0.04, f_max=0.2, theta_deg=180))
print(area_section)

# def dynamic_pressure_field (rho: float, g: float, zeta: float, k: float, epsilon: float, omega: float):
#     pressure = rho*g*zeta*E**(-k * z) * sin(omega*t - k*x + epsilon)
#     return pressure
cppw.generate_cpp_files(p_D, 'dynamic_pressure', pd_vars, filepath)

print("Accumulated total time: ", datetime.now()-startTimeTotal)


import matplotlib.pyplot as plt

# Parametre
Hs = 0.3       # signifikant bølgehøyde (m)
Tp = 8.5       # peak periode (s)
gamma = 3.3    # toppskarpethetsfaktor
N = 100        # antall frekvenser
f_min = 0.04   # laveste frekvens
f_max = 0.2    # høyeste frekvens

# Beregn spekter
f, S, a = jonswap_spectrum(Hs, Tp, gamma=gamma, N=N, f_min=f_min, f_max=f_max)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(f, S, label='JONSWAP spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Spectral density $S(f)$ (m²/Hz)')
plt.title('JONSWAP wave spectrum')
plt.grid(True)
plt.legend()
plt.show()

