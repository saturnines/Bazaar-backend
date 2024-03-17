import json

from fastapi import FastAPI,HTTPException
from Bazaar_Algo import Main
from pydantic import BaseModel
app = FastAPI()

class InvalidSearch(Exception):
    """Raised if we search something invalid"""
    pass



class Metrics(BaseModel):
    profitability: float
    volatility: float
    liquidity: float
    price_momentum: float
    relative_volume: float
    spread: float
    price_stability: float
    historical_buy_comparison: float
    historical_sell_comparison: float
    risk_reward_ratio: float
    volatility_index: float
    possible_profit: float
    current_price: float
    instant_sell: float


@app.get("/items/", response_model=Metrics)
async def get_item_metrics(search_term: str):
    if not search_term:
        raise HTTPException(status_code=400, detail="Search term is required.")

    search = Main()
    try:
        dict_result = search.main_algo(search_term)
        return Metrics(**dict_result) #unpack the dict from Bazaar_algo.py
    except InvalidSearch:
        raise HTTPException(status_code=404, detail="Item not found (This shouldn't happen because frontend is a dynamic search with only safe values)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






# This is a quick run command for debugging purposes
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)