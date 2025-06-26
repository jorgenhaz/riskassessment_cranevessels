#ifndef RK4_H
#define RK4_H

#include <iostream>
#include <vector>
#include <functional>
#include <Eigen/Dense>
#include <cmath>
namespace RK4
{
    // Alias for function type
    using ModelFunction = std::function<Eigen::VectorXd(const Eigen::VectorXd&)>;

    std::vector<double> RK_classic(const ModelFunction& f, double t, const std::vector<double>& y, double dt);
    std::vector<double> RK_classic_adaptive(const ModelFunction& f, double& t, const std::vector<double>& y, double& dt, 
        double tol, double safety);
} // namespace RK4

#endif