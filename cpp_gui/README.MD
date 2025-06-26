# Model description
Boat: 6 DoF


# Compiling
rm -rf build/*
cmake -B build
cmake --build build -j$(nproc)
./build/<program>

## Compiler
**CMake:** ≥ 3.10
**Standard:** C++17
**Compiler:** g++ 13.3.0 (Ubuntu 24.04)