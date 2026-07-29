import pytest
from src.routers.orders_router import create_order, OrderError

def test_create_order():
    response = create_order(user_id=1, cart_id=1)
    assert response['status'] == 'created'

def test_create_order_invalid_cart():
    with pytest.raises(OrderError):
        create_order(user_id=1, cart_id=999)
