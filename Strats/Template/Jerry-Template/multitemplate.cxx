#include "multitemplate.hxx"
#include <iostream>

// Path: Strats/Template/Jerry-Template/multitemplate.cxx

TemplateStrategy::TemplateStrategy(unordered_map<string, unordered_map<string, string> > initDict)
: data(initDict)
{
    time = 0;
    ticks = 0;
    orders = unordered_map<string, string>();
    for (auto & [ticker, value] : data){
        data[ticker].at("trend") = "Upward";
    }
    
}

void TemplateStrategy::update_stock(string ticker, unordered_map<string, string> data)
{
    double prev_price = stod(this->data[ticker]["price"]);
    string prev_trend = this->data[ticker]["trend"];
    set_data_for_stock(ticker, data);
    double next_price = stod(data["price"]);

    if(next_price > prev_price){
        if(prev_trend == "Downward"){
            orders[ticker] = "BUY";
        }
        this->data[ticker]["trend"] = "Upward";
    }

    else if(next_price < prev_price){
        if(prev_trend == "Upward"){
            orders[ticker] = "SELL";
        }
        this->data[ticker]["trend"] = "Downward";
    }

    else{
        orders[ticker] = "HOLD";
    }
}

void TemplateStrategy::clear_orders(){
    orders = unordered_map<string, string>();
}

unordered_map<string, string> TemplateStrategy::update(unordered_map<string,string> data){
    ticks += 1;
    clear_orders();
    for (auto & [ticker, value] : data){
        update_stock(ticker, data);
    }
}
