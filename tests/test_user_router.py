import pytest
from src.routers.user_router import create_user, UserError

def test_create_user():
    response = create_user(username='testuser', password='password')
    assert response['status'] == 'created'

def test_create_user_existing():
    with pytest.raises(UserError):
        create_user(username='existinguser', password='password')
