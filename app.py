import random
from errors import *
from items import *
from shoppinglist import *

class AppEngine:
    def __init__(self, shoppingList = None, items = None):
        self.items = items
        self.shopping_list = shoppingList
        self.continue_execution = True
        self.message = None
        self.correct_answer = None
        self.status = None

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
            self.message = self.items.show_items()
        elif what == 'list' :
            self.message = self.shopping_list.show_list()
        else:
            self.message= f'Cannot show {what}.\n'
            self.message += 'Usage: show list|items'

    def process_add_item(self, cmd):
        item_str = cmd[4:]
        item_tuple = item_str.split(': ')
        if len(item_tuple)==2:
            name, price = item_tuple
            item = Item(name, price)
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
