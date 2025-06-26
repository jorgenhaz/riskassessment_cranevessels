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
	m0(0) = 12964.523281596452*q + 6000*u;
	m0(1) = -21607.538802660754*p + 10000*v;
	m0(2) = 350000*w;
	m0(3) = 846688.57331084902*p - 21607.538802660754*v;
	m0(4) = 828013.14398650941*q + 12964.523281596452*u;
	m0(5) = 1500000*r;
	return m0;
}