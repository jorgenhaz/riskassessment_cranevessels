#ifndef RUN_SIM_H
#define RUN_SIM_h

#include <iostream>
#include "csv_write.h"
#include "model.h"
#include "rk4.h"
#include "wave_model.h"

void run_sim(CSV::CSV_Writer &writer, std::vector<double> &y_init, 
    double &t, double &dt, double &tol, double &safety, 
    double &sim_time, double& wave_angle);


#endif