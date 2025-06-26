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
	Eigen::VectorXd m4(6, 1);
	m4(0) = 0;
	m4(1) = 0;
	m4(2) = -1250775.0*theta*(-7.0*m_aft_ps - 7.0*m_aft_stb + 7.0*m_fp_ps + 7.0*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) + 1250775.0*z;
	m4(3) = phi*(9.8100000000000005*m_aft_ps + 9.8100000000000005*m_aft_stb + 9.8100000000000005*m_fp_ps + 9.8100000000000005*m_fp_stb + 588600.0)*(-3.9215686274509803e-6*m_aft_ps - 3.9215686274509803e-6*m_aft_stb - 3.9215686274509803e-6*m_fp_ps - 3.9215686274509803e-6*m_fp_stb - 0.23529411764705882 - (m_aft_ps*(2 - 0.00050000000000000001*m_aft_ps) + m_aft_stb*(2 - 0.00050000000000000001*m_aft_stb) + m_fp_ps*(2 - 0.00050000000000000001*m_fp_ps) + m_fp_stb*(2 - 0.00050000000000000001*m_fp_stb) + 135000.0)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) - 333.33333333333331/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) + 767.65625/((1.0/1000.0)*m_aft_ps + (1.0/1000.0)*m_aft_stb + (1.0/1000.0)*m_fp_ps + (1.0/1000.0)*m_fp_stb + 60));
	m4(4) = theta*(9.8100000000000005*m_aft_ps + 9.8100000000000005*m_aft_stb + 9.8100000000000005*m_fp_ps + 9.8100000000000005*m_fp_stb + 588600.0)*(-3.9215686274509803e-6*m_aft_ps - 3.9215686274509803e-6*m_aft_stb - 3.9215686274509803e-6*m_fp_ps - 3.9215686274509803e-6*m_fp_stb - 0.23529411764705882 - (m_aft_ps*(2 - 0.00050000000000000001*m_aft_ps) + m_aft_stb*(2 - 0.00050000000000000001*m_aft_stb) + m_fp_ps*(2 - 0.00050000000000000001*m_fp_ps) + m_fp_stb*(2 - 0.00050000000000000001*m_fp_stb) + 135000.0)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000) + 2390.625/((1.0/1000.0)*m_aft_ps + (1.0/1000.0)*m_aft_stb + (1.0/1000.0)*m_fp_ps + (1.0/1000.0)*m_fp_stb + 60)) - 1250775.0*z*(-7.0*m_aft_ps - 7.0*m_aft_stb + 7.0*m_fp_ps + 7.0*m_fp_stb)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + 60000);
	m4(5) = 0;
	return m4;
}