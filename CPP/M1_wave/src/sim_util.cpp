#include "sim_util.h"

void load_yaml(const std::string& file, std::vector<std::string>& header, std::vector<double>& y_val){
    YAML::Node root = YAML::LoadFile(file);

    for (auto it = root.begin(); it != root.end(); it++){
        const std::string key = it->first.as<std::string>(); // First line as string
        const YAML::Node& val = it->second;
        
        // val = 0 if no val found
        if(val.IsNull()){
            header.push_back(key);
            y_val.push_back(0.0);
        }
        // val = scalar then push this
        else if(val.IsScalar()){
            header.push_back(key);
            y_val.push_back(val.as<double>());
        }
    }
}