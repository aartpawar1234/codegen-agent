import pytest
from src.crud.cart_crud import add_to_cart, remove_from_cart, CartError

def test_add_to_cart():
    result = add_to_cart(user_id=1, product_id=1)
    assert result == 'Product added to cart'

def test_remove_from_cart():
    result = remove_from_cart(user_id=1, product_id=1)
    assert result == 'Product removed from cart'

def test_remove_from_cart_not_in_cart():
    with pytest.raises(CartError):
        remove_from_cart(user_id=1, product_id=999)
