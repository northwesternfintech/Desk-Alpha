


#include <iostream>;
#include string;

class MultiStock{
  """
  A base strategy that is used to explain how to properly develop a strategy.
  """

  std::unordered_map data = std::unordered_map<std::string, std::unordered_map<std::string, std::string>>();
  std::unordered_map orders = std::unordered_map<std::string, std::vector<std::string>>();
  std::unordered_map trends = std::unordered_map<std::string, std::vector<std::string>>();
  

  int ticks = 0;
  
  MultiStock(std::unordered_map<std::string, std::unordered_map<std::string, std::string>> stock_data){
    """
    Metrics - the actual information you need to track. If this is a specific algorithm, you can hard-code it and remove that argument.
    Initvalues - the initial values of your arguments. 
    """

    
    for (auto [ticker, s_data] : stock_data){
        this.data[ticker] = s_data;
        this.trends[ticker] = "Upwards";
        this.orders[ticker] = std::vector<std::string>();

    }
  }
   
    
    
  
  
  std::unordered_map getData(){
    return this.data;
  }

  std::unordered_map get_data_ticker(std::stringticker){
    return this.data[ticker];
  }

 
  std::vector<std::string>> get_orders(std::string ticker){
    return this.orders[ticker];

  }


  int get_ticks(){
    return this.ticks;
  }

  std::vector<std::string>> get_trend(std::string ticker){
    return this.trend[ticker];
  }

  void set_trend(std::string ticker, std::string newTrend){
    this.trend[ticker] = newTrend;
  }
  
  
void clear_order(ticker){
    """
    Clears all current orders and logs relevant information.
   """
    this.orders[ticker] = std::vector<std::string>;
    
}

void update_stock(self, data, ticker):
    """
    Will be called on every tick to update the algorithm state and output buys/sells.
    @type data: dict
    @rtype: list
    """
    this.ticks += 1;
    double previousPrice = std::stof(self.data[ticker]['price']);


    std::unordered_map updates = std::unordered_map<std::string, std::unordered_map<std::string, std::string>>;
    for (auto [ticker, data] : this.data){
        updates[ticker] = data;

    }

    for([metric, information] : updates){
      this.data[metric] = information
    }
      
    this.clear_orders()



    
        
    if (this.data[ticker]['price'] > previousPrice): 
        if (this.get_trend() == "Downward"):  
            this.orders.append('BUY') 
        this.set_trend("Upward") 

    else if (this.data[ticker]['price'] < previousPrice){ 
            this.orders.append('SELL') 
        }
        this.set_trend("Downward") 
    #More example logic
    return this.orders

void update(this, data){
    for (ticker : this.data){
        update_stock(data[ticker], ticker)
    }
    return self.orders
}


}