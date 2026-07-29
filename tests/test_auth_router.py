import pytest
from src.routers.auth_router import login, AuthError

def test_login():
    response = login(username='testuser', password='password')
    assert response['status'] == 'success'

def test_login_invalid_credentials():
    with pytest.raises(AuthError):
        login(username='wronguser', password='wrongpassword')
