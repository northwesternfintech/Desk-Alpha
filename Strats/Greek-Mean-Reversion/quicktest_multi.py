import Ms_gmr_strat
import random


# Single stock tests
kwargs = {
    "option_strategy": [], 
    "option_type": [],     
    "strikes": [],
    "underlying_price": [],
    "option_price": [],
    "interest_rate": [],
    "dividend_yields": [],              
    "time_to_expiration": [],         
    "implied_volatility": [],      
}

kwargs2 = {
    "option_strategy": [], 
    "option_type": [],     
    "strikes": [],
    "underlying_price": [],
    "option_price": [],
    "interest_rate": [],
    "dividend_yields": [],              
    "time_to_expiration": [],         
    "implied_volatility": [],      
}

kwargs3 = {
    "option_strategy": [], 
    "option_type": [],     
    "strikes": [],
    "underlying_price": [],
    "option_price": [],
    "interest_rate": [],
    "dividend_yields": [],              
    "time_to_expiration": [],         
    "implied_volatility": [],      
}
    
    
test_obj = Ms_gmr_strat.Ms_gmr_strat()

# randomize some values for kwargs
for i in range(50):
    kwargs["option_strategy"].append("long")
    kwargs["option_type"].append("call")
    kwargs["strikes"].append(random.randint(1, 50))
    kwargs["underlying_price"].append(random.randint(50, 150))
    kwargs["option_price"].append(random.randint(1, 50))
    kwargs["interest_rate"].append(random.random())
    kwargs["dividend_yields"].append(random.random())
    kwargs["time_to_expiration"].append(50-i)
    kwargs["implied_volatility"].append(random.random())
    
    kwargs2["option_strategy"].append("short")
    kwargs2["option_type"].append("call")
    kwargs2["strikes"].append(random.randint(50, 150))
    kwargs2["underlying_price"].append(random.randint(1, 60))
    kwargs2["option_price"].append(random.randint(1, 50))
    kwargs2["interest_rate"].append(random.random())
    kwargs2["dividend_yields"].append(random.random())
    kwargs2["time_to_expiration"].append(50-i)
    kwargs2["implied_volatility"].append(random.random())
    
    kwargs3["option_strategy"].append("short")
    kwargs3["option_type"].append("put")
    kwargs3["strikes"].append(random.randint(1, 50))
    kwargs3["underlying_price"].append(random.randint(50, 150))
    kwargs3["option_price"].append(random.randint(1, 50))
    kwargs3["interest_rate"].append(random.random())
    kwargs3["dividend_yields"].append(random.random())
    kwargs3["time_to_expiration"].append(50-i)
    kwargs3["implied_volatility"].append(random.random())
    
kwargs_multi = {"AAPL": kwargs, 
                "MSFT": kwargs2,
                "NVDA": kwargs3}

test_obj.update(**kwargs_multi)
test_obj.plotting_strat("AAPL", "call", "long")
test_obj.plotting_strat("NVDA", "put", "short")

print(test_obj.get_decisions("AAPL" , "call", "long", "gamma"))
print(test_obj.get_decisions("MSFT" , "call", "short", "gamma"))
