#include "R_n_b.h"

Eigen::MatrixXd R_n_b(Eigen::VectorXd kwargs) {
	double x = kwargs(0);
	double y = kwargs(1);
	double z = kwargs(2);
	double phi = kwargs(3);
	double theta = kwargs(4);
	double psi = kwargs(5);
	double t = kwargs(6);
	Eigen::MatrixXd m(3, 3);
	m(0, 0) = cos(psi)*cos(theta);
	m(0, 1) = sin(phi)*sin(theta)*cos(psi) - sin(psi)*cos(phi);
	m(0, 2) = sin(phi)*sin(psi) + sin(theta)*cos(phi)*cos(psi);
	m(1, 0) = sin(psi)*cos(theta);
	m(1, 1) = sin(phi)*sin(psi)*sin(theta) + cos(phi)*cos(psi);
	m(1, 2) = -sin(phi)*cos(psi) + sin(psi)*sin(theta)*cos(phi);
	m(2, 0) = -sin(theta);
	m(2, 1) = sin(phi)*cos(theta);
	m(2, 2) = cos(phi)*cos(theta);
	return m;
}