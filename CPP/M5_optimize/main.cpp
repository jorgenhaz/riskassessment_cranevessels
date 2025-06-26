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
#include "optimizing.h"

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

    /*Optimizing parameters*/
    auto start = std::chrono::high_resolution_clock::now();
    double alpha = 10000.0;             // step length
    double h = 100.0;               // difference element
    double epsilon = 0.002;//was 0.005 - 0.002 much better          // convergence tolerance
    int max_iter = 100;             // maximum iterations

    std::vector<double> x(4);
    std::vector<double> x_new = x;
    for (int i = 0; i<4;i++){
        x[i] = y_val[24+i];
    }
    /*Optimizing parameters END*/

    int iterations_optimizing = 0;

    //Optimizing
    writer.openFile();

    auto simulate = [&](std::vector<double>& y) {
    double t_local = 0.0;                 // <- egen klokke
    run_sim(writer, y, t_local, dt, tol, safety, simulation_time);
        };
    for (int iter = 0; iter < max_iter; iter++){
        std::cout<<"iteration: "<<iter<<std::endl;
        iterations_optimizing ++;
        std::vector<double> grad(x.size());

        for (int j = 0; j < x.size(); j++){
            std::vector<double> y_plus = y_val;
            std::vector<double> y_minus = y_val;

            for (int i = 0; i<x.size(); i++){
                y_plus[24+i] = x[i];
                y_minus[24+i] = x[i];
            }

            y_plus[24+j] += h;
            y_minus[24+j] -= h;
       
            simulate(y_plus);
            std::vector<double> x_plus  = x;  x_plus [j] += h;
            double f_plus = OPT::eval_F(writer, x_plus);
 
            simulate(y_minus);
            std::vector<double> x_minus = x;  x_minus[j] -= h;
            double f_minus = OPT::eval_F(writer, x_minus);

            grad[j] = (f_plus - f_minus)/(2*h);
        }
        
        if(OPT::norm(grad) < epsilon){
            std::cout << "Converged" << std::endl;
            break;
        }
        for (int i = 0; i < x.size(); i++){
            x[i] -= alpha * grad[i];
            x[i] = std::max(0.0, std::min(10000.0, x[i]));
            y_val[24+i] = x[i];
            std::cout<<x[i]<<std::endl;
        }
    }


    auto end = std::chrono::high_resolution_clock::now();
    t = 0.0;
    run_sim(writer,y_val, t, dt, tol, safety, simulation_time);
    std::chrono::duration<double> duration = end - start;
    std::cout << "Total time: " << duration.count() << " seconds" << std::endl;
    std::cout << "Simulation-time: " << simulation_time << std::endl;
    std::cout << "Iterations optimizing: " << iterations_optimizing << std::endl;

    return 0;
} 