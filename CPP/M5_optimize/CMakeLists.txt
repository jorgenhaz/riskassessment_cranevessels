# Minimum CMake version
cmake_minimum_required(VERSION 3.10)

# Project-name
project(MyProgram)

# C++-standard 
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Compiler flags 
set(CMAKE_CXX_FLAGS "-O2 -march=native -funroll-loops -flto")

find_package(yaml-cpp REQUIRED)
find_package(Eigen3 QUIET CONFIG)

# Static libraries
add_library(my_lib STATIC
    src/csv_write.cpp
    src/rk4.cpp
    src/model.cpp
    src/beta.cpp 
    src/mass_inertia.cpp 
    src/R_n_b.cpp 
    src/B_added_mass.cpp 
    src/C_added_mass.cpp 
    src/D_q_dot.cpp 
    src/gamma_T_diff_omega.cpp 
    src/P_diff_q.cpp 
    src/restoring.cpp 
    src/T_diff_q.cpp
    src/run_sim.cpp 
    src/sim_util.cpp 
    src/optimizing.cpp 
)

message(STATUS "C++ compiler: ${CMAKE_CXX_COMPILER}")

# Folders for include-files
target_include_directories(my_lib
    PUBLIC
        include
        $<BUILD_INTERFACE:${Eigen3_INCLUDE_DIRS}>     
        $<INSTALL_INTERFACE:include>
)

target_link_libraries(my_lib
    PUBLIC
        yaml-cpp
        $<$<BOOL:${Eigen3_FOUND}>:Eigen3::Eigen>     
)

# Make executable
add_executable(my_program main.cpp)
target_link_libraries(my_program PRIVATE my_lib)