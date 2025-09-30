import random
from core.errors import *
from core.items import *
from core.shoppinglist import *

class AppEngine:
    def __init__(self, shoppingList = None, items = None):
        self.items = items
        self.shopping_list = shoppingList
        self.continue_execution = True
        self.message = None
        self.correct_answer = None
        self.status = None

    def show_items(self):

        item_dictionary = self.items.items 

        max_name_len = max(len(item.name) for item in item_dictionary.values())
        max_order = max(item.get_order() for item in item_dictionary.values())
            
        out = 'ITEMS\n'

        for item_name in sorted(item_dictionary.keys()):
            item = item_dictionary[item_name]
            name_string = item.get_list_item_str()
            price_string = item.get_price_str(order=max_order)
            padding = max_name_len - len(item.name)
            dots = '...'
            out += f'{name_string} {dots + "." * padding} {price_string}\n'
        return out

    def show_list(self, mask_index=None):

        line_base_len = max(len('TOTAL') - 4, max(len(item.name) for item, _ in self.shopping_list.list))
        total = Item('TOTAL', self.shopping_list.get_total_price())

        max_order = total.get_order()
        max_name = len(total.name)

        for item, _ in self.shopping_list.list:
            max_name = max(max_name, len(item.name))
            max_order = max(max_order, item.get_order())

        out = 'SHOPPING LIST\n'

        # Display items
        for i, (item, quantity) in enumerate(self.shopping_list.list):
            hide_price = mask_index == i
            padding = line_base_len - len(item.name)
            name_string = item.get_list_item_str(quantity=quantity)
            price_string = item.get_price_str(
                quantity=quantity, 
                order=max_order, 
                hide_price=hide_price
                )
            dots = '...'
            out += f'{name_string} {dots + "." * padding} {price_string}\n'

        # TOTAL line
        hide_price = mask_index == len(self.shopping_list.list)
        q_len = 5
        d_len = 2
        padding = max_name - len(total.name) + q_len + d_len
        total_name_string = total.get_list_item_str(leading_dash=False)
        total_price_string = total.get_price_str(order=max_order, hide_price=hide_price)
        dots = '...'
        total_line = f'{total_name_string} {dots + "." * padding} {total_price_string}'

        hline = '-' * len(total_line) + '\n'

        return out + hline + total_line + '\n'

    def run(self):
        while True:
            prompt = 'What would you like to do? '
            if self.correct_answer is not None:
                prompt = 'What amount should replace the questionmarks? $'
            cmd = input(prompt)
            self.execute_command(cmd)
            print(f'{self.message}\n')
            self.message = None

            if not self.continue_execution:
                break

    def execute_command(self,cmd):
        if self.correct_answer is not None:
            self.process_answer(cmd)
        elif cmd == 'q' or cmd == 'quit':
            self.continue_execution = False
            self.message = 'Have a nice day!'
        elif cmd == 'a' or cmd == 'ask':
            self.process_ask()
        elif cmd == 'l' or cmd == 'list':
            self.shopping_list.refresh(item_pool = self.items)
            self.message = (f'Shopping list with {len(self.shopping_list)} items has been created.')
        elif cmd.startswith('show'):
            self.process_show(cmd)
        elif cmd.startswith('add'):
            self.process_add_item(cmd)
        elif cmd.startswith('del'):
            self.process_del_item(cmd)
        else:
            self.message = f'"{cmd}" is not a valid command.'

    def process_ask(self):
        q =random.randint(0, len(self.shopping_list.list))
        self.message= self.shopping_list.show_list(mask_index = q)
        if q<len(self.shopping_list.list):
            self.correct_answer = self.shopping_list.get_item_price(q)
        else:
           self.correct_answer = self.shopping_list.get_total_price()

    def process_answer(self, cmd):
        answer = round(float(cmd), 2)
        if answer == self.correct_answer:
            self.message = 'Correct!'
        else:
            self.message = f'Not Correct! (Expected ${self.correct_answer:.02f})\nYou answered ${answer:.02f}.'
        self.correct_answer = None

    def process_show(self, cmd):
        what = cmd[ 5: ]
        if what == 'items' :
            self.message = self.show_items()
        elif what == 'list' :
            self.message = self.show_list()
        else:
            self.message= f'Cannot show {what}.\n'
            self.message += 'Usage: show list|items'

    def process_add_item(self, cmd):
        item_str = cmd[4:]
        item_tuple = item_str.split(': ')
        if len(item_tuple)==2:
            name, price = item_tuple
            item = Item(name, float(price))
            self.items.add_item(item)
            self.message = f'{item} added successfully.'
        else:
            self.message = f'Cannot add "{item_str}".\n'
            self.message += 'Usage: add <item_name>: <item_price>'

    def process_del_item(self, cmd):
        item_name = cmd[4: ]
        self.items.remove_item( item_name )
        self.message =f'{item_name} removed successfully.'

if __name__ == '__main__':
    # usage example
    item2 = Item('Macbook', 1999.99)
    item3 = Item('Milk', 4.25)
    item4 = Item('Hotel Room', 255.00)
    item5 = Item('Beef Steak', 25.18)
    ip = ItemPool()
    ip.add_item(item2)
    ip.add_item(item3)
    ip.add_item(item4)
    ip.add_item(item5)
    sp = ShoppingList(size=3, quantities=[3, 2, 4], item_pool=ip)
    app = AppEngine(sp, ip)
    app.run()
