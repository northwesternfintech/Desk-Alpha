#include <unordered_map>
#include <ctime>
#include <string>

using namespace std;

class TemplateStrategy
{
    private:
    unordered_map<string, unordered_map<string, string> > data;
    time_t time;
    unordered_map<string, string> orders;
    size_t ticks;

    public:
    //Constructors
    TemplateStrategy(unordered_map<string, unordered_map<string, string> > initDict);

    //Getters
    unordered_map<string, string> get_orders() { return orders; }
    unordered_map<string, unordered_map<string, string> > get_data() { return data; }
    size_t get_ticks() { return ticks; }
    time_t get_time() { return time; }
    unordered_map<string, string> get_data_for_stock(string ticker) { return data[ticker]; }


    //Setters
    void set_data(unordered_map<string, unordered_map<string, string> > data) { this->data = data; }
    void set_orders(unordered_map<string, string> orders) { this->orders = orders; }
    void set_ticks(size_t ticks) { this->ticks = ticks; }
    void set_time(time_t time) { this->time = time; }
    void set_data_for_stock(string ticker, unordered_map<string, string> data) { this->data[ticker] = data; }

    //Methods
    void update_stock(string ticker, unordered_map<string, string> data);
    void clear_orders();
    unordered_map<string, string> update(unordered_map<string,string> data);
};