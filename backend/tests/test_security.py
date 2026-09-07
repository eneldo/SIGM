from __future__ import annotations

import uuid

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_password_hashing():
    password = "MiPasswordSeguro123!"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)


def test_access_token_creation_and_decode():
    user_id = str(uuid.uuid4())
    tenant_id = str(uuid.uuid4())
    token = create_access_token(user_id, tenant_id)
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == user_id
    assert payload["tenant_id"] == tenant_id
    assert payload["type"] == "access"


def test_refresh_token_creation_and_decode():
    user_id = str(uuid.uuid4())
    tenant_id = str(uuid.uuid4())
    token = create_refresh_token(user_id, tenant_id)
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == user_id
    assert payload["tenant_id"] == tenant_id
    assert payload["type"] == "refresh"


def test_invalid_token_decode():
    payload = decode_token("invalid.token.here")
    assert payload is None
