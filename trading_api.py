import json

from fastapi import FastAPI,HTTPException
from Bazaar_Algo import Main
from pydantic import BaseModel
from dyn_search_arr import DynSearchList
app = FastAPI()

class InvalidSearch(Exception):
    """Raised if we search something invalid"""
    pass



class Metrics(BaseModel): #data validation
    profitability: float
    volatility: float
    liquidity: float
    price_momentum: float
    relative_volume: float
    spread: float
    price_stability: float
    historical_buy_comparison: float
    historical_sell_comparison: float
    medium_sell: float
    medium_buy: float
    possible_profit: float
    current_price: float
    instant_sell: float

class InvestmentSignal(BaseModel):
    Signal: str
    metrics: Metrics

class possible_item(BaseModel):
    all_items: list

@app.get("/items/", response_model=InvestmentSignal) # may need to change the address when i build frontend.
async def get_item_metrics(search_term: str):
    if not search_term:
        raise HTTPException(status_code=400, detail="Search term is required.")

    search = Main()
    try:
        returned_dict = search.main_algo(search_term)
        if not returned_dict:  # Handle case when main_algo returns False
            raise HTTPException(status_code=404, detail="Item not found...")

        metrics_inst = Metrics(**returned_dict['metrics'])
        investment_signal = InvestmentSignal(Signal=returned_dict["Signal"], metrics=metrics_inst)
        return investment_signal

    except InvalidSearch:
        raise HTTPException(status_code=404, detail="Item not found...")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dyn_search_list/", response_model=possible_item)
async def dyn_search_list():
    """API call for frontend use to get a list of searchable items"""
    try:
        dyn_items = DynSearchList()
        searchable_list = dyn_items.get_item()
        return searchable_list
    except InvalidSearch:
        raise HTTPException(status_code=405, detail='List not found!')


"""
_
TODO:
Implement Caching
Finish Frontend
Implement ALL bazaar items to item_list.py"""

# This is a quick run command for debugging purposes
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)