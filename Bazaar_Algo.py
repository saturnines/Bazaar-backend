# tuple call is returned by day month year
#from api_call import Item, Search


class Item:
    def __init__(self, maxSell, maxBuy, min_buy, minSell, buy, sell, sellvolume, buyvolume):
        self._maxSell = maxSell
        self._maxBuy = maxBuy
        self._min_buy = min_buy
        self._minSell = minSell
        self._buy = buy
        self._sell = sell
        self._sellvolume = sellvolume
        self._buyvolume = buyvolume

    # Example method to get average sell volume
    def get_avg_sell_volume(self):
        return sum(self._sellvolume) / len(self._sellvolume)

    # Example method to get average buy volume
    def get_avg_buy_volume(self):
        return sum(self._buyvolume) / len(self._buyvolume)

    def get_avg_buy(self):
        return sum(self._buy) / len(self._buy)

    def get_avg_sell(self):
        return sum(self._sell) / len(self._sell)

    def get_avg_minsell(self):
        return sum(self._minSell) / len(self._minSell)

    def get_avg_minbuy(self):
        return sum(self._min_buy) / len(self._min_buy)

    def get_avg_maxbuy(self):
        return sum(self._maxBuy) / len(self._maxBuy)

    def get_avg_maxsell(self):
        return sum(self._maxSell) / len(self._maxSell)


# Dummy data for one day
item_data_day = Item(
    maxSell=[105, 107, 108],
    maxBuy=[95, 97, 99],
    min_buy=[90, 92, 93],
    minSell=[100, 102, 103],
    buy=[96, 98, 100],
    sell=[104, 106, 107],
    sellvolume=[500, 520, 530],
    buyvolume=[480, 495, 510]
)

# Dummy data for one hour (assuming more volatility in shorter time frames)
item_data_hour = Item(
    maxSell=[108, 110, 112],
    maxBuy=[96, 98, 100],
    min_buy=[91, 93, 95],
    minSell=[103, 105, 107],
    buy=[97, 99, 101],
    sell=[107, 109, 111],
    sellvolume=[300, 320, 340],
    buyvolume=[280, 295, 310]
)

# Dummy data for one week (assuming less volatility but noticeable trends)
item_data_week = Item(
    maxSell=[100, 102, 104, 106, 108, 110, 112],
    maxBuy=[90, 92, 94, 96, 98, 100, 102],
    min_buy=[85, 87, 89, 91, 93, 95, 97],
    minSell=[95, 97, 99, 101, 103, 105, 107],
    buy=[91, 93, 95, 97, 99, 101, 103],
    sell=[105, 107, 109, 111, 113, 115, 117],
    sellvolume=[700, 720, 740, 760, 780, 800, 820],
    buyvolume=[680, 695, 710, 725, 740, 755, 770]
)

class TradingAlgo:
    def __init__(self, item_day, item_hour, item_week):
        self.item_day = item_day
        self.item_hour = item_hour
        self.item_week = item_week


    def weighted_sell_volume(self):
        # Calculates the average weighted sell volume.
        day_avg_sell_vol = self.item_day.get_avg_sell_volume()
        hour_avg_sell_vol = self.item_hour.get_avg_sell_volume()
        week_avg_sell_vol = self.item_week.get_avg_sell_volume()

        weighted_sell_vol = (0.4 * day_avg_sell_vol) + (0.3 * hour_avg_sell_vol) + (0.4 * week_avg_sell_vol)
        return weighted_sell_vol

    def weighted_buy_volume(self):
        # Calculates the average weighted buy volume.
        day_avg_sell_vol = self.item_day.get_avg_sell_volume()
        hour_avg_sell_vol = self.item_hour.get_avg_sell_volume()
        week_avg_sell_vol = self.item_week.get_avg_sell_volume()

        weighted_buy_vol = (0.4 * day_avg_sell_vol) + (0.3 * hour_avg_sell_vol) + (0.3 * week_avg_sell_vol)
        return weighted_buy_vol

    def weighted_buy(self):
        """Calculates weighted buy not volume"""
        day_avg_buy = self.item_day.get_avg_buy()
        hour_avg_buy = self.item_hour.get_avg_buy()
        week_avg_buy = self.item_week.get_avg_buy()
        weighted_buy_vol = (0.5 * day_avg_buy) + (0.3 * hour_avg_buy) + (0.2 * week_avg_buy)
        return weighted_buy_vol

    def weighted_sell(self):
        """Calulates weighted sell not volume"""
        week_avg_sell = self.item_week.get_avg_sell()
        hour_avg_sell = self.item_hour.get_avg_sell()
        daily_avg_sell = self.item_day.get_avg_sell()
        weighted_sell_vol = (0.4 * week_avg_sell) + (0.3 * hour_avg_sell) + (0.3 * daily_avg_sell)

        return weighted_sell_vol

    def weighted_min_buy(self):
        """Calculates current minimum weighted buy"""
        day_min_buy = self.item_day.get_avg_minbuy()
        hour_min_buy = self.item_hour.get_avg_minbuy()
        week_min_buy = self.item_week.get_avg_minbuy()

        # Calculate the weighted minimum buy price
        weighted_min_buy_price = (0.6 * day_min_buy) + (0.3 * hour_min_buy) + (0.1 * week_min_buy)

        return weighted_min_buy_price

    def weighted_min_sell(self):
        """Calculates current minium weighted sell"""
        day_min_sell = self.item_day.get_avg_minsell()
        hour_min_sell = self.item_hour.get_avg_minsell()
        week_min_sell = self.item_week.get_avg_minsell()

        # Calculate the weighted minimum sell price
        weighted_min_sell_price = (0.6 * day_min_sell) + (0.3 * hour_min_sell) + (0.1 * week_min_sell)

        return weighted_min_sell_price


    def weighted_max_buy(self):
        """Calculates current maximum weighted buy"""
        day_max_buy = self.item_day.get_avg_maxbuy()
        hour_max_buy = self.item_hour.get_avg_maxbuy()
        week_max_buy = self.item_week.get_avg_maxbuy()

        # Calculate the weighted maximum buy price
        weighted_max_buy_price = (0.6 * day_max_buy) + (0.3 * hour_max_buy) + (0.1 * week_max_buy)

        return weighted_max_buy_price

    def weighted_max_sell(self):
        """Calculates current maximum weighted sell"""
        day_max_sell = self.item_day.get_avg_maxsell()
        hour_max_sell = self.item_hour.get_avg_maxsell()
        week_max_sell = self.item_week.get_avg_maxsell()

        # Calculate the weighted maximum sell price
        weighted_max_sell_price = (0.6 * day_max_sell) + (0.3 * hour_max_sell) + (0.1 * week_max_sell)

        return weighted_max_sell_price


# Assuming your dummy data instances are created as before...
trading_algo = TradingAlgo(item_data_day, item_data_hour, item_data_week)

# Now you can call the method to analyze the market based on the data
print(trading_algo.weighted_min_sell())
print(trading_algo.weighted_min_buy())
print(trading_algo.weighted_sell())
print(trading_algo.weighted_buy())
print(trading_algo.weighted_max_buy())
print(trading_algo.weighted_max_sell())



