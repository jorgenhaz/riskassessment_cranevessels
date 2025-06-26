#include "restoring.h"

Eigen::VectorXd restoring(Eigen::VectorXd kwargs) {
	double x = kwargs(0);
	double y = kwargs(1);
	double z = kwargs(2);
	double phi = kwargs(3);
	double theta = kwargs(4);
	double psi = kwargs(5);
	double q1_p = kwargs(6);
	double q2_p = kwargs(7);
	double u = kwargs(8);
	double v = kwargs(9);
	double w = kwargs(10);
	double p = kwargs(11);
	double q = kwargs(12);
	double r = kwargs(13);
	double q1_pdot = kwargs(14);
	double q2_pdot = kwargs(15);
	double tau_xn = kwargs(16);
	double tau_yn = kwargs(17);
	double tau_zn = kwargs(18);
	double tau_phi = kwargs(19);
	double tau_theta = kwargs(20);
	double tau_psi = kwargs(21);
	double tau_q1p = kwargs(22);
	double tau_q2p = kwargs(23);
	double m_fp_stb = kwargs(24);
	double m_fp_ps = kwargs(25);
	double m_aft_stb = kwargs(26);
	double m_aft_ps = kwargs(27);
	double m_payload = kwargs(28);
	double wire_length = kwargs(29);
	double q1 = kwargs(30);
	double q2 = kwargs(31);
	double q3 = kwargs(32);
	double q4 = kwargs(33);
	Eigen::VectorXd m4(8, 1);
	m4(0) = 0;
	m4(1) = 0;
	m4(2) = 1282044.375*z;
	m4(3) = phi*(9.8100000000000005*m_aft_ps + 9.8100000000000005*m_aft_stb + 9.8100000000000005*m_fp_ps + 9.8100000000000005*m_fp_stb + 9.8100000000000005*m_payload + 594976.5)*(-3.8259206121472981e-6*m_aft_ps - 3.8259206121472981e-6*m_aft_stb - 3.8259206121472981e-6*m_fp_ps - 3.8259206121472981e-6*m_fp_stb + m_payload*wire_length/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + m_payload + 60650) - 3.8259206121472981e-6*m_payload - 0.23204208512673363 - (m_aft_ps*(2 - 0.00048780487804878049*m_aft_ps) + m_aft_stb*(2 - 0.00048780487804878049*m_aft_stb) + m_fp_ps*(2 - 0.00048780487804878049*m_fp_ps) + m_fp_stb*(2 - 0.00048780487804878049*m_fp_stb) + m_payload*(-1.0*q4*sin(q2 + q3) - wire_length*(sin(q2_p)*sin(q2 + q3) - cos(q1_p)*cos(q2_p)*cos(q2 + q3)) - 2.0*sin(q2) - 1.2000000000000002*sin(q2 + q3) - 3.0) - 100.0*q4*sin(q2 + q3) - 200*(-1.0/2.0*q4 - 1.0/2.0)*sin(q2 + q3) - 600.0*sin(q2) - 140.0*sin(q2 + q3) + 133450.0)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + m_payload + 60650) - 341.66666666666663/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + m_payload + 60650) + 767.65625/((1.0/1025.0)*m_aft_ps + (1.0/1025.0)*m_aft_stb + (1.0/1025.0)*m_fp_ps + (1.0/1025.0)*m_fp_stb + (1.0/1025.0)*m_payload + 2426.0/41.0));
	m4(4) = 10055.25*theta*((1.0/1025.0)*m_aft_ps + (1.0/1025.0)*m_aft_stb + (1.0/1025.0)*m_fp_ps + (1.0/1025.0)*m_fp_stb + (1.0/1025.0)*m_payload + 2426.0/41.0)*(-3.8259206121472981e-6*m_aft_ps - 3.8259206121472981e-6*m_aft_stb - 3.8259206121472981e-6*m_fp_ps - 3.8259206121472981e-6*m_fp_stb - 3.8259206121472981e-6*m_payload - 0.23204208512673363 - (m_aft_ps*(2 - 0.00048780487804878049*m_aft_ps) + m_aft_stb*(2 - 0.00048780487804878049*m_aft_stb) + m_fp_ps*(2 - 0.00048780487804878049*m_fp_ps) + m_fp_stb*(2 - 0.00048780487804878049*m_fp_stb) + m_payload*(-1.0*q4*sin(q2 + q3) - wire_length*(sin(q2_p)*sin(q2 + q3) - cos(q1_p)*cos(q2_p)*cos(q2 + q3)) - 2.0*sin(q2) - 1.2000000000000002*sin(q2 + q3) - 3.0) - 100.0*q4*sin(q2 + q3) - 200*(-1.0/2.0*q4 - 1.0/2.0)*sin(q2 + q3) - 600.0*sin(q2) - 140.0*sin(q2 + q3) + 133450.0)/(m_aft_ps + m_aft_stb + m_fp_ps + m_fp_stb + m_payload + 60650) + 2390.625/((1.0/1025.0)*m_aft_ps + (1.0/1025.0)*m_aft_stb + (1.0/1025.0)*m_fp_ps + (1.0/1025.0)*m_fp_stb + (1.0/1025.0)*m_payload + 2426.0/41.0));
	m4(5) = 0;
	m4(6) = 0;
	m4(7) = 0;
	return m4;
}