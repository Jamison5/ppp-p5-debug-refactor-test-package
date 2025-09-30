import math
import pytest
from core.items import Item, ItemPool
from core.shoppinglist import ShoppingList
from core.appengine import AppEngine
from core.errors import (
    InvalidItemNameError,
    InvalidItemPriceError,
    InvalidItemPoolError,
    DuplicateItemError,
    NonExistingItemError,
    InvalidShoppingListSizeError
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
    with pytest.raises(InvalidItemNameError):
        Item(5, 3.25)

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
    items = {f"item{i}": Item(f"item{i}", i+1) for i in range(5)}
    pool = ItemPool(items)
    slist = ShoppingList()
    slist.refresh(pool)
    assert len(slist.list) >= 1
    for item, qty in slist.list:
        assert isinstance(item, Item)
        assert isinstance(qty, int)
        assert qty >= 1
    items = {f"item{i}": Item(f"item{i}", i+1) for i in range(5)}
    pool = ItemPool(items)
    slist = ShoppingList()
    slist.refresh(pool, size=3, quantities=[2, 3, 1])
    assert len(slist.list) == 3
    for (_, qty), expected_qty in zip(slist.list, [2, 3, 1]):
        assert qty == expected_qty
    items = {f"item{i}": Item(f"item{i}", i+1) for i in range(5)}
    pool = ItemPool(items)
    slist = ShoppingList()
    short_quantities = [2]
    slist.refresh(pool, size=3, quantities=short_quantities)
    assert len(slist.list) == 3
    # first quantity should remain, rest should be 1
    _, qty1 = slist.list[0]
    _, qty2 = slist.list[1]
    _, qty3 = slist.list[2]
    assert qty1 == 2
    assert qty2 == 1
    assert qty3 == 1
    long_quantities = [2, 3, 4, 5]
    slist.refresh(pool, size=2, quantities=long_quantities)
    assert len(slist.list) == 2
    _, qty1 = slist.list[0]
    _, qty2 = slist.list[1]
    assert qty1 == 2
    assert qty2 == 3


def test_invalid_shoppinglist_refresh():
    items = {f"item{i}": Item(f"item{i}", i+1) for i in range(5)}
    pool = ItemPool(items)
    slist = ShoppingList()
    with pytest.raises(ValueError):
        slist.refresh(pool, size=-1)
    with pytest.raises(ValueError):
        slist.refresh(pool, size="three")
    with pytest.raises(ValueError):
        slist.refresh(pool, size=3, quantities="not_a_list")
    with pytest.raises(ValueError):
        slist.refresh(pool, size=3, quantities=[1, 0, 2])
    with pytest.raises(ValueError):
        slist.refresh(pool, size=3, quantities=[1, "a", 2])
    items = {f"item{i}": Item(f"item{i}", i+1) for i in range(2)}
    pool = ItemPool(items)
    slist = ShoppingList()
    with pytest.raises(InvalidShoppingListSizeError):
        slist.refresh(pool, size=5)
    
def test_itempool_get_total_price():
    item1 = Item("apple", 1.5)
    item2 = Item("banana", 2.0)
    slist = ShoppingList()
    slist.list = [(item1, 2), (item2, 3)]
    total_expected = 2 * item1.price + 3 * item2.price
    assert slist.get_total_price() == round(total_expected, 2)

def test_itempool_get_item_price():
    item1 = Item("apple", 1.5)
    item2 = Item("banana", 2.0)
    slist = ShoppingList()
    slist.list = [(item1, 2), (item2, 3)]
    assert slist.get_item_price(0) == round(2 * item1.price, 2)
    assert slist.get_item_price(1) == round(3 * item2.price, 2)

def test_itempool_len():
    item1 = Item("apple", 1.5)
    item2 = Item("banana", 2.0)
    slist = ShoppingList()
    slist.list = [(item1, 2), (item2, 3)]
    assert len(slist) == 2


def test_appengine_init():
    engine = AppEngine()
    assert engine.items is None
    assert engine.shopping_list is None
    assert engine.continue_execution is True
    assert engine.message is None
    assert engine.correct_answer is None
    assert engine.status is None
    item1 = Item("apple", 1.5)
    pool = ItemPool({"apple": item1})
    slist = ShoppingList(item_pool=pool)
    engine = AppEngine(shopping_list=slist, items=pool)
    assert engine.items == pool
    assert engine.shopping_list == slist
    assert engine.continue_execution is True
    assert engine.message is None
    assert engine.correct_answer is None
    assert engine.status is None

def test_valid_appengine_process_add_item():
    pool = ItemPool()
    engine = AppEngine(items=pool)
    engine.process_add_item("add apple: 1.5")
    assert "apple" in pool.items
    assert "added successfully" in engine.message


def test_invalid_appengine_process_add_item():
    pool = ItemPool()
    engine = AppEngine(items=pool)
    engine.process_add_item("add apple")  # Missing price
    assert "Cannot add" in engine.message
    assert "Usage: add" in engine.message
    engine.process_add_item("add : 1.5")
    assert isinstance(engine.message, InvalidItemNameError)
    engine.process_add_item("add apple: not_a_number")
    assert isinstance(engine.message, ValueError)
    engine.process_add_item("add apple: 1.5")
    engine.process_add_item("add apple: 1.5")
    assert isinstance(engine.message, DuplicateItemError)
    engine.process_add_item("add apple: -1.5")
    assert isinstance(engine.message, InvalidItemPriceError)

def test_valid_appengine_process_del_item():
    pool = ItemPool()
    engine = AppEngine(items=pool)
    item = Item("apple", 1.5)
    pool.add_item(item)
    engine.process_del_item("del apple")
    assert "apple" not in pool.items
    assert engine.message == "apple removed successfully."

def test_invalid_appengine_process_del_item():
    pool = ItemPool()
    engine = AppEngine(items=pool)
    engine.process_del_item("del banana")
    assert isinstance(engine.message, NonExistingItemError)


def test_appengine_process_answer():
    engine = AppEngine()
    engine.correct_answer = 5.25
    engine.process_answer("5.25")
    assert engine.message == "Correct!"
    assert engine.correct_answer is None
    engine = AppEngine()
    engine.correct_answer = 3.50
    engine.process_answer("2.75")
    assert "Not Correct!" in engine.message
    assert "$3.50" in engine.message
    assert "$2.75" in engine.message
    assert engine.correct_answer is None


def test_invalid_appengine_process_answer():
    engine = AppEngine()
    engine.correct_answer = 2.0
    engine.process_answer("not_a_number")
    assert engine.message == "The provided answer is not a valid number!"