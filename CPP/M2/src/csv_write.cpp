#include "csv_write.h"
#include <sstream>
#include <limits>
#include <sstream>
#include <cmath>

using namespace CSV;

CSV_Writer::CSV_Writer(std::string _fileName , const std::vector<std::string>& _headerColumns) 
    : fileName(_fileName), headerColumns(_headerColumns) {

    // Open file or create if it does not exists
    std::ofstream file(fileName, std::ios::trunc); 

    if (!file){
        std::cerr << "Could not open file" << fileName << std::endl;
    }

    if(file.is_open()){
        for (size_t i = 0; i<headerColumns.size(); i++){
            file << headerColumns[i];
            if (i != headerColumns.size()-1){
                file << ",";
            }
        }
        file << "\n";
    } else{
        std::cerr << "Could not open file " << fileName << std::endl;
    }

    file.close();
}

void CSV_Writer::openFile() {
    if(!file.is_open()){
        file.open(fileName, std::ios::out | std::ios::app);
        if (!file.is_open()){
            std::cerr << "Could not open file " << fileName << std::endl;
        }
    }
}

void CSV_Writer::closeFile() {
    if (file.is_open()){
        file.close();
    }
}

void CSV_Writer::writeLine(const std::vector<double>& rowData) {
    if (file.is_open()) {
        for (size_t i = 0; i < rowData.size(); i++) {
            file << rowData[i];
            if (i != rowData.size() - 1) {
                file << ",";
            }
        }
        file << "\n";
        file.flush();  // writing to disc immediately
    } else {
        std::cerr << "File is not open!" << std::endl;
    }
}

// Getting max absolute value
double CSV_Writer::getMax(std::string param){

    std::ifstream infile(fileName);

    if (!infile.is_open()) {
        std::cerr << "Could not open file " << fileName << std::endl;
        return std::numeric_limits<double>::quiet_NaN();
    }

    std::string line;
    // Get header
    std::getline(infile, line); 

    // Searching for param
    int target_col = -1;
    {
        std::stringstream ss(line);
        std::string col;
        int idx = 0;
        while (std::getline(ss, col, ',')) {
            if (col == param) {
                target_col = idx;
                break;
            }
            idx++;
        }
        if (target_col == -1) {
            std::cerr << "Parameter " << param << " not found in header." << std::endl;
            return std::numeric_limits<double>::quiet_NaN();
        }
    }

    // Initializing max_value
    double max_val = 0.0;
    // While new line exists
    while (std::getline(infile, line)) {
        std::stringstream ss(line);
        std::string val;
        int col = 0;
    
        // While delimiter ',' keeps coming
        while (std::getline(ss, val, ',')) {
            if (col == target_col) {
                try {
                    double num = std::stod(val);
                    max_val = std::max(max_val, std::abs(num)); // Checking if absolute value of param in next line is bigger
                } catch (...) {
                    std::cout<<"Could not convert to double"<<std::endl;
                }
                break;
            }
            col++; // Next column
        }
    }

    return max_val;
}



std::vector<double> CSV_Writer::integralSquare(const std::vector<std::string>& cols){
    if (file.is_open()) file.flush();     // Making sure everything is written

    std::vector<double> sum(cols.size(), 0.0);   // Number of cols to integrate
    std::vector<int>    colIdx(cols.size(), -1);  // Index-vector

    std::ifstream in(fileName);
    if (!in) return sum;                       

    std::string header;
    std::getline(in, header); // Getting header

    std::stringstream hs(header);
    std::string token;
    int csvCol = 0;
    while (std::getline(hs, token, ',')) { // Iterating through header with delimiter ',' and retrieving index
        for (std::size_t i = 0; i < cols.size(); ++i)
            if (token == cols[i]) { colIdx[i] = csvCol; break; }
        ++csvCol;
    }
    

    std::string line;
    // Iterating through indices found above
    while (std::getline(in, line)) {
        std::stringstream ls(line);
        std::string token;
        int csvCol = 0;
        while (std::getline(ls, token, ',')) {

            for (std::size_t i = 0; i < cols.size(); ++i)
                if (csvCol == colIdx[i]) {     
                    try {
                        double v = std::stod(token);
                        sum[i] += v * v;       
                    } catch (...) {}// Ignore non-numbers
                }
            ++csvCol;
        }
    }
    return sum;
}


// Clear CSV-file
void CSV_Writer::clearFile() {
    std::ofstream file(fileName, std::ios::trunc);
    if (file.is_open()) {
        for (size_t i = 0; i < headerColumns.size(); ++i) {
            file << headerColumns[i];
            if (i != headerColumns.size() - 1)
                file << ",";
        }
        file << "\n";
        file.close();
    } else {
        std::cerr << "Could not clear file " << fileName << std::endl;
    }
}

// Destructor
CSV_Writer::~CSV_Writer() {
    if (file.is_open()) {
        file.close();
    }
}


