#include "MultiStockTemplate.h"
#include <iostream>

MultiStockTemplate::MultiStockTemplate(unordered_map<string, unordered_map<string, string> > initDict) {

    this->time = 0;
    this->ticks = 0;
    this->orders = {};
    this->data = initDict;

    for (auto& [stock, value]: data) {
            this->data[stock]["trend"] = "Down";
     }


}


void MultiStockTemplate::update_stock(string ticker, unordered_map<string, string> newData) {
    // Updates information for one stock given new data and adds the necessary order for that stock to the orders dict
    // ticker - the stock ticker (string)
    // newData - a dictionary of the current data for the stock (dictionary)

    // # Update the orders for the stock
    double previous_price = stod(this->data[ticker]["price"]);
    this->set_stock_data(ticker, newData);


    double new_price = stod(newData["price"]);
    string current_trend = this->data[ticker]["trend"];


    bool price_updated = false;


    if (new_price > previous_price) { // if price of this stock goes up...
        if (current_trend == "Down") { // and the trend is down, update the trend to up
            this->orders[ticker]= "BUY"; // set the order to buy
            price_updated = true;
        }
          this->data[ticker]["trend"] = "Up"; // set new trend to upward
    }


    else if (new_price < previous_price) { // if price of this stock goes down...
        if (current_trend == "Up") { // and the trend is up, update the trend to down
            this->orders[ticker] = "SELL"; // set the order to sell
            price_updated = true;
        }
        this->data[ticker]["trend"] = "Down"; // set new trend to downward
    }

    if (!price_updated) {
        this->orders[ticker] = ""; // if we are not buying or selling, set order for stock to empty string
    }
}

unordered_map<string, string> MultiStockTemplate::update(unordered_map<string, unordered_map<string, string> > newStockDataAll) {

    this->clear_orders();
    this->ticks += 1;

    for (auto& [stock, new_stock_data]: newStockDataAll) {
        this->update_stock(stock, new_stock_data);
    }

    return this->get_orders(); // orders for the stocks are returned in the the dictionary with the key being stock ticker and value being buy/sell/stay

}



