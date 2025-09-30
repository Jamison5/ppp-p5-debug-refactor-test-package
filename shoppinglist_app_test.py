import math
import pytest
from core.items import Item, ItemPool
from core.errors import (
    InvalidItemNameError,
    InvalidItemPriceError,
    InvalidItemPoolError
)



def test_valid_item_init():
    item = Item('bread', 3.25)
    assert item.name == 'bread'
    assert math.isclose(item.price, 3.25)

def test_invalid_item_init():
    with pytest.raises(InvalidItemNameError):
        Item('', 3.25)
    with pytest.raises(InvalidItemPriceError):
        Item('bread', -3.25)

def test_item_get_order():
    item = Item('bread', 3.25)
    assert item.get_order() == 0
    item.price = 1000.0
    assert item.get_order() == 3

def test_item_get_list_item_str():
    item = Item('bread', 3.25)
    assert item.get_list_item_str() == '- bread'
    assert item.get_list_item_str(quantity=2) == '- bread (2x)'
    assert item.get_list_item_str(
        quantity=2,
        leading_dash=True
    ) == '- bread (2x)'
    assert item.get_list_item_str(
        quantity=2,
        leading_dash=False
    ) == 'bread (2x)'

def test_item_get_price_str():
    item = Item('bread', 3.25)
    assert item.get_price_str() == '$3.25'
    assert item.get_price_str(hide_price=True) == '$?.??'
    assert item.get_price_str(order=3) == '$0003.25'

def test_item_repr():
    item = Item('bread', 3.25)
    assert repr(item) == 'Item(bread, 3.25)'
    
def test_item_eq():
    item1 = Item('bread', 3.25)
    item2 = Item('bread', 3.25)
    item3 = Item('butter', 4.10)
    assert item1 == item2
    assert item1 != item3

def test_valid_itempool_init():
    item1 = Item("apple", 1.5)
    item2 = Item("banana", 2.0)
    items_dict = {"apple": item1, "banana": item2}
    pool = ItemPool(items_dict)
    assert isinstance(pool.items, dict)
    assert all(isinstance(k, str) for k in pool.items.keys())
    assert all(isinstance(v, Item) for v in pool.items.values())
    pool = ItemPool()
    assert pool.items == {}
    assert isinstance(pool.items, dict)

def test_invalid_itempool_init():
    with pytest.raises(InvalidItemPoolError):
        ItemPool(items=['not', 'a', 'dict'])
    item = Item("apple", 1.0)
    invalid_dict = { 123 : item }
    with pytest.raises(InvalidItemPoolError):
        ItemPool(invalid_dict)
    invalid_dict = {"apple": "not_an_item"}
    with pytest.raises(InvalidItemPoolError):
        ItemPool(invalid_dict)