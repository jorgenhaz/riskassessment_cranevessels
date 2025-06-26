#include "P_diff_q.h"

Eigen::VectorXd P_diff_q(Eigen::VectorXd kwargs) {
	double x = kwargs(0);
	double y = kwargs(1);
	double z = kwargs(2);
	double phi = kwargs(3);
	double theta = kwargs(4);
	double psi = kwargs(5);
	double u = kwargs(6);
	double v = kwargs(7);
	double w = kwargs(8);
	double p = kwargs(9);
	double q = kwargs(10);
	double r = kwargs(11);
	double tau_xn = kwargs(12);
	double tau_yn = kwargs(13);
	double tau_zn = kwargs(14);
	double tau_phi = kwargs(15);
	double tau_theta = kwargs(16);
	double tau_psi = kwargs(17);
	double m_fp_stb = kwargs(18);
	double m_fp_ps = kwargs(19);
	double m_aft_stb = kwargs(20);
	double m_aft_ps = kwargs(21);
	Eigen::VectorXd m4(6, 1);
	m4(0) = 0;
	m4(1) = 0;
	m4(2) = -9.8100000000000005*m_aft_ps - 9.8100000000000005*m_aft_stb - 9.8100000000000005*m_fp_ps - 9.8100000000000005*m_fp_stb - 588600.0;
	m4(3) = -2.1607538802660753*(-9.8100000000000005*m_aft_ps - 9.8100000000000005*m_aft_stb - 9.8100000000000005*m_fp_ps - 9.8100000000000005*m_fp_stb - 588600.0)*sin(phi)*cos(theta);
	m4(4) = -2.1607538802660753*(-9.8100000000000005*m_aft_ps - 9.8100000000000005*m_aft_stb - 9.8100000000000005*m_fp_ps - 9.8100000000000005*m_fp_stb - 588600.0)*sin(theta)*cos(phi);
	m4(5) = 0;
	return m4;
}