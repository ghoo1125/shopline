import pytest
from src.model import CartItem, Product, User
from src.processor import Processor


def test_add_item_fail(mocker):
    test_quantity = 3
    test_user = User(id=1, name="John Doe", email="test@email.com", address="test address")
    test_product = Product(id=222, name="Apple", price=10, inventory=999)
    mock_dao = mocker.MagicMock()
    processor = Processor(mock_dao)

    # fail if user not found
    mock_dao.get_user.return_value = None
    with pytest.raises(ValueError) as e:
        processor.add_item(test_user.id, test_product.id, test_quantity)
    assert str(e.value) == "user 1 not found"

    # fail if product not exist
    mock_dao.get_user.return_value = test_user
    mock_dao.get_product.return_value = None
    with pytest.raises(ValueError) as e:
        processor.add_item(test_user.id, test_product.id, test_quantity)
    assert str(e.value) == "product 222 not exist"

def test_add_item_success(mocker):
    test_quantity = 3
    test_user = User(id=1, name="John Doe", email="test@email.com", address="test address")
    test_product = Product(id=222, name="Apple", price=10, inventory=999)
    mock_dao = mocker.MagicMock()
    processor = Processor(mock_dao)

    # add item to cart successfully
    mock_dao.get_user.return_value = test_user
    mock_dao.get_product.return_value = test_product    
    processor.add_item(test_user.id, test_product.id, test_quantity)
    mock_dao.upsert_cart_item.assert_called_with(1, 222, 3)

def test_checkout_fail(mocker):
    test_user = User(id=1, name="John Doe", email="test@email.com", address="test address")
    test_products = [
        Product(id=111, name="Apple", price=10, inventory=999),
        Product(id=222, name="Banana", price=5, inventory=3)
    ]
    test_cart_items = [
        CartItem(id=111, name="Apple", price=10, quantity=3),
        CartItem(id=222, name="Banana", price=5, quantity=10)
    ]
    mock_dao = mocker.MagicMock()
    processor = Processor(mock_dao)

    # fail if user not found
    mock_dao.get_user.return_value = None
    with pytest.raises(ValueError) as e:
        processor.checkout(test_user.id)
    assert str(e.value) == "user 1 not found"

    # fail if no item in cart
    mock_dao.get_user.return_value = test_user
    mock_dao.get_cart_items.return_value = []
    with pytest.raises(ValueError) as e:
        processor.checkout(test_user.id)
    assert str(e.value) == "no items to checkout"

    # fail if item out of stock
    mock_dao.get_user.return_value = test_user
    mock_dao.get_cart_items.return_value = test_cart_items
    mock_dao.get_products.return_value = test_products
    with pytest.raises(ValueError) as e:
        processor.checkout(test_user.id)
    assert str(e.value) == "product Banana is out of stock"

def test_checkout_success(mocker):
    test_user = User(id=1, name="John Doe", email="test@email.com", address="test address")
    test_products = [
        Product(id=111, name="Apple", price=10, inventory=999),
        Product(id=222, name="Banana", price=5, inventory=3)
    ]
    test_cart_items = [
        CartItem(id=111, name="Apple", price=10, quantity=3),
        CartItem(id=222, name="Banana", price=5, quantity=10)
    ]
    mock_dao = mocker.MagicMock()
    processor = Processor(mock_dao)

    # checkout cart successfully
    mock_dao.get_user.return_value = test_user
    test_cart_items[1].quantity = 1
    mock_dao.get_cart_items.return_value = test_cart_items
    mock_dao.get_products.return_value = test_products
    mock_dao.create_order.return_value = 1
    result = processor.checkout(test_user.id)
    assert result == 1
    mock_dao.create_order.assert_called_with(1, [
        {"id": 111, "name": "Apple", "price": 10, "quantity": 3},
        {"id": 222, "name": "Banana", "price": 5, "quantity": 1}
    ])
    mock_dao.delete_cart.assert_called_with(1)
    update_products = list(mock_dao.update_products.call_args.args[0])
    update_products.sort(key=lambda item:item.id)
    assert update_products == [
        {"id": 111, "name": "Apple", "price": 10, "inventory": 996},
        {"id": 222, "name": "Banana", "price": 5, "inventory": 2}
    ]
