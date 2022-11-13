#include "multitemplate.hxx"
#include <iostream>

// Path: Strats/Template/Jerry-Template/multitemplate.cxx

TemplateStrategy::TemplateStrategy(unordered_map<string, unordered_map<string, string> > initDict)
: data(initDict)
{
    time = 0;
    ticks = 0;
    orders = unordered_map<string, string>();
    for (auto const& [ticker, metric_value_pair] : data){
        std::cout << "Ticker: " << ticker;
        //ticker['trend'] = "Upward";
    }
    
}

void TemplateStrategy::update_stock(string ticker, unordered_map<string, string> data)
{
    double prev_price = stod(this->data[ticker]["price"]);
    string prev_trend = this->data[ticker]["trend"];
    set_data_for_stock(ticker, data);
    double next_price = stod(data["price"]);
}
