from app.services.authentication.auth_services import hash_password, verify_password, create_access_token, decode_access_token

def test_password_hashing():
    pw = "test123"
    hashed = hash_password(pw)
    assert verify_password(pw, hashed) is True
    assert verify_password("wrong", hashed) is False

def test_token_encoding_decoding():
    data = {"sub": "abc123", "email": "test@example.com"}
    token = create_access_token(data)
    decoded = decode_access_token(token)
    assert decoded["sub"] == "abc123"

def test_token_creation_and_verification():
    data = {"sub": "abc123", "email": "abc@example.com"}
    token = create_access_token(data)
    decoded = decode_access_token(token)
    assert decoded["sub"] == "abc123"
    assert decoded["email"] == "abc@example.com"
