import numpy as np
from sympy import*

def jonswap_spectrum(Hs, Tp, gamma=3.3, N=100, f_min=0.05, f_max=0.2):
    """
    - Hs: significant wave period (H_1/3) (m)
    - Tp: peak period (s)
    - gamma: peak shape parameter (default 3.3)
    - N: number of components (frequencies)
    - f_min: lowest frequency (Hz)
    - f_max: highest frequency (Hz). Default: 2.5 / Tp <- cutoff
    
    Returns:
    - omega: frequency array (rad/s)
    - S_omega: spectra values (m² s/rad)
    - a: amplitudes (m)

    Expressions according to master thesis (Chapter ''JONSWAP Spectrum'')
    """
    T1 = 0.834 * Tp
    fp = 1 / Tp
    if f_max is None:
        f_max = 2.5 * fp

    omega_min = f_min*2*np.pi
    omega_max = f_max*2*np.pi

    omega  = np.linspace(omega_min, omega_max, N)
    domega = omega[1] - omega[0]

    alpha = 155.0 * Hs**2 / T1**4
    sigma = np.where(omega <= 2*np.pi*fp, 0.07, 0.09)
    Y     = np.exp(-((0.191 * omega * T1 - 1)**2) / (2 * sigma**2))
    S_omega   = alpha * omega**(-5) * np.exp(-944 / (T1**4 * omega**4)) * gamma**Y
    a = np.sqrt(2 * S_omega * domega)       

    return omega, S_omega, a

def dynamical_pressure_field(Hs, Tp, gamma=3.3, N=100, f_min=0.05, f_max=0.3125):
    omega, S_omega, a = jonswap_spectrum(Hs, Tp, gamma, N, f_min, f_max)

    x, y, z, t, wave_angle = symbols('x y z t wave_angle')

    p_D = 0
    g = 9.81
    rho = 1000.0

    epsilons = np.random.uniform(0, 2 * np.pi, N)

    for i in range(N):
        omega_i = omega[i]
        k_i = (omega_i**2)/g
        zeta_i = a[i]
        epsilon_i = epsilons[i]
        arg = -k_i * (x * cos(wave_angle) + y * sin(wave_angle)) + omega_i * t + epsilon_i
        p_D += (rho * g * zeta_i * exp(-k_i * z) * sin(arg))
    
    return Matrix([p_D]), S_omega, omega, a, epsilons

def wave_accelerations(omega, a, epsilons):
    """
    
    """
    g = 9.81
    a_x = 0
    a_y = 0
    a_z = 0

    x, y, z, t, wave_angle = symbols('x y z t wave_angle')

    for i in range(len(omega)):
        omega_i = omega[i]
        k_i     = (omega_i**2)/g
        zeta_i  = a[i]
        eps_i = epsilons[i]

        cosine_arg_i = omega_i * t - k_i * (x*cos(wave_angle) + y*sin(wave_angle)) + eps_i
        a_x += omega_i**2 * zeta_i * exp(-k_i * z) * cos(cosine_arg_i) * cos(wave_angle)
        a_y += omega_i**2 * zeta_i * exp(-k_i * z) * cos(cosine_arg_i) * sin(wave_angle)
        a_z += -omega_i**2 * zeta_i * exp(-k_i * z) * sin(cosine_arg_i)

    a_vec = Matrix([a_x, a_y, a_z])
    return a_vec
