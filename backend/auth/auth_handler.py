"""
JWT creation, decoding, and password hashing utilities.
Uses the `bcrypt` library directly to avoid a passlib/Python 3.13 compatibility issue.
"""
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# --- Configuration (read from environment, never hardcode secrets) ---
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "cybershield-local-dev-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

security = HTTPBearer()

# --- Password hashing (using bcrypt directly, not passlib) ---


def hash_password(plain: str) -> str:
    """Hash a plain-text password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain-text password against its bcrypt hash."""
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

# --- JWT ---


def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT that encodes user identity."""
    to_encode = data.copy()
    expire = datetime.now(
        timezone.utc) + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """Decode a JWT and return its payload, or None if invalid/expired."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

# --- FastAPI dependency ---


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    FastAPI dependency that validates the Bearer token.
    Inject into any protected endpoint with: Depends(get_current_user)
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload  # contains: user_id, email, full_name
