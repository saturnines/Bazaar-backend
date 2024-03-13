# tuple call is returned by day month year
from api_call import Item, Search
import statistics


class ValidationError(Exception):
    pass


import statistics


class TradingItemAlgo:
    def __init__(self, maxSell, maxBuy, min_buy, minSell, buy, sell, sellvolume, buyvolume):
        # Initialize with data fields from Item
        self._maxSell = maxSell
        self._maxBuy = maxBuy
        self._min_buy = min_buy
        self._minSell = minSell
        self._buy = buy
        self._sell = sell
        self._sellvolume = sellvolume
        self._buyvolume = buyvolume

    def flatten_and_check(self, data):
        """Flatten data if it's a list of lists and ensure it's not empty."""
        if not isinstance(data, list) or all(not isinstance(sub, list) for sub in data):
            data = [data]
        flat_list = [item for sublist in data for item in sublist if item is not None and sublist]
        return flat_list if flat_list else [1]

    def get_avg(self, data):
        flat_list = self.flatten_and_check(data)
        return sum(flat_list) / len(flat_list) if flat_list else 0

    def get_median(self, data):
        if data:
            return statistics.median(data)
        else:
            raise ValueError("Data not found.")

    # Methods directly ported from Item
    def get_avg_sell_volume(self):
        return self.get_avg(self._sellvolume)

    def get_avg_buy_volume(self):
        return self.get_avg(self._buyvolume)

    def get_avg_buy(self):
        return self.get_avg(self._buy)

    def get_avg_sell(self):
        return self.get_avg(self._sell)

    def get_avg_minsell(self):
        return self.get_avg(self._minSell)

    def get_avg_minbuy(self):
        return self.get_avg(self._min_buy)

    def get_avg_maxbuy(self):
        return self.get_avg(self._maxBuy)

    def get_avg_maxsell(self):
        return self.get_avg(self._maxSell)

    def get_buy_med(self):
        return self.get_median(self._buy)

    def get_sell_med(self):
        return self.get_median(self._sell)

    def weighted_volume(self, volume_type):
        if volume_type == "sell":
            return (0.35 * self.get_avg_sell_volume()) + (0.45 * self.get_avg_sell_volume()) + (
                        0.2 * self.get_avg_sell_volume())
        elif volume_type == "buy":
            return (0.35 * self.get_avg_buy_volume()) + (0.45 * self.get_avg_buy_volume()) + (
                        0.2 * self.get_avg_buy_volume())
        else:
            raise ValueError("Invalid volume type specified.")

    def weighted_price(self, price_type):
        if price_type in ["buy", "sell", "min_buy", "min_sell", "max_buy", "max_sell"]:
            method_map = {
                "buy": self.get_avg_buy,
                "sell": self.get_avg_sell,
                "min_buy": self.get_avg_minbuy,
                "min_sell": self.get_avg_minsell,
                "max_buy": self.get_avg_maxbuy,
                "max_sell": self.get_avg_maxsell,
            }
            avg_price = method_map[price_type]()
            return (0.3 * avg_price) + (0.5 * avg_price) + (0.2 * avg_price)
        else:
            raise ValueError("Invalid price type specified.")

    def main_algo(self):
        buy_signal_points = 0


        buy_signal = self.weighted_volume("buy") - self.weighted_volume("sell")
        return buy_signal






# Need to do main algo to return a boolean
# main algo could return a tuple -> use tuple to spit out useful data


# debugging
x = Search()

to_parse = x.search_item("Booster Cookie")
item_day = to_parse[0]
item_hour = to_parse[1]
item_week = to_parse[2]

# Initialize your TradingAlgo
trading_algo = TradingItemAlgo(item_day.get_max_sell(), item_day.get_max_buy(), item_day.get_min_buy(), item_day.get_min_sell(), item_day.get_buy(), item_day.get_sell(), item_day.get_sell_vol(), item_day.get_buy_vol())

print(trading_algo.main_algo())