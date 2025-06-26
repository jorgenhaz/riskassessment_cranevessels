#ifndef SIM_UTIL_H
#define SIM_UTIL_H

#include <yaml-cpp/yaml.h>
#include <vector>
#include <string>
#include <stdexcept>

void load_yaml(const std::string& file, std::vector<std::string>& header, std::vector<double>& y_val);

template<typename T>
T retrieve_parameter_yaml(const std::string& file, const std::string& param){
    YAML::Node config = YAML::LoadFile(file);
    if(!config){
        throw std::runtime_error("Could not open YAML file: " + file);
    }
    if(!config[param]){
        throw std::runtime_error("Could not find parameter: " + param);
    }

    try{
        return config[param].as<T>();
    }
    catch (const YAML::BadConversion& e){
        throw std::runtime_error("Bad conversion for '" + param + "': " +e.what());
    }
}


#endif