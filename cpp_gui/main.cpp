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
#include "wave_model.h"
#include "run_sim.h"
#include "sim_util.h"

int main(int argc, char const *argv[]) {
    std::vector<double> y_val;
    std::vector<std::string> header;
    std::string yaml_file_init = "cpp_gui/files/init.yaml";
    std::string yaml_file_sim = "cpp_gui/files/sim_args.yaml";

    // Initial values
    load_yaml(yaml_file_init, header, y_val);
    header.insert(header.begin(), "time");
    // Simulation values
    double t                = 0.0;
    double dt               = retrieve_parameter_yaml<double>(yaml_file_sim,"dt");
    double tol              = retrieve_parameter_yaml<double>(yaml_file_sim, "tol");
    double safety           = retrieve_parameter_yaml<double>(yaml_file_sim, "safety");
    double simulation_time  = retrieve_parameter_yaml<double>(yaml_file_sim, "simulation_time");
    double wave_angle       = retrieve_parameter_yaml<double>(yaml_file_sim, "wave_angle");
    std::string file_name   = retrieve_parameter_yaml<std::string>(yaml_file_sim, "file_name");

    CSV::CSV_Writer writer(file_name, header);

    //____________________________________________________________________
    Eigen::VectorXd q_dot_init(6);
    q_dot_init << 0.0, 0.0, 0.0, 0.0, 0.0, 0.0;

    // Mass and transformation matrices
    Eigen::VectorXd y_vec = Eigen::Map<Eigen::VectorXd>(y_val.data(), y_val.size());
    Eigen::MatrixXd B = mass_inertia(y_vec);
    Eigen::MatrixXd beta_mat = beta(y_vec);
    // Calculate p = B * beta⁻¹ * q_dot
    Eigen::VectorXd p = B * beta_mat.fullPivLu().solve(q_dot_init);

    // Insert p into y_val starting at index 25
    for (int i = 0; i < 6; ++i) {
        y_val[22 + i] = p[i];
    }

    //_________________________________________________________

    if (argc == y_val.size() + 1){
        std::vector<double> arg_values;
        double value;
        for (int i = 1; i < argc; i++){
            std::istringstream iss(argv[i]);
            if (iss >> value && iss.eof()){
                arg_values.push_back(value);
            }else{
                std::cerr << "Unvalid number in argument " << i 
                << " ('" << argv[i] << "') ignore or quitting.\n";
                return 1; 
            }
        }
        y_val = arg_values;
    }

    auto start = std::chrono::high_resolution_clock::now();
    run_sim(writer, y_val, t, dt, tol, safety, simulation_time, wave_angle);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> duration = end - start;
    std::cout << "Total time: " << duration.count() << " seconds" << std::endl;
    std::cout << "Simulation-time: " << simulation_time << std::endl;

    return 0;
} 
