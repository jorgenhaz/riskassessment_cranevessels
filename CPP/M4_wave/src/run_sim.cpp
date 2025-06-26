#include "run_sim.h"

void run_sim(CSV::CSV_Writer &writer, std::vector<double> &y_val, double &t, double &dt, double &tol, double &safety, double &sim_time, double& wave_angle){
    writer.clearFile();
    writer.openFile();

    int step = 0;
    t = 0.0;
    double counter = 5.0;

    while (t < sim_time) { 
        std::vector<double> outputBuffer;
        Eigen::VectorXd kwargs_wave = Eigen::Map<Eigen::VectorXd>(y_val.data(), y_val.size());
        kwargs_wave[6] = t;  
        kwargs_wave[7] = wave_angle;
        Eigen::VectorXd wave_tau = wave_model(kwargs_wave);

        for (int i = 0; i<6; i++){
            y_val[24 + i] = wave_tau[i];
        }

        y_val = RK4::RK_classic_adaptive(model, t, y_val, dt, tol, safety);
        step++;
        outputBuffer.push_back(t);
        outputBuffer.insert(outputBuffer.end(), y_val.begin(), y_val.end());
        writer.writeLine(outputBuffer);

        if (t > counter){
            counter += 5.0;
            std::cout<<"Progress: "<<t<<std::endl;
        }
    }

    
    std::cout<<"Steps: "<<step<<std::endl;
    std::cout<<"Time: "<<t<<std::endl;

    writer.closeFile();
}