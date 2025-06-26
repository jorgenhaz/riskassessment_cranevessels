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
    
    Eigen::VectorXd q     = kwargs.segment(0, 6);
    Eigen::VectorXd p     = kwargs.segment(22, 6);
    Eigen::MatrixXd B     = mass_inertia(kwargs);
    
    Eigen::MatrixXd B_A   = B_added_mass(kwargs);
    
    Eigen::MatrixXd B_Tot = B + B_A;
    Eigen::MatrixXd Beta  = beta(kwargs);
    Eigen::MatrixXd Beta_transpose = Beta.transpose();
    
    Eigen::VectorXd omega = B_Tot.fullPivLu().solve(p);
    Eigen::VectorXd G_restoring = restoring(kwargs);

    Eigen::VectorXd dq    = Beta * omega;
    
    kwargs.segment(6,6)   = omega;
    Eigen::MatrixXd C_A     = C_added_mass(kwargs);
    Eigen::VectorXd tau     = kwargs.segment(12,6);
    Eigen::VectorXd dp    =   Beta_transpose * tau + C_A*omega-Beta_transpose*gamma_T_diff_omega(kwargs)+Beta_transpose*T_diff_q(kwargs)-Beta_transpose*P_diff_q(kwargs)-Beta_transpose * G_restoring-Beta_transpose * D_q_dot(kwargs);

    Eigen::VectorXd dx = Eigen::VectorXd::Zero(28);
    dx.segment(0, 6) = dq;
    dx.segment(22, 6) = dp;

    return dx;
}
