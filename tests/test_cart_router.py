import pytest
from src.routers.cart_router import add_to_cart, CartError

def test_add_to_cart():
    response = add_to_cart(user_id=1, product_id=1)
    assert response['status'] == 'added'

def test_add_to_cart_invalid_product():
    with pytest.raises(CartError):
        add_to_cart(user_id=1, product_id=999)
