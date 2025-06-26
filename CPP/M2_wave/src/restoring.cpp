#include "restoring.h"

Eigen::VectorXd restoring(Eigen::VectorXd kwargs) {
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
	Eigen::VectorXd m6(6, 1);
	m6(0) = 0;
	m6(1) = 0;
	m6(2) = 1282044.375*z;
	m6(3) = phi*(9.8100000000000005*m_aft_ps + 9.8100000000000005*m_aft_stb + 9.8100000000000005*m_fp_ps + 9.8100000000000005*m_fp_stb + 588600.0)*(-3.8259206121472981e-6*m_aft_ps - 3.8259206121472981e-6*m_aft_stb - 3.8259206121472981e-6*m_fp_ps - 3.8259206121472981e-6*m_fp_stb - 2.3903091169949131 - 341.66666666666663/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) + 767.65625/((1.0/1025.0)*m_aft_ps + (1.0/1025.0)*m_aft_stb + (1.0/1025.0)*m_fp_ps + (1.0/1025.0)*m_fp_stb + 2400.0/41.0));
	m6(4) = 10055.25*theta*((1.0/1025.0)*m_aft_ps + (1.0/1025.0)*m_aft_stb + (1.0/1025.0)*m_fp_ps + (1.0/1025.0)*m_fp_stb + 2400.0/41.0)*(-3.8259206121472981e-6*m_aft_ps - 3.8259206121472981e-6*m_aft_stb - 3.8259206121472981e-6*m_fp_ps - 3.8259206121472981e-6*m_fp_stb - 2.3903091169949131 + 2390.625/((1.0/1025.0)*m_aft_ps + (1.0/1025.0)*m_aft_stb + (1.0/1025.0)*m_fp_ps + (1.0/1025.0)*m_fp_stb + 2400.0/41.0));
	m6(5) = 0;
	return m6;
}