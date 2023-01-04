#include <iostream>
#include "MultipleStock_RSI.h"

int main() {
    std::cout << "Hello, World!" << std::endl;

    TemplateStrategy::Stocks_Dict data = {
            {"APPL", {{"price", 100.0},
                             {"trend", "upwards"},
                             {"volume", 100000}}},
            {"FISV", {{"price", 50.0},
                             {"trend", "downwards"},
                             {"volume", 20000}}},
            {"PAR", {{"price", 50.0},
                             {"trend", "downwards"},
                             {"volume", 20000}}}};

    TemplateStrategy strategy(data);

    return 0;
}
