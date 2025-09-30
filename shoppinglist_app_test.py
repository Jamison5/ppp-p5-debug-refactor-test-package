import math
import pytest
from core.items import Item
from core.errors import (
    InvalidItemNameError,
    InvalidItemPriceError
)



def test_valid_item_init():
    item = Item('bread', 3.25)
    assert item.name == 'bread'
    assert math.isclose(item.price, 3.25)

def test_invalid_item_init():
    with pytest.raises(InvalidItemNameError):
        Item('', 3.25)