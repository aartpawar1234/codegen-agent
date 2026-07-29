import pytest
from src.crud.product_crud import get_product, ProductError

def test_get_product():
    product = get_product(product_id=1)
    assert product['id'] == 1

def test_get_product_not_found():
    with pytest.raises(ProductError):
        get_product(product_id=999)
