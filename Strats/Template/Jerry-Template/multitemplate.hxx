#include <map>
#include <ctime>
#include <string>

using namespace std;

class TemplateStrategy
{
    private:
    map<string, map<string, string> > data;
    time_t time;
    map<string, string> orders;
    size_t ticks;

    public:
    //Constructors
    TemplateStrategy(map<string, map<string, string>> initDict);

    //Getters
    map<string, string> get_orders() { return orders; }
    map<string, map<string, string> > get_data() { return data; }
    size_t get_ticks() { return ticks; }
    time_t get_time() { return time; }
    map<string, string> get_data_for_stock(string ticker) { return data[ticker]; }


    //Setters
    void set_data(map<string, map<string, string> > data) { this->data = data; }
    void set_orders(map<string, string> orders) { this->orders = orders; }
    void set_ticks(size_t ticks) { this->ticks = ticks; }
    void set_time(time_t time) { this->time = time; }
    void set_data_for_stock(string ticker, map<string, string> data) { this->data[ticker] = data; }

    //Methods
    void update_stock(string ticker, map<string, string> data);
    void clear_orders();
    map<string, string> update();
};