#include "Multiple_Stocks_Template.h"
#include <iostream>
#include <map>
#include <string>
#include <list>
#include <ctime>
#include <any>



// Constructor
TemplateStrategy::TemplateStrategy(Stocks_Dict stocks_data)
    : stocks_data_(stocks_data)
{
    Stocks_Dict::iterator stock;
    for (stock = stocks_data_.begin(); stock != stocks_data_.end(); stock++) {
        stock->second["trend"] = "downwards";
    }
}



// Getters
TemplateStrategy::Stocks_Dict
TemplateStrategy::get_data() {
    return stocks_data_;
}

TemplateStrategy::Orders_Dict
TemplateStrategy::get_orders() {
    return orders_;
}

int TemplateStrategy::get_ticks() {
    return ticks_;
}

TemplateStrategy::Stock_Dict
TemplateStrategy::get_stock_data(std::string ticker) {
    return stocks_data_[ticker];
}



// Setters

void TemplateStrategy::set_data(TemplateStrategy::Stocks_Dict new_data) {
    stocks_data_ = new_data;
}

void TemplateStrategy::set_orders(TemplateStrategy::Orders_Dict new_orders) {
    orders_ = new_orders;
}

void TemplateStrategy::set_ticks(int new_tick) {
    ticks_ = new_tick;
}

void TemplateStrategy::set_stock_data(std::string ticker, TemplateStrategy::Stock_Dict single_stock_data) {
    Stock_Dict::iterator metric;
    for (metric = single_stock_data.begin() ; metric != single_stock_data.end(); metric++) {
        stocks_data_[ticker][metric->first] = metric->second;
    }
}



// Functions

void TemplateStrategy::update_stock(std::string ticker, TemplateStrategy::Stock_Dict data) {
    // Ingest data
    auto prev_price = std::any_cast<float>(stocks_data_[ticker]["price"]);
    auto prev_trend = std::any_cast<std::string>(stocks_data_[ticker]["trend"]);
    set_stock_data(ticker, data);
    auto curr_price = std::any_cast<float>(stocks_data_[ticker]["price"]);

    // Re-run logic
    if (curr_price > prev_price) {
        if (prev_trend == "downwards") {
            orders_[ticker].push_back("BUY");
            stocks_data_[ticker]["trend"] = "upwards";
        }
    }
    else if (curr_price < prev_price) {
        if (prev_trend == "upwards") {
            orders_[ticker].push_back("SELL");
            stocks_data_[ticker]["trend"] = "downwards";
        }
    }
}

void TemplateStrategy::clear_orders() {
    std::cout << "Clearing" << orders_.size() << "Orders" << "\n";
    orders_.clear();
}

TemplateStrategy::Orders_Dict
TemplateStrategy::update_all(TemplateStrategy::Stocks_Dict new_data) {
    clear_orders();
    ticks_ += 1;

    Stocks_Dict::iterator stock;
    for (stock = new_data.begin(); stock != new_data.end(); stock++) {
        std::string ticker = stock->first;
        Stock_Dict stock_data = stock->second;
        update_stock(ticker, stock_data);
    }

    return orders_;
}