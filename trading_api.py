from fastapi import FastAPI, HTTPException
from Bazaar_Algo import Main
from pydantic import BaseModel
from dyn_search_arr import DynSearchList
from typing import List
from fastapi.middleware.cors import CORSMiddleware

# Caching Imports Below:
from redis.asyncio import Redis

app = FastAPI()

# CORS handling.
origins = [  # Used this to test if the apis work within the frontend
    "http://127.0.0.1:6379",  # Allow Reddis
    "http://localhost:8000",  # Allow local development server
    "http://127.0.0.1:5500",  # Allow Frontends
    "http://127.0.0.1:51242",
    "http://172.17.0.1:53332/"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InvalidSearch(Exception):
    """Raised if we search something invalid"""
    pass


class Metrics(BaseModel):  # data validation
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


class InvestmentSignal(BaseModel):  # data validation for the investment singal
    Signal: str
    metrics: Metrics


@app.get("/items/", response_model=InvestmentSignal)
async def get_item_metrics(search_term: str):
    if not search_term:  # Raise exception that search term is not there. (This should never happen)
        raise HTTPException(status_code=400, detail="Search term is required.")
    search = Main()  # Init API and search function

    client = Redis.from_url("redis://redis")  # Open Redis pool
    try:
        print(f"Connection Pool Open! {await client.ping()}")

        cache = await client.get(search_term)  # Wait search term result
        if cache:
            print("Cache exists") # If there is a cache we return the cache result
            return InvestmentSignal.parse_raw(cache)
        else:
            print("Cache Miss")
            returned_dict = search.main_algo(search_term)  # If no cache, search the item result which calls the API
            if not returned_dict:
                raise HTTPException(status_code=404, detail="Item not found...")

            metrics_inst = Metrics(**returned_dict['metrics']) #Debugging if way more users, this returns the full result of the backend
            investment_signal = InvestmentSignal(Signal=returned_dict["Signal"], metrics=metrics_inst) #Set investment signal as the api result
            await client.set(search_term, investment_signal.json(), ex=3600) #Add to the redis, will be removed in 1 hour
            return investment_signal # Return the result
    except InvalidSearch:
        raise HTTPException(status_code=404, detail="Item not found...")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.aclose() #close the redis instance.


class PossibleItem(BaseModel): #(I think this one is unnecessary.) but still good practice.
    all_items: List[str]


@app.get("/dyn_search_list")
async def dyn_search_list():
    """API call for frontend use to get a list of searchable items"""
    try:
        dyn_items = DynSearchList()
        searchable_list_inst = dyn_items.get_item()
        to_return = PossibleItem(all_items=searchable_list_inst)
        return to_return
    except InvalidSearch:
        raise HTTPException(status_code=405, detail='List not found!')


# Note if you want to run the redis server use "
# "
# This is a quick run command for debugging purposes
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
