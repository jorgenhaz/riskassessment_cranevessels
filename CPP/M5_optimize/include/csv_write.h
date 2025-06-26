#ifndef CSV_WRITE_H
#define CSV_WRITE_H

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

namespace CSV{

class CSV_Writer {
    public:
        CSV_Writer(std::string _fileName, const std::vector<std::string>& _headerColumns);
        void openFile();
        void closeFile();
        void writeLine(const std::vector<double>& rowData);
        double getMax(std::string param);
        void clearFile();  // deklarasjon
        std::vector<double> integralSquare (const std::vector<std::string>& cols);


        ~CSV_Writer();
    private:
        std::string fileName;
        std::vector<std::string> headerColumns;
        std::ofstream file;
};

}
#endif