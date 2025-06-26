#ifndef OPTIMIZING_H
#define OPTIMIZING_H

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cmath>  
#include "csv_write.h"
#include <Eigen/Dense>

namespace OPT{

    double eval_F (CSV::CSV_Writer& writer, std::vector<double>& x);
    double norm(const std::vector<double>& v); 
}
#endif