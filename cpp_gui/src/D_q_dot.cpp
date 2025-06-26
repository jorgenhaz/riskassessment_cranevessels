#include "D_q_dot.h"

Eigen::VectorXd D_q_dot(Eigen::VectorXd kwargs) {
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
	Eigen::VectorXd m0(6, 1);
	m0(0) = 4500*q*(m_aft_ps*(2 - 0.00050000000000000001*m_aft_ps) + m_aft_stb*(2 - 0.00050000000000000001*m_aft_stb) + m_fp_ps*(2 - 0.00050000000000000001*m_fp_ps) + m_fp_stb*(2 - 0.00050000000000000001*m_fp_stb) + 135000.0)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) - 4500*r*(-3.75*m_aft_ps + 3.75*m_aft_stb - 3.75*m_fp_ps + 3.75*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) + 4500*u;
	m0(1) = -8500*p*(m_aft_ps*(2 - 0.00050000000000000001*m_aft_ps) + m_aft_stb*(2 - 0.00050000000000000001*m_aft_stb) + m_fp_ps*(2 - 0.00050000000000000001*m_fp_ps) + m_fp_stb*(2 - 0.00050000000000000001*m_fp_stb) + 135000.0)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) + 8500*r*(-7.0*m_aft_ps - 7.0*m_aft_stb + 7.0*m_fp_ps + 7.0*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) + 8500*v;
	m0(2) = 33700*p*(-3.75*m_aft_ps + 3.75*m_aft_stb - 3.75*m_fp_ps + 3.75*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) - 33700*q*(-7.0*m_aft_ps - 7.0*m_aft_stb + 7.0*m_fp_ps + 7.0*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) + 33700*w;
	m0(3) = 800000*p - 4500*v*(m_aft_ps*(2 - 0.00050000000000000001*m_aft_ps) + m_aft_stb*(2 - 0.00050000000000000001*m_aft_stb) + m_fp_ps*(2 - 0.00050000000000000001*m_fp_ps) + m_fp_stb*(2 - 0.00050000000000000001*m_fp_stb) + 135000.0)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) + 4500*w*(-3.75*m_aft_ps + 3.75*m_aft_stb - 3.75*m_fp_ps + 3.75*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000);
	m0(4) = 800000*q + 8500*u*(m_aft_ps*(2 - 0.00050000000000000001*m_aft_ps) + m_aft_stb*(2 - 0.00050000000000000001*m_aft_stb) + m_fp_ps*(2 - 0.00050000000000000001*m_fp_ps) + m_fp_stb*(2 - 0.00050000000000000001*m_fp_stb) + 135000.0)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) - 8500*w*(-7.0*m_aft_ps - 7.0*m_aft_stb + 7.0*m_fp_ps + 7.0*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000);
	m0(5) = 1500000*r - 33700*u*(-3.75*m_aft_ps + 3.75*m_aft_stb - 3.75*m_fp_ps + 3.75*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) + 33700*v*(-7.0*m_aft_ps - 7.0*m_aft_stb + 7.0*m_fp_ps + 7.0*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000);
	return m0;
}