#include "beta.h"
#include "mass_inertia.h"
#include "D_q_dot.h"
#include "gamma_T_diff_omega.h"
#include "P_diff_q.h"
#include "T_diff_q.h"
#include "restoring.h"
#include "B_added_mass.h"
#include "C_added_mass.h"
#include <iostream>

Eigen::VectorXd model(Eigen::VectorXd kwargs) {
    
    Eigen::VectorXd q     = kwargs.segment(0, 12);
    Eigen::VectorXd p     = kwargs.segment(46, 12);
    Eigen::MatrixXd B     = mass_inertia(kwargs);
    
    Eigen::MatrixXd B_A   = B_added_mass(kwargs);
    
    Eigen::MatrixXd B_Tot = B + B_A;
    Eigen::MatrixXd Beta  = beta(kwargs);
    Eigen::MatrixXd Beta_transpose = Beta.transpose();
    
    Eigen::VectorXd omega = B_Tot.fullPivLu().solve(p);
    Eigen::VectorXd G_restoring = restoring(kwargs);

    Eigen::VectorXd dq    = Beta * omega;
    
    kwargs.segment(12,12)   = omega;
    Eigen::MatrixXd C_A     = C_added_mass(kwargs);
    Eigen::VectorXd tau     = kwargs.segment(24,12);
    Eigen::VectorXd potential = Beta_transpose * P_diff_q(kwargs);
    double kp = 8000.0;
    double kd = 4000.0;
    tau(6) = kp*(kwargs(40)-q(6)) - kd*omega(6) + potential(6);
    tau(7) = kp*(kwargs(41)-q(7)) - kd*omega(7) + potential(7);
    tau(8) = kp*(kwargs(42)-q(8)) - kd*omega(8) +  potential(8);
    tau(9) = kp*(kwargs(43)-q(9)) - kd*omega(9) + potential(9);

    
    Eigen::VectorXd dp    =   Beta_transpose * tau + C_A*omega-Beta_transpose*gamma_T_diff_omega(kwargs)+Beta_transpose*T_diff_q(kwargs)-potential-Beta_transpose * G_restoring-Beta_transpose * D_q_dot(kwargs);

    Eigen::VectorXd dx = Eigen::VectorXd::Zero(58);
    dx.segment(0, 12) = dq;
    dx.segment(46, 12) = dp;

    return dx;
}
