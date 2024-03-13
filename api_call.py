import requests


class Item:
    """Item class derived from the api.

    The lists here will be populated with the items stats.


    """

    def __init__(self):
        self._maxSell = []
        self._maxBuy = []
        self._min_buy = []
        self._minSell = []
        self._buy = []
        self._sell = []
        self._sellvolume = []
        self._buyvolume = []

    def set_max_sell(self, data):
        """Adds to max sell."""
        self._maxSell.append(data)

    def get_max_sell(self):
        """Returns list of max sell"""
        return self._maxSell

    def set_max_buy(self, data):
        self._maxBuy.append(data)

    def get_max_buy(self):
        return self._maxBuy

    def set_min_buy(self, data):
        """Add to min buy"""
        self._min_buy.append(data)

    def get_min_buy(self):
        return self._min_buy

    def set_min_sell(self, data):
        """Add to min sell"""
        self._minSell.append(data)

    def get_min_sell(self):
        return self._minSell

    def set_buy(self, data):
        """curr buy price"""
        self._buy.append(data)

    def get_buy(self):
        return self._buy

    def set_sell(self, data):
        self._sell.append(data)

    def get_sell(self):
        return self._sell

    def set_sell_vol(self, data):
        self._sellvolume.append(data)

    def get_sell_vol(self):
        return self._sellvolume

    def set_buy_vol(self, data):
        self._buyvolume.append(data)

    def get_buy_vol(self):
        return self._buyvolume


class Api:
    """This class searches the api"""

    def __init__(self):
        self._item_name = None
        self._item_information = Item()

    def get_api_item(self):
        return self._item_name

    def set_api_item(self, item):
        self._item_name = item

    def call_api_week(self):
        """This calls the api for weekly """
        api_item = self.get_api_item()
        api_response = requests.get(f"https://sky.coflnet.com/api/bazaar/{api_item}/history/week")

        if api_response.status_code == 400:
            print("Bad Request. Api Linked most likely changed.")
            return

        if api_response.status_code == 500:
            print("Server side problem. CoflSky Api is most likely down.")
            return

        if api_response.status_code == 503:
            print("CoflSky Api is down! Try again later.")
            return

        if api_response.status_code == 404:
            print("Website link changed, please notify the developer so they can update it!")
            return

        if api_response.status_code == 200:
            api_data = api_response.json()
            current_item = Item()
            for data in api_data:
                try:
                    current_item.set_max_buy(data.get("maxBuy", []))
                    current_item.set_min_buy(data.get("minBuy", []))
                    current_item.set_max_sell(data.get("maxSell", []))
                    current_item.set_min_sell(data.get("minSell", []))
                    current_item.set_buy(data.get("buy", []))
                    current_item.set_sell(data.get("sell", []))
                    current_item.set_sell_vol(data.get("sellVolume", []))
                    current_item.set_buy_vol(data.get("buyVolume", []))
                except KeyError:
                    pass

            return current_item

    def call_api_hourly(self):
        """Calls the api """
        api_item = self.get_api_item()
        api_response = requests.get(f"https://sky.coflnet.com/api/bazaar/{api_item}/history/hour")

        if api_response.status_code == 400:
            print("Bad Request. Api Linked most likely changed.")
            return

        if api_response.status_code == 500:
            print("Server side problem. CoflSky Api is most likely down.")
            return

        if api_response.status_code == 503:
            print("CoflSky Api is down! Try again later.")
            return

        if api_response.status_code == 404:
            print("Website link changed, please notify the developer so they can update it!")
            return

        if api_response.status_code == 200:
            api_data = api_response.json()
            current_item = Item()
            for data in api_data:
                try:
                    current_item.set_max_buy(data.get("maxBuy", []))
                    current_item.set_min_buy(data.get("minBuy", []))
                    current_item.set_max_sell(data.get("maxSell", []))
                    current_item.set_min_sell(data.get("minSell", []))
                    current_item.set_buy(data.get("buy", []))
                    current_item.set_sell(data.get("sell", []))
                    current_item.set_sell_vol(data.get("sellVolume", []))
                    current_item.set_buy_vol(data.get("buyVolume", []))
                except KeyError:
                    pass

            return current_item

    def call_api_day(self):
        """Calls the api """
        api_item = self.get_api_item()
        api_response = requests.get(f"https://sky.coflnet.com/api/bazaar/{api_item}/history/day")

        if api_response.status_code == 400:
            print("Bad Request. Api Linked most likely changed.")
            return

        if api_response.status_code == 500:
            print("Server side problem. CoflSky Api is most likely down.")
            return

        if api_response.status_code == 503:
            print("CoflSky Api is down! Try again later.")
            return

        if api_response.status_code == 404:
            print("Website link changed, please notify the developer so they can update it!")
            return

        if api_response.status_code == 200:
            api_data = api_response.json()
            current_item = Item()
            for data in api_data:
                try:
                    current_item.set_max_buy(data.get("maxBuy", []))
                    current_item.set_min_buy(data.get("minBuy", []))
                    current_item.set_max_sell(data.get("maxSell", []))
                    current_item.set_min_sell(data.get("minSell", []))
                    current_item.set_buy(data.get("buy", []))
                    current_item.set_sell(data.get("sell", []))
                    current_item.set_sell_vol(data.get("sellVolume", []))
                    current_item.set_buy_vol(data.get("buyVolume", []))
                except KeyError:
                    pass

            return current_item


class Search:
    """Handles search from user."""

    def __init__(self):
        from search_func import Search_Fun
        self._search_function = Search_Fun()
        self._api = Api()

    def search_item(self, arg):
        """Searches something returns by day/hour/week"""
        x = self._search_function.search_item(arg)
        from items_list import baz_items
        if x is False:
            return
        else:
            dict_item = baz_items[arg]
            self._api.set_api_item(dict_item)
            item_data_week = self._api.call_api_week()
            item_data_hour = self._api.call_api_hourly()
            item_data_day = self._api.call_api_day()

            data_to_process = item_data_day, item_data_hour, item_data_week
            return data_to_process #possible bug here with getters setters will fix

x = Search()
to_parse = x.search_item("Enchanted Sugar Cane")

