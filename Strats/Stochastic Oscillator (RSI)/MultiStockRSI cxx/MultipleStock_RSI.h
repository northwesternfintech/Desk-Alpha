//
// Created by Jerry C on 1/3/23.
//

#pragma once

#include <iostream>
#include <map>
#include <string>
#include <list>
#include <ctime>
#include <any>

using namespace std;




class TemplateStrategy{

public:
    using Stock_Dict = std::map<std::string, std::any>;
    using Stocks_Dict = std::map<std::string, Stock_Dict>;
    using Orders_Dict = std::map<std::string, std::list<std::string>>;

    // Constructor
    TemplateStrategy(Stocks_Dict stocks_data);

    // Getters
    Stocks_Dict get_data();
    Orders_Dict get_orders();
    int get_ticks ();
    Stock_Dict get_stock_data(std::string ticker);

    // Setters
    void set_data(Stocks_Dict new_data);
    void set_orders(Orders_Dict new_orders);
    void set_ticks(int new_tick);
    void set_stock_data(std::string ticker, Stock_Dict single_stock_data);


private:
    int ticks_ = 0;
    Stocks_Dict stocks_data_;
    Orders_Dict orders_;

    void update_stock(std::string ticker, Stock_Dict data);

public:

    void clear_orders();
    TemplateStrategy::Orders_Dict update_all(Stocks_Dict new_data);

};