import pytest
from src.crud.order_crud import create_order, OrderError

def test_create_order():
    result = create_order(user_id=1, cart_id=1)
    assert result == 'Order created'

def test_create_order_invalid_cart():
    with pytest.raises(OrderError):
        create_order(user_id=1, cart_id=999)
