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
	Eigen::VectorXd m4(6, 1);
	m4(0) = 6000*q*(m_aft_ps*(2 - 0.00048780487804878049*m_aft_ps) + m_aft_stb*(2 - 0.00048780487804878049*m_aft_stb) + m_fp_ps*(2 - 0.00048780487804878049*m_fp_ps) + m_fp_stb*(2 - 0.00048780487804878049*m_fp_stb) + 135000.0)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) - 6000*r*(-3.75*m_aft_ps + 3.75*m_aft_stb - 3.75*m_fp_ps + 3.75*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) + 6000*u;
	m4(1) = -10000*p*(m_aft_ps*(2 - 0.00048780487804878049*m_aft_ps) + m_aft_stb*(2 - 0.00048780487804878049*m_aft_stb) + m_fp_ps*(2 - 0.00048780487804878049*m_fp_ps) + m_fp_stb*(2 - 0.00048780487804878049*m_fp_stb) + 135000.0)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) + 10000*r*(-7.0*m_aft_ps - 7.0*m_aft_stb + 7.0*m_fp_ps + 7.0*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) + 10000*v;
	m4(2) = 350000*p*(-3.75*m_aft_ps + 3.75*m_aft_stb - 3.75*m_fp_ps + 3.75*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) - 350000*q*(-7.0*m_aft_ps - 7.0*m_aft_stb + 7.0*m_fp_ps + 7.0*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) + 350000*w;
	m4(3) = p*(350000*(14.0625*pow(-m_aft_ps + m_aft_stb - m_fp_ps + m_fp_stb, 2))/pow(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000, 2) + 800000 + 10000*(18225000000.0*pow(7.4074074074074075e-6*m_aft_ps*(2 - 0.00048780487804878049*m_aft_ps) + 7.4074074074074075e-6*m_aft_stb*(2 - 0.00048780487804878049*m_aft_stb) + 7.4074074074074075e-6*m_fp_ps*(2 - 0.00048780487804878049*m_fp_ps) + 7.4074074074074075e-6*m_fp_stb*(2 - 0.00048780487804878049*m_fp_stb) + 1, 2))/pow(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000, 2)) - 350000*q*(-7.0*m_aft_ps - 7.0*m_aft_stb + 7.0*m_fp_ps + 7.0*m_fp_stb)*(-3.75*m_aft_ps + 3.75*m_aft_stb - 3.75*m_fp_ps + 3.75*m_fp_stb)/pow(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000, 2) - 10000*r*(-7.0*m_aft_ps - 7.0*m_aft_stb + 7.0*m_fp_ps + 7.0*m_fp_stb)*(m_aft_ps*(2 - 0.00048780487804878049*m_aft_ps) + m_aft_stb*(2 - 0.00048780487804878049*m_aft_stb) + m_fp_ps*(2 - 0.00048780487804878049*m_fp_ps) + m_fp_stb*(2 - 0.00048780487804878049*m_fp_stb) + 135000.0)/pow(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000, 2) - 10000*v*(m_aft_ps*(2 - 0.00048780487804878049*m_aft_ps) + m_aft_stb*(2 - 0.00048780487804878049*m_aft_stb) + m_fp_ps*(2 - 0.00048780487804878049*m_fp_ps) + m_fp_stb*(2 - 0.00048780487804878049*m_fp_stb) + 135000.0)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) + 350000*w*(-3.75*m_aft_ps + 3.75*m_aft_stb - 3.75*m_fp_ps + 3.75*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000);
	m4(4) = -350000*p*(-7.0*m_aft_ps - 7.0*m_aft_stb + 7.0*m_fp_ps + 7.0*m_fp_stb)*(-3.75*m_aft_ps + 3.75*m_aft_stb - 3.75*m_fp_ps + 3.75*m_fp_stb)/pow(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000, 2) + q*(350000*(49.0*pow(-m_aft_ps - m_aft_stb + m_fp_ps + m_fp_stb, 2))/pow(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000, 2) + 800000 + 6000*(18225000000.0*pow(7.4074074074074075e-6*m_aft_ps*(2 - 0.00048780487804878049*m_aft_ps) + 7.4074074074074075e-6*m_aft_stb*(2 - 0.00048780487804878049*m_aft_stb) + 7.4074074074074075e-6*m_fp_ps*(2 - 0.00048780487804878049*m_fp_ps) + 7.4074074074074075e-6*m_fp_stb*(2 - 0.00048780487804878049*m_fp_stb) + 1, 2))/pow(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000, 2)) - 6000*r*(-3.75*m_aft_ps + 3.75*m_aft_stb - 3.75*m_fp_ps + 3.75*m_fp_stb)*(m_aft_ps*(2 - 0.00048780487804878049*m_aft_ps) + m_aft_stb*(2 - 0.00048780487804878049*m_aft_stb) + m_fp_ps*(2 - 0.00048780487804878049*m_fp_ps) + m_fp_stb*(2 - 0.00048780487804878049*m_fp_stb) + 135000.0)/pow(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000, 2) + 6000*u*(m_aft_ps*(2 - 0.00048780487804878049*m_aft_ps) + m_aft_stb*(2 - 0.00048780487804878049*m_aft_stb) + m_fp_ps*(2 - 0.00048780487804878049*m_fp_ps) + m_fp_stb*(2 - 0.00048780487804878049*m_fp_stb) + 135000.0)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) - 350000*w*(-7.0*m_aft_ps - 7.0*m_aft_stb + 7.0*m_fp_ps + 7.0*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000);
	m4(5) = -10000*p*(-7.0*m_aft_ps - 7.0*m_aft_stb + 7.0*m_fp_ps + 7.0*m_fp_stb)*(m_aft_ps*(2 - 0.00048780487804878049*m_aft_ps) + m_aft_stb*(2 - 0.00048780487804878049*m_aft_stb) + m_fp_ps*(2 - 0.00048780487804878049*m_fp_ps) + m_fp_stb*(2 - 0.00048780487804878049*m_fp_stb) + 135000.0)/pow(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000, 2) - 6000*q*(-3.75*m_aft_ps + 3.75*m_aft_stb - 3.75*m_fp_ps + 3.75*m_fp_stb)*(m_aft_ps*(2 - 0.00048780487804878049*m_aft_ps) + m_aft_stb*(2 - 0.00048780487804878049*m_aft_stb) + m_fp_ps*(2 - 0.00048780487804878049*m_fp_ps) + m_fp_stb*(2 - 0.00048780487804878049*m_fp_stb) + 135000.0)/pow(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000, 2) + r*(10000*(49.0*pow(-m_aft_ps - m_aft_stb + m_fp_ps + m_fp_stb, 2))/pow(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000, 2) + 6000*(14.0625*pow(-m_aft_ps + m_aft_stb - m_fp_ps + m_fp_stb, 2))/pow(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000, 2) + 1500000) - 6000*u*(-3.75*m_aft_ps + 3.75*m_aft_stb - 3.75*m_fp_ps + 3.75*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) + 10000*v*(-7.0*m_aft_ps - 7.0*m_aft_stb + 7.0*m_fp_ps + 7.0*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000);
	return m4;
}