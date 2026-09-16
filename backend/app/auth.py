import base64
import hashlib
import hmac
import json
import os
import secrets
import time

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.app.database.mongodb import database


security = HTTPBearer()
users_collection = database["users"]
users_collection.create_index("username", unique=True)

TOKEN_SECRET = os.getenv("AUTH_TOKEN_SECRET")
if not TOKEN_SECRET:
    if os.getenv("APP_ENV", "development") == "production":
        raise RuntimeError("AUTH_TOKEN_SECRET must be set in production")
    TOKEN_SECRET = "development-only-change-this-secret"
TOKEN_LIFETIME_SECONDS = 60 * 60 * 24
PASSWORD_ITERATIONS = 310_000


def _hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PASSWORD_ITERATIONS,
    )
    return f"{salt.hex()}${password_hash.hex()}"


def _verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt_hex, expected_hash = stored_hash.split("$", 1)
        actual_hash = _hash_password(
            password,
            salt=bytes.fromhex(salt_hex),
        ).split("$", 1)[1]
    except (ValueError, TypeError):
        return False

    return hmac.compare_digest(actual_hash, expected_hash)


def create_access_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": int(time.time()) + TOKEN_LIFETIME_SECONDS,
    }
    encoded_payload = base64.urlsafe_b64encode(
        json.dumps(payload, separators=(",", ":")).encode("utf-8")
    ).decode("ascii").rstrip("=")
    signature = hmac.new(
        TOKEN_SECRET.encode("utf-8"),
        encoded_payload.encode("ascii"),
        hashlib.sha256,
    ).hexdigest()
    return f"{encoded_payload}.{signature}"


def verify_access_token(token: str) -> str:
    try:
        encoded_payload, signature = token.split(".", 1)
        expected_signature = hmac.new(
            TOKEN_SECRET.encode("utf-8"),
            encoded_payload.encode("ascii"),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(signature, expected_signature):
            raise ValueError

        padding = "=" * (-len(encoded_payload) % 4)
        payload = json.loads(
            base64.urlsafe_b64decode(
                f"{encoded_payload}{padding}"
            )
        )
        username = payload["sub"]
        if payload["exp"] <= int(time.time()):
            raise ValueError
    except (KeyError, ValueError, TypeError, json.JSONDecodeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return username


def create_user(username: str, password: str) -> None:
    users_collection.insert_one({
        "username": username,
        "password_hash": _hash_password(password),
    })


def authenticate_user(username: str, password: str) -> bool:
    user = users_collection.find_one({"username": username})
    return bool(user and _verify_password(password, user["password_hash"]))


def verify_credentials(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    return verify_access_token(credentials.credentials)