import pytest
from src.crud.user_crud import create_user, UserError

def test_create_user():
    result = create_user(username='testuser', password='password')
    assert result == 'User created'

def test_create_user_existing():
    with pytest.raises(UserError):
        create_user(username='existinguser', password='password')
