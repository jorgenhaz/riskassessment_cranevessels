#include <iostream>
#include <vector>
#include "model.h"
#include "csv_write.h"
#include <chrono>
#include "rk4.h"
#include <sstream>
#include <string>
#include "beta.h"
#include "mass_inertia.h"
#include <Eigen/Dense>
#include "run_sim.h"
#include "sim_util.h"

int main(int argc, char const *argv[]) {
    std::vector<double> y_val;
    std::vector<std::string> header;
    std::string yaml_file_init = "files/init.yaml";
    std::string yaml_file_sim = "files/sim_args.yaml";

    // Initial values
    load_yaml(yaml_file_init, header, y_val);
    header.insert(header.begin(), "time");
    
    // Simulation values
    double t                = 0.0;
    double dt               = retrieve_parameter_yaml<double>(yaml_file_sim,"dt");
    double tol              = retrieve_parameter_yaml<double>(yaml_file_sim, "tol");
    double safety           = retrieve_parameter_yaml<double>(yaml_file_sim, "safety");
    double simulation_time  = retrieve_parameter_yaml<double>(yaml_file_sim, "simulation_time");
    std::string file_name   = retrieve_parameter_yaml<std::string>(yaml_file_sim, "file_name");

    CSV::CSV_Writer writer(file_name, header);
    
    auto start = std::chrono::high_resolution_clock::now();
    run_sim(writer, y_val, t, dt, tol, safety, simulation_time);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> duration = end - start;
    std::cout << "Total time: " << duration.count() << " seconds" << std::endl;
    std::cout << "Simulation-time: " << simulation_time << std::endl;

    return 0;
} 