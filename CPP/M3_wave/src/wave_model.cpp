#include "wave_model.h"
#include "dynamic_pressure.h"
#include "worldframepoints.h"
#include "vectors_cog.h"
#include "R_n_b.h"
#include "wave_accelerations.h"
#include "B_added_mass.h"
#include <iostream>
#include <Eigen/Dense>

Eigen::VectorXd wave_model( Eigen::VectorXd& kwargs) {
    Eigen::MatrixXd world_points_num = worldframepoints(kwargs);

    Eigen::VectorXd cog_kwargs = kwargs.segment(36,4);
    Eigen::MatrixXd cog_vectors = vectors_cog(cog_kwargs);

    Eigen::Vector3d F_vec = Eigen::Vector3d::Zero();
    Eigen::Vector3d M_vec = Eigen::Vector3d::Zero();

    Eigen::VectorXd p_D_arg(5);

    p_D_arg[3] = kwargs[6];  // time in index 6
    p_D_arg[4] = kwargs[7];  // wave angle

    Eigen::MatrixXd B_A = B_added_mass(kwargs).block<3,3>(0,0);
    Eigen::MatrixXd R_b_n = R_n_b(kwargs).transpose();

    int N = world_points_num.cols();

    for (int i = 0; i < N; ++i) {
        p_D_arg.segment<3>(0) = world_points_num.col(i);
        Eigen::VectorXd p_D_i_vec = dynamic_pressure(p_D_arg);
        double p_D_i = p_D_i_vec[0];  // eller p_D_i_vec(i) hvis du vil ha komponent i


        Eigen::Vector3d F_vec_i_ned(0, 0, p_D_i);  // kraft i z-retning
        F_vec_i_ned += B_A * R_b_n * wave_accelerations(p_D_arg);
        Eigen::Vector3d F_vec_i = F_vec_i_ned;
        F_vec += F_vec_i_ned;

        Eigen::Vector3d r = cog_vectors.col(i);
        M_vec += r.cross(F_vec_i);
    }

    F_vec =  (F_vec);
    M_vec =  (M_vec);
    Eigen::VectorXd result(6);
    result << F_vec, M_vec;
    return result;
}