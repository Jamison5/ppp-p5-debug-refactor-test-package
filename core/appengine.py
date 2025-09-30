"""Core processor of application, handles processing for answers,
adding items to ItemPool and removing Items from ItemPool."""

from .errors import (
    InvalidItemNameError,
    DuplicateItemError,
    InvalidItemPriceError,
    NonExistingItemError,
)
from .items import Item


class AppEngine:
    """
    Core application engine responsible for processing user commands.

    Handles operations such as verifying numeric answers, adding items
    to the item pool, and removing items. Provides status messages and
    tracks the current state of the application.
    """

    def __init__(self, shopping_list=None, items=None):
        """
        Initialize the AppEngine.

        Args:
            shopping_list (ShoppingList, optional): The shopping list
                instance that may be modified or referenced by commands.
            items (ItemPool, optional): The pool of items to manage.
        """
        self.items = items
        self.shopping_list = shopping_list
        self.continue_execution = True
        self.message = None
        self.correct_answer = None
        self.status = None

    def process_answer(self, cmd):
        """
        Process the user-provided answer the numeric question.

        Args:
            cmd (str): The user input string representing their answer.

        Side Effects:
            - Updates 'self.message' with feedback about correctness
              or validity of the answer
            - Resets 'self.correct_answer' to None after checking.
        """
        try:
            answer = round(float(cmd), 2)
            if answer == self.correct_answer:
                self.message = "Correct!"
            else:
                self.message = (
                    f"Not Correct! (Expected ${self.correct_answer:.02f})\n"
                    f"You answered ${answer:.02f}."
                )
            self.correct_answer = None
        except ValueError:
            self.message = "The provided answer is not a valid number!"

    def process_add_item(self, cmd):
        """
        Add a new item to the item pool.

        Args:
            cmd (str): Command string in the format
                'add <item_name>: <item_price>'.

        Side Effects:
            - Add an Item to 'self.items' if valid.
            - Updates 'self.message' with a success or error message.

        Raises:
            InvalidItemNameError: If the item name is invlaid.
            DuplicateItemError: If the item already exists.
            InvalidItemPriceError: If the price is not valid.
        """
        try:
            item_str = cmd[4:]
            item_tuple = item_str.split(": ")
            if len(item_tuple) == 2:
                name, price = item_tuple
                item = Item(name, float(price))
                self.items.add_item(item)
                self.message = f"{item} added successfully."
            else:
                self.message = f'Cannot add "{item_str}".\n'
                self.message += "Usage: add <item_name>: <item_price>"
        except ValueError as e:
            self.message = e
        except InvalidItemNameError as e:
            self.message = e
        except DuplicateItemError as e:
            self.message = e
        except InvalidItemPriceError as e:
            self.message = e

    def process_del_item(self, cmd):
        """
        Remove an item from the item pool.

        Args:
            cmd (str): Command string in the format
                "del <item_name>".

        Side Effects:
            - Removes the item from `self.items` if it exists.
            - Updates `self.message` with a success or error message.

        Raises:
            NonExistingItemError: If the specified item does not exist.
        """
        try:
            item_name = cmd[4:]
            self.items.remove_item(item_name)
            self.message = f"{item_name} removed successfully."
        except NonExistingItemError as e:
            self.message = e
