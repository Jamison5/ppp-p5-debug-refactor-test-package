"""
Module that handles creating Items and managing the ItemPool.

Provides classes to define items with names and prices, compute
price strings, and maintain a collection of items with add/remove
operations.
"""

import math
import random
from .errors import (
    InvalidItemNameError,
    InvalidItemPriceError,
    InvalidItemPoolError,
    NonExistingItemError,
    DuplicateItemError,
)


class Item:
    """
    Represents a purchasable item with a name and a price.

    Attributes:
        name (str): Name of the item.
        price (float): Price of the item, rounded to 2 decimal places.
    """

    def __init__(self, name, price):
        """
        Initialize an Item instance.

        Args:
            name (str): Name of the item; must be a non-empty string.
            price (float|int): Price of the item; must be positive.

        Raises:
            InvalidItemNameError: If the name is not a string or empty.
            InvalidItemPriceError: If the price is not a positive number.
        """
        if not isinstance(name, str) or not name:
            raise InvalidItemNameError(name)
        self.name = name
        if not isinstance(price, (float, int)) or not price > 0:
            raise InvalidItemPriceError(price)
        self.price = round(price, 2)

    def get_order(self):
        """
        Compute the "order of magnitude" of the item price.

        Returns:
            int: Floor of the base-10 logarithm of the price.
        """
        return math.floor(round(math.log(self.price, 10), 10))

    def get_price_str(self, quantity=None, hide_price=False, order=None):
        """
        Format the price of the item as a string, optionally for a quantity.

        Args:
            - quantity (int, optional): Number of items. Defaults to 1.
            hide_price (bool, optional): If True, hide digits with '?'.
            Defaults to False.
            - order (int, optional): Order of magnitude to format against.
            Defaults to normal order.

        Returns:
            str: Formatted price string (e.g., "$12.34" or "$???.??").
        """
        if quantity is None:
            qty = 1
        else:
            qty = quantity

        total = round(self.price * qty, 2)

        normal_order = self.get_order()

        if order is None:
            target_order = normal_order
        else:
            target_order = order

        if hide_price:
            min_digits = max(normal_order + 1, target_order + 1)
            return f"${'?' * min_digits}.??"

        min_digits = max(normal_order + 1, target_order + 1)

        format_style = "${:0" + str(min_digits + 3) + ".2f}"

        return format_style.format(total)

    def get_list_item_str(self, quantity=None, leading_dash=True):
        """
        Format the item as a string suitable for listing.

        Args:
            quantity (int, optional): Number of items to display.
            leading_dash (bool, optional): Include a leading dash.
            Defaults to True.

        Returns:
            str: Formatted string, e.g., "- ItemName (3x)".
        """
        if quantity is None:
            quantity_string = ""
        else:
            quantity_string = f" ({quantity}x)"

        if leading_dash:
            dash = "- "
        else:
            dash = ""

        return f"{dash}{self.name}{quantity_string}"

    def __repr__(self):
        """Return a developer-friendly string representation of the Item."""
        return f"Item({self.name}, {self.price})"

    def __eq__(self, other):
        """
        Check equality with another Item.

        Args:
            other (Item): Another item to compare.

        Returns:
            bool: True if names and prices match.
        """
        return (
            isinstance(other, Item)
            and self.name == other.name
            and self.price == other.price
        )


class ItemPool:
    """
    A collection of Item instances, providing management and sampling.

    Attributes:
        items (dict[str, Item]): Dictionary mapping item names to Item objects.
    """

    def __init__(self, items=None):
        """
        Initialize an ItemPool.

        Args:
            items (dict[str, Item], optional): Pre-existing items.
            Defaults to empty dict.

        Raises:
            InvalidItemPoolError: If the items argument is not a
            dictionary or contains invalid keys/values.
        """
        if not items:
            items = {}
        if not isinstance(items, dict):
            raise InvalidItemPoolError()
        for key, val in items.items():
            if not isinstance(key, str) or not isinstance(val, Item):
                raise InvalidItemPoolError()
        self.items = items

    def add_item(self, item):
        """
        Add a new Item to the pool.

        Args:
            item (Item): The item to add.

        Raises:
            InvalidItemPoolError: If the argument is not an Item instance.
            DuplicateItemError: If an item with the same name already exists.
        """
        if not isinstance(item, Item):
            raise InvalidItemPoolError()
        if item.name in self.items:
            raise DuplicateItemError()
        self.items[item.name] = item

    def remove_item(self, item_name):
        """
        Remove an Item from the pool by name.

        Args:
            item_name (str): Name of the item to remove.

        Raises:
            NonExistingItemError: If the item is not present in the pool.
        """
        if item_name not in self.items:
            raise NonExistingItemError(item_name)
        del self.items[item_name]

    def get_size(self):
        """
        Get the number of items in the pool.

        Returns:
            int: Count of items.
        """
        return len(self.items)

    def sample_items(self, sample_size):
        """
        Randomly sample items from the pool.

        Args:
            sample_size (int): Number of items to sample.

        Returns:
            list[Item]: Randomly selected items, up to the size of the pool.
        """
        return random.sample(
            list(self.items.values()), min(sample_size, len(self.items))
        )

    def __repr__(self):
        """
        Return a developer-friendly string representation of the ItemPool.
        """
        return f"ItemPool({self.items})"

    def __eq__(self, other):
        """
        Check equality with another ItemPool.

        Args:
            other (ItemPool): Another pool to compare.

        Returns:
            bool: True if all items are equal.
        """
        return isinstance(other, ItemPool) and self.items == other.items
