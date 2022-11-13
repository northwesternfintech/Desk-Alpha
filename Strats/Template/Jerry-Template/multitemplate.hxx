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
    TemplateStrategy();

    //Getters
    map<string, string> get_orders();
    map<string, map<string, string> > get_data();
    size_t get_ticks();
    time_t get_time();
    map<string, string> get_data_for_stock(string ticker);


    //Setters
    void set_data(map<string, map<string, string> >);
    void set_orders(map<string, string>);
    void set_ticks(size_t);
    void set_time(time_t);
    void set_data_for_stock(string ticker, map<string, string> data);

    //Methods
    void update_stock(string ticker, map<string, string> data);
    void clear_orders();
    map<string, string> update();
};