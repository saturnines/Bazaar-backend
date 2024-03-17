from api_call import Item, Search
import statistics


class ValidationError(Exception):
    pass


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

    def flatten_and_check(self, data):
        """Ensure data is a list of lists, flatten it, and handle non-iterable items correctly."""
        # Ensure data is in a list
        if not isinstance(data, list):
            data = [data]

        flat_list = []
        for item in data:
            # If the item is a list, extend flat_list by iterating over its elements
            if isinstance(item, list):
                flat_list.extend([subitem for subitem in item if subitem is not None])
            # For non-list items (including non-iterables like float, int), append directly to flat_list
            else:
                if item is not None:
                    flat_list.append(item)

        # Return [1] if flat_list is empty, ensuring there's always something to calculate with
        return flat_list if flat_list else [1]

    # Example method to get average sell volume
    def get_avg_sell_volume(self):
        flat_list = self.flatten_and_check(self._sellvolume)
        return sum(flat_list) / len(flat_list)

    def get_avg_buy_volume(self):
        flat_list = self.flatten_and_check(self._buyvolume)
        return sum(flat_list) / len(flat_list)

    def get_sell(self):
        return self._sell

    def get_avg_buy(self):
        flat_list = self.flatten_and_check(self._buy)
        return sum(flat_list) / len(flat_list)

    def get_avg_sell(self):
        flat_list = self.flatten_and_check(self._sell)
        return sum(flat_list) / len(flat_list)

    def get_avg_minsell(self):
        flat_list = self.flatten_and_check(self._minSell)
        return sum(flat_list) / len(flat_list)

    def get_avg_minbuy(self):
        flat_list = self.flatten_and_check(self._min_buy)
        return sum(flat_list) / len(flat_list)

    def get_avg_maxbuy(self):
        flat_list = self.flatten_and_check(self._maxBuy)
        return sum(flat_list) / len(flat_list)

    def get_avg_maxsell(self):
        flat_list = self.flatten_and_check(self._maxSell)
        return sum(flat_list) / len(flat_list)

    def get_buy_med(self):
        if self._buy:
            return statistics.median(self._buy)
        else:
            raise ValidationError("self._buy not found.")

    def get_sell_med(
            self):  # note buy and sell may not work bc not sure if it works on objects can just do a  long way medium
        if self._sell:
            return statistics.median(self._sell)
        else:
            raise ValidationError("Self._sell not found")


class TradingAlgo:
    def __init__(self, item_day, item_hour, item_week):
        self.item_day = item_day
        self.item_hour = item_hour
        self.item_week = item_week

    def get_liquid_sell(self):
        return self.item_day.get_avg_sell()

    def possible_profit_comprehensive(self):
        # Calculate the average trading cost based on recent hourly data
        immediate_trade_cost = (self.item_hour.get_avg_buy() + self.item_hour.get_avg_sell()) / 2

        # Incorporate daily data to get a sense of short to medium-term market trends
        daily_trade_value = (self.item_day.get_avg_buy() + self.item_day.get_avg_sell()) / 2

        # Use weekly data for a longer-term market perspective
        expected_future_trade_value = (self.item_week.get_avg_buy() + self.item_week.get_avg_sell()) / 2

        # Calculate potential profit, factoring in immediate, daily, and weekly data
        # The method weights these differently, assuming that more recent data might be more relevant
        # Adjust the weights according to your trading strategy and risk tolerance
        weighted_trade_value = (immediate_trade_cost * 0.4) + (daily_trade_value * 0.3) + (
                expected_future_trade_value * 0.3)
        profit = expected_future_trade_value - weighted_trade_value
        return profit

    def medium_sell_week(self):
        return self.item_week.get_sell_med()

    def medium_buy_week(self):
        return self.item_week.get_buy_med()

    def weighted_sell_volume(self):
        # Calculates the average weighted sell volume.
        day_avg_sell_vol = self.item_day.get_avg_sell_volume()
        hour_avg_sell_vol = self.item_hour.get_avg_sell_volume()
        week_avg_sell_vol = self.item_week.get_avg_sell_volume()

        weighted_sell_vol = (0.35 * day_avg_sell_vol) + (0.45 * hour_avg_sell_vol) + (0.2 * week_avg_sell_vol)
        return weighted_sell_vol

    def weighted_buy_volume(self):
        # Calculates the average weighted buy volume.
        day_avg_sell_vol = self.item_day.get_avg_sell_volume()
        hour_avg_sell_vol = self.item_hour.get_avg_sell_volume()
        week_avg_sell_vol = self.item_week.get_avg_sell_volume()

        weighted_buy_vol = (0.35 * day_avg_sell_vol) + (0.45 * hour_avg_sell_vol) + (0.2 * week_avg_sell_vol)
        return weighted_buy_vol

    def weighted_buy(self):
        """Calculates weighted buy not volume"""
        day_avg_buy = self.item_day.get_avg_buy()
        hour_avg_buy = self.item_hour.get_avg_buy()
        week_avg_buy = self.item_week.get_avg_buy()
        weighted_buy_vol = (0.3 * day_avg_buy) + (0.5 * hour_avg_buy) + (0.2 * week_avg_buy)
        return weighted_buy_vol

    def weighted_sell(self):
        """Calulates weighted sell not volume"""
        week_avg_sell = self.item_week.get_avg_sell()
        hour_avg_sell = self.item_hour.get_avg_sell()
        daily_avg_sell = self.item_day.get_avg_sell()
        weighted_sell_vol = (0.3 * daily_avg_sell) + (0.5 * hour_avg_sell) + (0.2 * week_avg_sell)

        return weighted_sell_vol

    def weighted_min_buy(self):
        """Calculates current minimum weighted buy"""
        day_min_buy = self.item_day.get_avg_minbuy()
        hour_min_buy = self.item_hour.get_avg_minbuy()
        week_min_buy = self.item_week.get_avg_minbuy()

        # Calculate the weighted minimum buy price
        weighted_min_buy_price = (0.3 * day_min_buy) + (0.5 * hour_min_buy) + (0.2 * week_min_buy)

        return weighted_min_buy_price

    def weighted_min_sell(self):
        """Calculates current minium weighted sell"""
        day_min_sell = self.item_day.get_avg_minsell()
        hour_min_sell = self.item_hour.get_avg_minsell()
        week_min_sell = self.item_week.get_avg_minsell()

        # Calculate the weighted minimum sell price
        weighted_min_sell_price = (0.3 * day_min_sell) + (0.5 * hour_min_sell) + (0.2 * week_min_sell)

        return weighted_min_sell_price

    def weighted_max_buy(self):
        """Calculates current maximum weighted buy"""
        day_max_buy = self.item_day.get_avg_maxbuy()
        hour_max_buy = self.item_hour.get_avg_maxbuy()
        week_max_buy = self.item_week.get_avg_maxbuy()

        # Calculate the weighted maximum buy price
        weighted_max_buy_price = (0.3 * day_max_buy) + (0.5 * hour_max_buy) + (0.2 * week_max_buy)

        return weighted_max_buy_price

    def weighted_max_sell(self):
        """Calculates current maximum weighted sell"""
        day_max_sell = self.item_day.get_avg_maxsell()
        hour_max_sell = self.item_hour.get_avg_maxsell()
        week_max_sell = self.item_week.get_avg_maxsell()

        # Calculate the weighted maximum sell price
        weighted_max_sell_price = (0.3 * day_max_sell) + (0.5 * hour_max_sell) + (0.2 * week_max_sell)

        return weighted_max_sell_price


class Main:
    def __init__(self):
        self.search_function = Search()  # Use this instance for searching

    def metrics(self, search):
        """Determines if it's worth buying or not. Acts like main()."""
        item_result = self.search_function.search_item(search)  # Use the instance variable

        if not item_result:
            print("Item not found!")
            return False
        # This part handles the search, now we have a tuple.

        # Set up Trading Algo and the 3 items:
        item_day = Item(item_result[0].get_max_sell(), item_result[0].get_max_buy(), item_result[0].get_min_buy(),
                        item_result[0].get_min_sell(), item_result[0].get_buy(), item_result[0].get_sell(),
                        item_result[0].get_sell_vol(), item_result[0].get_buy_vol())
        item_hour = Item(item_result[1].get_max_sell(), item_result[1].get_max_buy(), item_result[1].get_min_buy(),
                         item_result[1].get_min_sell(), item_result[1].get_buy(), item_result[1].get_sell(),
                         item_result[1].get_sell_vol(), item_result[1].get_buy_vol())
        item_week = Item(item_result[2].get_max_sell(), item_result[2].get_max_buy(), item_result[2].get_min_buy(),
                         item_result[2].get_min_sell(), item_result[2].get_buy(), item_result[2].get_sell(),
                         item_result[2].get_sell_vol(), item_result[2].get_buy_vol())

        # This is the item with access to the different methods
        searched_item = TradingAlgo(item_day, item_hour, item_week)

        # profitability indicator
        profitability = ((
                                 searched_item.weighted_sell() - searched_item.weighted_buy()) / searched_item.weighted_buy()) * 100

        # market volatility indicator
        volatility = ((
                              searched_item.weighted_max_sell() - searched_item.weighted_max_buy()) / searched_item.weighted_min_buy()) * 100

        # Liquidity Indicator
        liquid = (searched_item.weighted_buy() + searched_item.weighted_sell()) / 2

        # price momentum (weekly)
        current_price = (searched_item.weighted_sell() + searched_item.weighted_buy()) / 2
        previous_price = item_week.get_sell_med()
        momentum = (current_price - previous_price) / previous_price

        # relative_volume
        current_volume = (searched_item.weighted_buy_volume() + searched_item.weighted_sell_volume()) / 2
        average_volume = item_week.get_sell_med()
        relative_volume = current_volume / average_volume

        # Spread Analysis
        spread = searched_item.weighted_sell() - searched_item.weighted_buy()

        # Price Stability Indicator
        weekly_avg_price = (searched_item.weighted_min_sell() + searched_item.weighted_max_sell()) / 2
        current_price_stability = (current_price - weekly_avg_price) / weekly_avg_price * 100

        # Historical buy Comparison
        historical_buy_comparison = (
                                            searched_item.weighted_buy() - searched_item.medium_buy_week()) / searched_item.medium_buy_week() * 100

        # Historical sell Comparison
        historical_sell_comparison = (
                                             searched_item.weighted_sell() - searched_item.medium_sell_week()) / searched_item.medium_sell_week() * 100

        # Medium sell
        medium_sell = searched_item.medium_sell_week()

        # medium buy
        medium_buy = searched_item.medium_buy_week()

        # Possible Profit
        possible_profit = searched_item.possible_profit_comprehensive()

        # current - instant sell:
        instant_sell = searched_item.get_liquid_sell()

        # Compile all metrics into a dictionary
        metrics = {
            "profitability": profitability,
            "volatility": volatility,
            "liquidity": liquid,
            "price_momentum": momentum,
            "relative_volume": relative_volume,
            "spread": spread,
            "price_stability": current_price_stability,
            "historical_buy_comparison": historical_buy_comparison,
            "historical_sell_comparison": historical_sell_comparison,
            "medium_sell": medium_sell,
            "medium_buy": medium_buy,
            "possible_profit": possible_profit,
            "current_price": current_price,
            "instant_sell": instant_sell,
        }

        return metrics

    def main_algo(self, search):
        metrics = self.metrics(search)

        if not metrics:
            raise ValidationError("Item not Found")

        print(metrics["profitability"])


x = Main()
print(x.main_algo("Nurse Shark Tooth"))