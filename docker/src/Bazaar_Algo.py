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
        # Use recent hourly data (mediums) for immediate trade cost.
        immediate_trade_cost = (self.item_hour.get_buy_med() + self.item_hour.get_sell_med()) / 2

        # Incorporate daily data for short- to medium-term trends.
        daily_trade_value = (self.item_day.get_buy_med() + self.item_day.get_sell_med()) / 2

        # Use weekly data for expected future trends.
        expected_future_trade_value = (self.item_week.get_buy_med() + self.item_week.get_sell_med()) / 2

        # Weighting the trade values (more emphasis on recent data).
        weighted_trade_value = (immediate_trade_cost * 0.4) + (daily_trade_value * 0.3) + (expected_future_trade_value * 0.3)
        profit = expected_future_trade_value - weighted_trade_value
        return profit

    def medium_sell_week(self):
        """Gets the item sell week median"""
        return self.item_week.get_sell_med()

    def medium_buy_week(self):
        """Gets the item buy week median"""
        return self.item_week.get_buy_med()

    def weighted_sell_volume(self):
        """Calculates the average weighted sell volume."""
        day_avg_sell_vol = self.item_day.get_avg_sell_volume()
        hour_avg_sell_vol = self.item_hour.get_avg_sell_volume()
        week_avg_sell_vol = self.item_week.get_avg_sell_volume()

        weighted_sell_vol = (0.35 * day_avg_sell_vol) + (0.45 * hour_avg_sell_vol) + (0.2 * week_avg_sell_vol)
        return weighted_sell_vol

    def weighted_buy_volume(self):
        """Calculates the average weighted buy volume."""
        day_avg_sell_vol = self.item_day.get_avg_sell_volume()
        hour_avg_sell_vol = self.item_hour.get_avg_sell_volume()
        week_avg_sell_vol = self.item_week.get_avg_sell_volume()

        weighted_buy_vol = (0.35 * day_avg_sell_vol) + (0.45 * hour_avg_sell_vol) + (0.2 * week_avg_sell_vol)
        return weighted_buy_vol

    def weighted_buy(self):
        """Calculates weighted buy price (not volume)"""
        day_avg_buy = self.item_day.get_avg_buy()
        hour_avg_buy = self.item_hour.get_avg_buy()
        week_avg_buy = self.item_week.get_avg_buy()
        weighted_buy_price = (0.3 * day_avg_buy) + (0.5 * hour_avg_buy) + (0.2 * week_avg_buy)
        return weighted_buy_price

    def weighted_sell(self):
        """Calculates weighted sell price (not volume)"""
        daily_avg_sell = self.item_day.get_avg_sell()
        hour_avg_sell = self.item_hour.get_avg_sell()
        week_avg_sell = self.item_week.get_avg_sell()
        weighted_sell_price = (0.3 * daily_avg_sell) + (0.5 * hour_avg_sell) + (0.2 * week_avg_sell)
        return weighted_sell_price

    def weighted_min_buy(self):
        """Calculates current minimum weighted buy price"""
        day_min_buy = self.item_day.get_avg_minbuy()
        hour_min_buy = self.item_hour.get_avg_minbuy()
        week_min_buy = self.item_week.get_avg_minbuy()
        weighted_min_buy_price = (0.3 * day_min_buy) + (0.5 * hour_min_buy) + (0.2 * week_min_buy)
        return weighted_min_buy_price

    def weighted_min_sell(self):
        """Calculates current minimum weighted sell price"""
        day_min_sell = self.item_day.get_avg_minsell()
        hour_min_sell = self.item_hour.get_avg_minsell()
        week_min_sell = self.item_week.get_avg_minsell()
        weighted_min_sell_price = (0.3 * day_min_sell) + (0.5 * hour_min_sell) + (0.2 * week_min_sell)
        return weighted_min_sell_price

    def weighted_max_buy(self):
        """Calculates current maximum weighted buy price"""
        day_max_buy = self.item_day.get_avg_maxbuy()
        hour_max_buy = self.item_hour.get_avg_maxbuy()
        week_max_buy = self.item_week.get_avg_maxbuy()
        weighted_max_buy_price = (0.3 * day_max_buy) + (0.5 * hour_max_buy) + (0.2 * week_max_buy)
        return weighted_max_buy_price

    def weighted_max_sell(self):
        """Calculates current maximum weighted sell price"""
        day_max_sell = self.item_day.get_avg_maxsell()
        hour_max_sell = self.item_hour.get_avg_maxsell()
        week_max_sell = self.item_week.get_avg_maxsell()
        weighted_max_sell_price = (0.3 * day_max_sell) + (0.5 * hour_max_sell) + (0.2 * week_max_sell)
        return weighted_max_sell_price


class Main:
    def __init__(self):
        self.search_function = Search()

    def metrics(self, search):
        """Determines if it's worth buying """
        item_result = self.search_function.search_item(search)
        if not item_result:
            print("Item not found!")
            return False

        item_day = Item(
            item_result[0].get_max_sell(), item_result[0].get_max_buy(), item_result[0].get_min_buy(),
            item_result[0].get_min_sell(), item_result[0].get_buy(), item_result[0].get_sell(),
            item_result[0].get_sell_vol(), item_result[0].get_buy_vol()
        )
        item_hour = Item(
            item_result[1].get_max_sell(), item_result[1].get_max_buy(), item_result[1].get_min_buy(),
            item_result[1].get_min_sell(), item_result[1].get_buy(), item_result[1].get_sell(),
            item_result[1].get_sell_vol(), item_result[1].get_buy_vol()
        )
        item_week = Item(
            item_result[2].get_max_sell(), item_result[2].get_max_buy(), item_result[2].get_min_buy(),
            item_result[2].get_min_sell(), item_result[2].get_buy(), item_result[2].get_sell(),
            item_result[2].get_sell_vol(), item_result[2].get_buy_vol()
        )

        searched_item = TradingAlgo(item_day, item_hour, item_week)


        profitability = ((searched_item.weighted_sell() - searched_item.weighted_buy()) /
                           searched_item.weighted_buy()) * 100

        volatility = ((searched_item.weighted_max_sell() - searched_item.weighted_max_buy()) /
                      searched_item.weighted_min_buy()) * 100

        liquid = (searched_item.weighted_buy() + searched_item.weighted_sell()) / 2

        current_price = (searched_item.weighted_sell() + searched_item.weighted_buy()) / 2
        previous_price = item_week.get_sell_med()
        momentum = (current_price - previous_price) / previous_price

        current_volume = (searched_item.weighted_buy_volume() + searched_item.weighted_sell_volume()) / 2
        average_volume = item_week.get_sell_med()
        relative_volume = current_volume / average_volume

        spread = searched_item.weighted_sell() - searched_item.weighted_buy()

        weekly_avg_price = (searched_item.weighted_min_sell() + searched_item.weighted_max_sell()) / 2
        current_price_stability = ((current_price - weekly_avg_price) / weekly_avg_price) * 100

        historical_buy_comparison = ((searched_item.weighted_buy() - searched_item.medium_buy_week()) /
                                     searched_item.medium_buy_week()) * 100

        historical_sell_comparison = ((searched_item.weighted_sell() - searched_item.medium_sell_week()) /
                                      searched_item.medium_sell_week()) * 100

        medium_sell = searched_item.medium_sell_week()
        medium_buy = searched_item.medium_buy_week()

        possible_profit = searched_item.possible_profit_comprehensive()
        instant_sell = searched_item.get_liquid_sell()

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
            "search_query": search
        }
        return metrics

    def main_algo(self, search):
        metrics = self.metrics(search)
        if not metrics:
            print("Item not found!")
            return False

        # --- Scoring helper functions ---
        def score_possible_profit(m):
            return 1 if m["possible_profit"] > 0 else 0

        def score_profitability_volatility(m):
            s = 0
            if m["profitability"] > -5:
                s += 1
                if m["volatility"] < -2:
                    s -= 1
            return s

        def score_volatility(m):
            return 1 if m["volatility"] > -3 else 0

        def score_liquidity(m):
            s = 0
            if m["liquidity"] > 1_000_000:
                s += 1
                if m["volatility"] < -2:
                    s -= 1
            if m["liquidity"] > 1_500_000:
                s += 1
            return s

        def score_momentum_stability(m):
            s = 0
            if m["price_momentum"] > 0:
                s += 1
                if m["price_stability"] > 100:
                    s += 2
            s += 1 if m["price_stability"] > 100 else 0
            return s

        def score_spread(m):
            s = 0
            if m["spread"] > -50_000:
                s += 1
                if m["liquidity"] > 1_500_000:
                    ratio = abs(m["spread"]) / m["liquidity"]
                    if ratio < 0.01:
                        s += 1
            return s

        def score_historical(m):
            if m["historical_buy_comparison"] > m["historical_sell_comparison"]:
                return 2 if m["price_momentum"] > 0 else 1
            return 0

        def score_relative_volume(m):
            s = 0
            if m["relative_volume"] > 0.05:
                s += 1
                if m["volatility"] < -2:
                    s -= 1
            return s

        def score_current_price(m):
            s = 0
            if m["current_price"] <= m["medium_buy"]:
                s += 1
            if m["current_price"] >= m["medium_sell"]:
                s += 2
            return s

        def score_instant_sell(m):
            return 1 if m["instant_sell"] >= m["current_price"] * 0.98 else 0

        #  Total
        total_points = (
            score_possible_profit(metrics) +
            score_profitability_volatility(metrics) +
            score_volatility(metrics) +
            score_liquidity(metrics) +
            score_momentum_stability(metrics) +
            score_spread(metrics) +
            score_historical(metrics) +
            score_relative_volume(metrics) +
            score_current_price(metrics) +
            score_instant_sell(metrics)
        )

        decision = "Buy" if total_points >= 10 else "Watch" if total_points >= 5 else "No"
        return {"Signal": decision, "metrics": metrics}
