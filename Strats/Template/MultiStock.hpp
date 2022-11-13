class MultiStock {

    private:

    std::unordered_map data = unordered_map<std::string, std::string>();
    std::unordered_map orders = unordered_map<std::string, std::string>();
    std::unordered_map trends = unordered_map<std::string, std::string>();

    int ticks = 0;

    public:

    MultiStock(unordered_map<string, unordered_map<string, string> > initData);
    double getData(std::string ticker);
    std::vector<std::string> getOrders(std::string ticker);
    int getTicks();
    std::string getTrend(std::string ticker);
    void setTrend(std::string ticker, std::string trend);

    void clear_orders(std::string ticker);
    void updateAll();
    void update(std::string ticker, auto info);
}
