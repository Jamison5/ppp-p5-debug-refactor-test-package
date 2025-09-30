"""
Module for managing a shopping list with items sampled from an ItemPool.

Provides functionality to refresh the list, calculate item prices, and
get the total price.
"""

import random
from .errors import InvalidShoppingListSizeError


class ShoppingList:
    """
    Represents a shopping list of items with associated quantities.

    Attributes:
        list (list[tuple[Item, int]]): List of (Item, quantity) tuples.
    """

    def __init__(self, size=None, quantities=None, item_pool=None):
        """
        Initialize a ShoppingList.

        Args:
            size (int, optional): Desired number of items in the list.
            quantities (list[int], optional): Quantities for each item.
            item_pool (ItemPool, optional): Pool to sample items from.

        Side Effects:
            If item_pool is provided, the list is immediately populated
            using `refresh()`.
        """
        self.list = []
        if item_pool is not None:
            self.refresh(item_pool, size, quantities)

    def refresh(self, item_pool, size=None, quantities=None):
        """
        Refresh the shopping list with new items and quantities.

        Args:
            item_pool (ItemPool): Pool to sample items from.
            size (int, optional): Number of items to select. Random if None.
            quantities (list[int], optional): Quantities for each item.

        Raises:
            ValueError: If size or quantities are invalid.
            InvalidShoppingListSizeError: If requested size exceeds pool size.
        """
        if size is None:
            size = random.randint(1, item_pool.get_size())
        if not isinstance(size, int) or size < 1:
            raise ValueError()
        if size > item_pool.get_size():
            raise InvalidShoppingListSizeError()
        if quantities is None:
            quantities = random.choices(range(1, 10), k=size)
        if not isinstance(quantities, list):
            raise ValueError()
        for elem in quantities:
            if not isinstance(elem, int) or elem < 1:
                raise ValueError()
        if len(quantities) < size:
            quantities = quantities + [1] * (size - len(quantities))
        if len(quantities) > size:
            quantities = quantities[:size]
        items_list = item_pool.sample_items(size)
        self.list = list(zip(items_list, quantities))

    def get_total_price(self):
        """
        Calculate the total price of all items in the list.

        Returns:
            float: Total price rounded to 2 decimal places.
        """
        return round(sum(item.price * qnt for (item, qnt) in self.list), 2)

    def get_item_price(self, i):
        """
        Get the total price for a specific item in the list.

        Args:
            i (int): Index of the item in the list.

        Returns:
            float: Price of the item multiplied by its quantity,
            rounded to 2 decimals.
        """
        return round(self.list[i][0].price * self.list[i][1], 2)

    def __len__(self):
        """
        Get the number of items in the shopping list.

        Returns:
            int: Number of items.
        """
        return len(self.list)
