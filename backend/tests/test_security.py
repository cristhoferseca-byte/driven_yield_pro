from app.security import hash_password, verify_password, create_token, decode_token

def test_password_hashing():
    raw_password = "SecretPassword123!"
    hashed = hash_password(raw_password)
    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_token_lifecycle():
    payload = {"sub": 42, "role": "cliente"}
    token = create_token(payload)
    assert isinstance(token, str)
    decoded = decode_token(token)
    assert decoded["sub"] == 42
    assert decoded["role"] == "cliente"
