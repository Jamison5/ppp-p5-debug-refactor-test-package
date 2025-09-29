import math
import random

from errors import *

class Item:
    def __init__(self, name, price):
        if type(name) != str or not name:
            raise InvalidItemNameError(name)
        self.name = name
        if not isinstance(price, (float, int)) or not price > 0:
            raise InvalidItemPriceError(price)
        self.price = round(price, 2)

    def get_order(self):
        return math.floor(round(math.log(self.price, 10), 10))

    def item2line(self, quantity = None, hide_price = False, order = None, padding = 0,leading_dash = True):
        # quantity
        if quantity is None:
            qnt_str = ''
        else:
            qnt_str = f' ({quantity}x)'

        # price
        if order is None:
            order = self.get_order()
        prcStr = '${:0' + str(order + 4) + '.2f}'
        prcStr = prcStr.format(self.price * (quantity or 1))
        if hide_price:
            prcStr = f'${"?" * (order + 1)}.??'

        # dash
        dash = ''
        if leading_dash:
            dash = '- '
        return f'{dash}{self.name}{qnt_str} ...{"." * padding} {prcStr}'
    
    def __repr__(self):
        return f'Item({self.name}, {self.price})'
    
    def __eq__(self, other):
        return isinstance(other, Item) and self.name == other.name and self.price == other.price
           

class ItemPool:
    def __init__(self, items = None):
        if not items:
            items = {}
        if type(items) != dict:
            raise InvalidItemPoolError()
        for key, val in items.items():
            if type(key) != str or type(val) != Item:
                raise InvalidItemPoolError()
        self.items = items

    def add_item(self, item):
        if type(item) != Item:
            raise InvalidItemPoolError()
        if item.name in self.items:
            raise DuplicateItemError()
        self.items[item.name] = item

    def remove_item(self, item_name):
        if item_name not in self.items:
            raise NonExistingItemError(item_name)
        del self.items[item_name]

    def get_size(self):
        return len(self.items)

    def sample_items(self, sample_size):
        return random.sample(list(self.items.values()), min(sample_size, len(self.items)))

    def show_items(self):
        max_name, max_order = 0, 0
        for item in self.items.values():
            max_name = max(max_name, len(item.name))
            max_order = max(max_order, item.get_order())
        out = 'ITEMS\n'
        for item_name in sorted(self.items.keys()):
            item = self.items[item_name]
            out += item.item2line(padding=max_name - len(item_name), order=max_order) + '\n'
        return out
    
    def __repr__(self):
        return f'ItemPool({self.items})'

    def __eq__(self, other):
        return isinstance(other, ItemPool) and self.items == other.items
