from .errors import *
from .items import *
import random

class ShoppingList:
    def __init__(self, size = None, quantities = None, item_pool = None):
        self.list = []
        if item_pool is not None:
            self.refresh(item_pool, size, quantities)

    def refresh(self, item_pool, size = None, quantities = None):
        if size is None:
            size = random.randint(1,item_pool.get_size())
        if type(size) != int or size < 1:
            raise ValueError()
        if size > item_pool.get_size():
            raise InvalidShoppingListSizeError()
        if quantities is None:
            quantities = random.choices(range(1, 10), k=size)
        if type(quantities) != list:
            raise ValueError()
        for elem in quantities:
            if type(elem) != int or elem < 1:
                raise ValueError()
        if len(quantities) < size:
            quantities = quantities + [1] * (size - len(quantities))
        if len(quantities) > size:
            quantities = quantities[:size]
        items_list = item_pool.sample_items(size)
        self.list = [(item, q) for item, q in zip(items_list, quantities)]

    def get_total_price(self):
        return round(sum([item.price * qnt for item, qnt in self.list]), 2)

    def get_item_price(self, i):
        return round(self.list[i][0].price * self.list[i][1], 2)

    def show_list(self, mask_index=None):

        line_base_len = max(len('TOTAL') - 4, max(len(item.name) for item, _ in self.list))
        total = Item('TOTAL', self.get_total_price())

        max_order = total.get_order()
        max_name = len(total.name)
        for item, _ in self.list:
            max_name = max(max_name, len(item.name))
            max_order = max(max_order, item.get_order())

        out = 'SHOPPING LIST\n'

        # Display items
        for i, (item, quantity) in enumerate(self.list):
            hide_price = mask_index == i
            padding = line_base_len - len(item.name)
            name_string = item.get_list_item_str(quantity=quantity)
            price_string = item.get_price_str(quantity=quantity, order=max_order, hide_price=hide_price)
            dots = '...'
            out += f'{name_string} {dots + "." * padding} {price_string}\n'

        # TOTAL line
        hide_price = mask_index == len(self.list)
        q_len = 5
        d_len = 2
        padding = max_name - len(total.name) + q_len + d_len
        total_name_string = total.get_list_item_str(leading_dash=False)
        total_price_string = total.get_price_str(order=max_order, hide_price=hide_price)
        dots = '...'
        total_line = f'{total_name_string} {dots + "." * padding} {total_price_string}'

        hline = '-' * len(total_line) + '\n'

        return out + hline + total_line + '\n'


    def __len__(self):
        return len(self.list)
