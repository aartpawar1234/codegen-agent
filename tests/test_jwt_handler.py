import pytest
from src.auth.jwt_handler import encode_jwt, decode_jwt, JWTError

def test_encode_jwt():
    token = encode_jwt({'user_id': 1})
    assert isinstance(token, str)

def test_decode_jwt():
    token = encode_jwt({'user_id': 1})
    payload = decode_jwt(token)
    assert payload['user_id'] == 1

def test_decode_jwt_invalid_token():
    with pytest.raises(JWTError):
        decode_jwt('invalid.token')
