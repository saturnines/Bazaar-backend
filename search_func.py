#test
class ItemSearch:
    """This class is used to search an item and return it."""

    def __init__(self):
        from items_list import baz_items
        self._baz_list = baz_items

    def get_item(self, item):
        """Helper function to return a list of items or items"""

        if len(item) < 3:
            return False

        to_search = item.replace(" ", "").lower()
        possible_item_names = []

        for keys in self._baz_list:
            original = keys
            keys = keys.replace(" ", "").lower()
            if to_search == keys:
                return [original]

            else:
                short_str = to_search[:2]
                if short_str in keys and len(possible_item_names) <= 5:
                    possible_item_names.append(original)

        return possible_item_names


class Search_Fun:
    def __init__(self):
        self._search_function = ItemSearch()

    def search_item(self, item):
        curr_item = self._search_function.get_item(item)

        if not curr_item:
            print("Item not found!")
            return False


        elif len(curr_item) > 1:
            print("Perhaps a typo. Here are some possible items.")
            for i in curr_item:
                print(i)
            return False
        else:
            return curr_item


