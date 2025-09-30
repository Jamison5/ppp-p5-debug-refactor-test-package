import math
import pytest
from core.items import Item, ItemPool
from core.shoppinglist import ShoppingList
from core.errors import (
    InvalidItemNameError,
    InvalidItemPriceError,
    InvalidItemPoolError,
    DuplicateItemError,
    NonExistingItemError
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
    assert item.get_price_str(quantity=2) == '$6.50'
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

def test_valid_itempool_add_item():
    pool = ItemPool()
    item = Item("apple", 1.5)
    pool.add_item(item)
    assert 'apple' in pool.items
    assert pool.items['apple'] == item

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

def test_invalid_itempool_add_items():
    pool = ItemPool()
    invalid_item = 'not an item'
    with pytest.raises(InvalidItemPoolError):
        pool.add_item(invalid_item)
    pool = ItemPool()
    item1 = Item("apple", 1.5)
    item2 = Item("apple", 2.0)
    pool.add_item(item1)
    with pytest.raises(DuplicateItemError):
        pool.add_item(item2)

def test_valid_itempool_remove_item():
    pool = ItemPool()
    item = Item("apple", 1.5)
    pool.add_item(item)
    pool.remove_item(item.name)
    assert item.name not in pool.items

def test_invalid_itempool_remove_item():
    pool = ItemPool()
    item = Item("apple", 1.5)
    with pytest.raises(NonExistingItemError):
        pool.remove_item(item.name)

def test_itempool_get_size():
    item1 = Item("apple", 1.5)
    item2 = Item("banana", 2.0)
    items_dict = {"apple": item1, "banana": item2}
    pool = ItemPool(items_dict)
    assert pool.get_size() == 2

def test_itempool_sample_items():
    item1 = Item("apple", 1.0)
    item2 = Item("banana", 2.0)
    item3 = Item("cherry", 3.0)
    pool = ItemPool({"apple": item1, "banana": item2, "cherry": item3})
    sampled = pool.sample_items(2)
    assert len(sampled) == 2
    for item in sampled:
        assert isinstance(item, Item)
        assert item.name in pool.items

def test_itempool_repr():
    item1 = Item("apple", 1.0)
    item2 = Item("banana", 2.0)
    pool = ItemPool({"apple": item1, "banana": item2})
    repr_str = repr(pool)
    assert repr_str.startswith("ItemPool(")
    assert "apple" in repr_str
    assert "banana" in repr_str
    assert "Item(" in repr_str 

def test_itempool_eq():
    item1a = Item("apple", 1.0)
    item2a = Item("banana", 2.0)
    pool1 = ItemPool({"apple": item1a, "banana": item2a})
    item1b = Item("apple", 1.0)
    item2b = Item("banana", 2.0)
    pool2 = ItemPool({"apple": item1b, "banana": item2b})
    assert pool1 == pool2

    item1 = Item("apple", 1.0)
    pool1 = ItemPool({"apple": item1})
    item2 = Item("banana", 2.0)
    pool2 = ItemPool({"banana": item2})
    assert pool1 != pool2
    assert pool1 != "not_an_itempool"

def test_valid_shoppinglist_init():
    shoping_lst = ShoppingList()
    assert isinstance(shoping_lst, ShoppingList)
    assert shoping_lst.list == []
    item1 = Item("apple", 1.0)
    item2 = Item("banana", 2.0)
    pool = ItemPool({"apple": item1, "banana": item2})
    slist = ShoppingList(item_pool=pool)
    assert len(slist.list) >= 1
    for item, qty in slist.list:
        assert isinstance(item, Item)
        assert isinstance(qty, int)
    items = {f"item{i}": Item(f"item{i}", i+1) for i in range(5)}
    pool = ItemPool(items)
    slist = ShoppingList(size=3, quantities=[2, 3, 1], item_pool=pool)
    assert len(slist.list) == 3
    for item, qty in slist.list:
        assert isinstance(item, Item)
        assert isinstance(qty, int)


def test_valid_shoppinglist_refresh():
    pass