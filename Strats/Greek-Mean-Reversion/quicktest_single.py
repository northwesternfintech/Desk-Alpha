import Ss_gmr_strat
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
    
    
test_obj = Ss_gmr_strat.Ss_gmr_strat()

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
    
gamma_decisions, vega_decisions = test_obj.update(**kwargs)
