#include "optimizing.h"

using namespace OPT;

double OPT::eval_F (CSV::CSV_Writer& writer, std::vector<double>& x){

    auto I = writer.integralSquare({"phi", "theta"});

    double phi_integral = I[0];
    double theta_integral = I[1];

    double weight_phi = 1.0;
    double weight_theta = 1.0;

    double penalty = 0.0;

    double max_vol = 10000.0;
    double min_vol = 0.0;

    for (int i = 0; i <x.size(); i++){
        double vol = x[i];
        if (vol < min_vol){
            penalty += 1000000.0 * std::pow(min_vol - vol, 2);
        }
        else if (vol > max_vol){
            penalty += 1000000.0 * std::pow(vol - max_vol, 2);
        }
    }

    return weight_phi * phi_integral + weight_theta * theta_integral + penalty;
}

double OPT::norm(const std::vector<double>& v) {
    double sum = 0.0;
    for (double val : v)
        sum += val * val;
    return std::sqrt(sum);
}