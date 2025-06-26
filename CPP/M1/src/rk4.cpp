#include "rk4.h"
#include <iostream>

std::vector<double> RK4::RK_classic(const ModelFunction& f, double t, const std::vector<double>& y, double dt){
    // Converting y-vector to eigen-vector
    Eigen::VectorXd y_eigen = Eigen::Map<const Eigen::VectorXd>(y.data(), y.size());

    // Calculating the k's
    Eigen::VectorXd k1 = f(y_eigen);
    Eigen::VectorXd k2 = f(y_eigen + 0.5 * dt * k1);
    Eigen::VectorXd k3 = f(y_eigen + 0.5 * dt * k2);
    Eigen::VectorXd k4 = f(y_eigen + dt * k3);
    
    // Calculating the next y
    Eigen::VectorXd y_next = y_eigen + dt * ((1.0/6.0) * k1 + (1.0/3.0) * k2 + (1.0/3.0) * k3 + (1.0/6.0) * k4);

    //Converting back to vector
    return std::vector<double>(y_next.data(), y_next.data() + y_next.size());
}

std::vector<double> RK4::RK_classic_adaptive(const ModelFunction& f, double& t, const std::vector<double>& y, double& dt, 
                                             double tol, double safety) {

    Eigen::VectorXd y_eigen = Eigen::Map<const Eigen::VectorXd>(y.data(), y.size());
    
    bool accept_step = false;
    Eigen::VectorXd y4, y5;
    
    while (!accept_step) {
        
        Eigen::VectorXd k1 = f(y_eigen);
        Eigen::VectorXd k2 = f(y_eigen + (dt * 1.0/4.0) * k1);
        Eigen::VectorXd k3 = f(y_eigen + dt * (3.0/32.0 * k1 + 9.0/32.0 * k2));
        Eigen::VectorXd k4 = f(y_eigen + dt * (1932.0/2197.0 * k1 - 7200.0/2197.0 * k2 + 7296.0/2197.0 * k3));
        Eigen::VectorXd k5 = f(y_eigen + dt * (439.0/216.0 * k1 - 8.0 * k2 + 3680.0/513.0 * k3 - 845.0/4104.0 * k4));
        Eigen::VectorXd k6 = f(y_eigen + dt * (-8.0/27.0 * k1 + 2.0 * k2 - 3544.0/2565.0 * k3 + 1859.0/4104.0 * k4 - 11.0/40.0 * k5));
        
        // 4th order solution (less precise)
        y4 = y_eigen + dt * (25.0/216.0 * k1 + 1408.0/2565.0 * k3 + 2197.0/4104.0 * k4 - 1.0/5.0 * k5);

        // 5th order solution (more precise)
        y5 = y_eigen + dt * (16.0/135.0 * k1 + 6656.0/12825.0 * k3 + 28561.0/56430.0 * k4 - 9.0/50.0 * k5 + 2.0/55.0 * k6);

        // Estimating error
        double error = (y5 - y4).norm();
        
        // Accept if error is within tolerance
        if (error < tol) {
            accept_step = true;
            t += dt;
        }

        // Update dt with safety-factor
        double scale = safety * std::pow(tol / (error + 1e-10), 0.2);  // +1e-10 to avoid division by zero
        dt *= std::clamp(scale, 0.2, 5.0);  
    }

    // Convert back to vec
    return std::vector<double>(y5.data(), y5.data() + y5.size());
}
