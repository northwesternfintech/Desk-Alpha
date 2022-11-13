#include <iostream>

class MultiStock{
    private:

    std::unordered_map data = unordered_map<std::string, std::string>();
    std::unordered_map orders = unordered_map<std::string, std::string>();
    std::unordered_map trends = unordered_map<std::string, std::string>();

    int ticks = 0;
    
    public:

    MultiStock(unordered_map<string, unordered_map<string, string> > initData) {
        for (auto & [ ticker, value ] : initData) {
            this.data[ticker] = value;
            this.orders[ticker] = std::vector<std::string>;
            this.trends[ticker] = "UP";
        }

    }

     double getData(std::string ticker) {
        return this.data[ticker];
     }
     std::vector<std::string> getOrders(std::string ticker) {
        return this.orders[ticker];
     }
     int getTicks() {
        return this.ticks;
     }
     std::string getTrend(std::string ticker) {
        return this.trends[ticker];
     }
     void setTrend(std::string ticker, std::string trend) {
        this.trends[ticker] = trend;
     }


     void clear_orders(std::string ticker) {
        this.orders[ticker].clear();
     }
     void updateAll() {
        this.ticks++;
        for (auto & [ ticker, value ] : this.data) {
            this.update(ticker, value);

        }

    void update(std::string ticker, auto info) {
        prevPrice = info['price'];

        for (auto & [ metric, update ] : info) {
            this.data[ticker][metric] = update;
        }

        newPrice = info['price']
        
        if (newPrice > prevPrice) {
            if (this.trends[ticker] == "DOWN") {
                this.orders[ticker].push_back("BUY");
            }
        this.setTrend(ticker, "UP");
        } elif (newPrice < prevPrice) {
            if (this.trends[ticker] == "UP") {
                this.orders[ticker].push_back("SELL");
            }
        this.setTrend(ticker, "DOWN");
     }






}
