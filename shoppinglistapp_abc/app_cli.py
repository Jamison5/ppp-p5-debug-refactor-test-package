"""CLI interface for managing the shopping list application."""

import random
from shoppinglistapp.core.items import Item, ItemPool
from shoppinglistapp.core.shoppinglist import ShoppingList
from shoppinglistapp.core.appengine import AppEngine


class AppCLI:
    """Main command-line interface for application."""

    def __init__(self, shopping_list=None, items=None):
        """
        Initialize AppCLI with optional ShoppingList and ItemPool.

        Args:
            shopping_list (ShoppingList, optional)
            items (ItemPool, optional)
        """
        self.app_engine = AppEngine(shopping_list, items)

    def run(self):
        """Main loop to prompt and execute user commands."""
        while True:
            prompt = "What would you like to do? "
            if self.app_engine.correct_answer is not None:
                prompt = "What amount should replace the questionmarks? $"
            cmd = input(prompt)
            self.execute_command(cmd)
            print(f"{self.app_engine.message}\n")
            self.app_engine.message = None

            if not self.app_engine.continue_execution:
                break

    def process_ask(self):
        """Randomly ask for a price in the shopping list or the total."""
        q = random.randint(0, len(self.app_engine.shopping_list.list))
        self.app_engine.message = self.show_list(mask_index=q)
        if q < len(self.app_engine.shopping_list.list):
            self.app_engine.correct_answer = (
                self.app_engine.shopping_list.get_item_price(q)
            )
        else:
            self.app_engine.correct_answer = (
                self.app_engine.shopping_list.get_total_price()
            )

    def process_show(self, cmd):
        """Handle 'show' commands for items or the shopping list."""
        what = cmd[5:]
        if what == "items":
            self.app_engine.message = self.show_items()
        elif what == "list":
            self.app_engine.message = self.show_list()
        else:
            self.app_engine.message = f"Cannot show {what}.\n"
            self.app_engine.message += "Usage: show list|items"

    def execute_command(self, cmd):
        """Parse and execute a single CLI command."""
        if self.app_engine.correct_answer is not None:
            self.app_engine.process_answer(cmd)
        elif cmd in ('q', 'quit'):
            self.app_engine.continue_execution = False
            self.app_engine.message = "Have a nice day!"
        elif cmd in ('a', 'ask'):
            self.process_ask()
        elif cmd in ('l', 'list'):
            self.app_engine.shopping_list.refresh(
                item_pool=self.app_engine.items
                )
            self.app_engine.message = (
                f"Shopping list with {len(self.app_engine.shopping_list)} "
                "items has been created."
            )
        elif cmd.startswith("show"):
            self.process_show(cmd)
        elif cmd.startswith("add"):
            self.app_engine.process_add_item(cmd)
        elif cmd.startswith("del"):
            self.app_engine.process_del_item(cmd)
        else:
            self.app_engine.message = f'"{cmd}" is not a valid command.'

    def show_items(self):
        """Return a formatted string listing all available items."""
        item_dictionary = self.app_engine.items.items

        max_name_len = max(len(item.name) for item in item_dictionary.values())
        max_order = max(item.get_order() for item in item_dictionary.values())

        out = "ITEMS\n"

        for item_name in sorted(item_dictionary.keys()):
            item = item_dictionary[item_name]
            name_string = item.get_list_item_str()
            price_string = item.get_price_str(order=max_order)
            padding = max_name_len - len(item.name)
            dots = "..."
            out += f'{name_string} {dots + "." * padding} {price_string}\n'
        return out

    def show_list(self, mask_index=None):
        """Return a formatted string of the shopping list."""
        items = self.app_engine.shopping_list.list
        line_base_len = max(len("TOTAL") - 4, max(
            len(item.name) for item, _ in items
            )
        )
        total = Item("TOTAL", self.app_engine.shopping_list.get_total_price())

        # Precompute max_name and max_order in one line
        max_name = max(len(total.name),
                       * (len(item.name) for item, _ in items)
                       )
        max_order = max(total.get_order(),
                        * (item.get_order() for item, _ in items)
                        )

        out = "SHOPPING LIST\n"

        # Display items
        for i, (item, quantity) in enumerate(items):
            hide_price = mask_index == i
            price_str = item.get_price_str(
                quantity=quantity,
                order=max_order,
                hide_price=hide_price
            )
            out += (
                f"{item.get_list_item_str(quantity=quantity)} "
                f"{'...' + '.' * (line_base_len - len(item.name))} "
                f"{price_str}\n"
            )

        # TOTAL line
        hide_price = mask_index == len(items)
        total_line = (
            f"{total.get_list_item_str(leading_dash=False)} "
            f"{'...' + '.' * (max_name - len(total.name) + 7)} "
            f"{total.get_price_str(order=max_order, hide_price=hide_price)}"
        )
        hline = "-" * len(total_line) + "\n"

        return out + hline + total_line + "\n"


if __name__ == "__main__":
    # usage example
    item2 = Item("Macbook", 1999.99)
    item3 = Item("Milk", 4.25)
    item4 = Item("Hotel Room", 255.00)
    item5 = Item("Beef Steak", 25.18)
    ip = ItemPool()
    ip.add_item(item2)
    ip.add_item(item3)
    ip.add_item(item4)
    ip.add_item(item5)
    sp = ShoppingList(size=3, quantities=[3, 2, 4], item_pool=ip)
    app = AppCLI(sp, ip)
    app.run()
