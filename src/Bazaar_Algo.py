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
        """Ensure data is a list of numeric values, flatten it, and handle non-numeric items correctly."""
        if not isinstance(data, list):
            data = [data]

        flat_list = []
        for item in data:
            if isinstance(item, list):
                flat_list.extend([self.to_float(subitem) for subitem in item if subitem is not None])
            else:
                if item is not None:
                    flat_list.append(self.to_float(item))

        return flat_list if flat_list else [1.0]

    def to_float(self, value):
        """Convert value to float, returning 0.0 if conversion fails."""
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def safe_average(self, data):
        """Safely calculate the average of a list of numbers."""
        flat_list = self.flatten_and_check(data)
        return sum(flat_list) / len(flat_list) if flat_list else 0.0

    def get_avg_sell_volume(self):
        """Get Average Sell Volume"""
        return self.safe_average(self._sellvolume)

    def get_avg_buy_volume(self):
        """Get Average Buy Volume"""
        return self.safe_average(self._buyvolume)

    def get_sell(self):
        """Get current sell value"""
        return self.to_float(self._sell)

    def get_avg_buy(self):
        """Calculates Average buy of an item"""
        return self.safe_average(self._buy)

    def get_avg_sell(self):
        """Calculates average sell of items"""
        return self.safe_average(self._sell)

    def get_avg_minsell(self):
        """Calculates average min sell of an item"""
        return self.safe_average(self._minSell)

    def get_avg_minbuy(self):
        """Calculates average min buy of an item"""
        return self.safe_average(self._min_buy)

    def get_avg_maxbuy(self):
        """Calculates average max buy of an item"""
        return self.safe_average(self._maxBuy)

    def get_avg_maxsell(self):
        """Calculates average max sell of an item"""
        return self.safe_average(self._maxSell)

    def get_buy_med(self):
        """Calculates the median buy of items."""
        flat_list = self.flatten_and_check(self._buy)
        return statistics.median(flat_list) if flat_list else 0.0

    def get_sell_med(self):
        """Get sell median of an item"""
        flat_list = self.flatten_and_check(self._sell)
        return statistics.median(flat_list) if flat_list else 0.0


class TradingAlgo:
    def __init__(self, item_day, item_hour, item_week):
        self.item_day = item_day
        self.item_hour = item_hour
        self.item_week = item_week

    def get_liquid_sell(self):
        """Get liquidity of day average sell"""
        return self.item_day.get_avg_sell()

    def possible_profit_comprehensive(self):
        """Calculates possible profit, the closer to 0 the better."""
        # Calculate the average trading cost based on recent hourly data (mediums) for more accuracy.
        immediate_trade_cost = (self.item_hour.get_buy_med() + self.item_hour.get_sell_med()) / 2

        # Incorporate daily data to get a sense of short to medium-term market trends (This could be removed)
        daily_trade_value = (self.item_day.get_buy_med() + self.item_day.get_sell_med()) / 2

        # Use weekly data for comparison to hourly and daily.
        expected_future_trade_value = (self.item_week.get_buy_med() + self.item_week.get_sell_med()) / 2

        # Calculate potential profit, factoring in immediate, daily, and weekly data
        # The method weights these differently, assuming that more recent data might be more relevant
        weighted_trade_value = (immediate_trade_cost * 0.4) + (daily_trade_value * 0.3) + (
                expected_future_trade_value * 0.3)
        profit = expected_future_trade_value - weighted_trade_value
        return profit

    def medium_sell_week(self):
        """Gets the item sell week medium"""
        return self.item_week.get_sell_med()

    def medium_buy_week(self):
        """Gets the item buy week medium"""
        return self.item_week.get_buy_med()

    def weighted_sell_volume(self):
        "Calculates the average weighted sell volume."
        day_avg_sell_vol = self.item_day.get_avg_sell_volume()
        hour_avg_sell_vol = self.item_hour.get_avg_sell_volume()
        week_avg_sell_vol = self.item_week.get_avg_sell_volume()

        weighted_sell_vol = (0.35 * day_avg_sell_vol) + (0.45 * hour_avg_sell_vol) + (0.2 * week_avg_sell_vol)
        return weighted_sell_vol

    def weighted_buy_volume(self):
        "Calculates the average weighted buy volume."
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
        self.search_function = Search()

    def metrics(self, search):
        """Determines if it's worth buying or not. Acts like main()."""
        item_result = self.search_function.search_item(search)  # Use the instance variable

        if not item_result:
            print("Item not found!")
            return False
        # This part handles the search, now we have a tuple.

        # Set up Trading Algo and the 3 items: (There has to be a better way)
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

        # Medium sell of item
        medium_sell = searched_item.medium_sell_week()

        # medium buy of item
        medium_buy = searched_item.medium_buy_week()

        # Possible Profit of item
        possible_profit = searched_item.possible_profit_comprehensive()


        instant_sell = searched_item.get_liquid_sell()

        # Compile all metrics into a dictionary (To be used with the trading algo and debugging.)
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
        points = 0
        metrics = self.metrics(search)

        if not metrics:
            print("Item not found!")
            return False

        # Check if positive possible_profit
        points += 1 if metrics["possible_profit"] > 0 else 0

        # Profitability considering volatility
        if metrics["profitability"] > -5:
            points += 1
            if metrics["volatility"] < -2:  # Subtract a point if volatility is high
                points -= 1

        # Check for Low volatility
        points += 1 if metrics["volatility"] > -3 else 0

        # Check if High liquidity with adjustment for volatility
        if metrics["liquidity"] > 1000000:
            points += 1
            if metrics["volatility"] < -2:
                points -= 1

        # Positive price momentum and high price stability
        if metrics["price_momentum"] > 0:
            points += 1
            if metrics["price_stability"] > 100:
                points += 2

        # Spread indicating the market efficiency (formula may be inacc)
        if metrics["spread"] > -50000:
            points += 1
            if metrics["liquidity"] > 1500000:
                spread_to_liquidity_ratio = abs(metrics["spread"]) / metrics["liquidity"]
                if spread_to_liquidity_ratio < 0.01:
                    points += 1

        # If the price is stable
        points += 1 if metrics["price_stability"] > 100 else 0

        # historical buy vs. sell comparison adjusted with momentum
        if metrics["historical_buy_comparison"] > metrics["historical_sell_comparison"]:
            points += 2 if metrics["price_momentum"] > 0 else 1

        # Relative volume in context of how volatile the item is.
        if metrics["relative_volume"] > 0.05:
            points += 1
            if metrics["volatility"] < -2:
                points -= 1

        # Current price relative to medium buy or sell indicating possible direction
        if metrics["current_price"] <= metrics["medium_buy"]:
            points += 1
        if metrics["current_price"] >= metrics["medium_sell"]:
            points += 2

        # Instant sell price comparison
        if metrics["instant_sell"] >= metrics["current_price"] * 0.98:
            points += 1

        #  liquidity threshold:
        points += 1 if metrics["liquidity"] > 1500000 else 0

        if points >= 10:
            decision = "Buy"
        elif 5 <= points < 10:
            decision = "Watch"
        else:
            decision = "No"

        return {"Signal": decision, "metrics": metrics}




# Fix an bug with certain items < not supported between instances of list and float.