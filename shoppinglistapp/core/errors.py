"""
Module responsible for designating custom errors for input
validation through the applications processes.
"""


class InvalidItemNameError(Exception):
    """
    Raised when an item name is invalid.

    Conditions:
        - The item name is not a string.
        - The item name is an empty string.

    Attributes:
        item: The invalid item provided.
    """
    def __init__(self, item):
        if not isinstance(item, str):
            super().__init__(f"Item name must be a string (not {type(item)}).")
        elif item == '':
            super().__init__("Item name string cannot be empty.")


class InvalidItemPriceError(Exception):
    """
    Raised when the price argument for an Item is invalid.

    Conditions:
        - Price is not a float, integer, or a parsable non-negative string.

    Attributes:
        price: The invalid price provided.
    """
    def __init__(self, price):
        super().__init__(
            f'The price argument ("{price}") does not appear to be any of the '
            f"following: float, an integer, or a string that can be parsed to "
            f"a non-negative float."
        )


class InvalidItemPoolError(Exception):
    """
    Raised when the item pool is not properly configured.

    Conditions:
        - ItemsPool is not a dictionary.
        - Dictionary keys are not non-empty strings.
        - Dictionary values are not Item instances.
    """
    def __init__(self):
        super().__init__(
            "ItemsPool needs to be set as a dictionary with "
            "non-empty strings as keys and Item instances as values."
        )


class NonExistingItemError(Exception):
    """
    Raised when attempting to access or remove an item
    that does not exist in the item pool.

    Attributes:
        item_name: The name of the item that was not found.
    """
    def __init__(self, item_name):
        super().__init__(
            f'Item named "{item_name}" is not '
            f'present in the item pool.'
            )


class DuplicateItemError(Exception):
    """
    Raised when attempting to add an item that already exists
    in the item pool.
    """
    def __init__(self):
        super().__init__("Duplicate!")


class InvalidShoppingListSizeError(Exception):
    """
    Raised when a shopping list has an invalid size.

    Conditions:
        - List size does not meet required constraints.
    """
    def __init__(self):
        super().__init__("Invalid List Size!")
