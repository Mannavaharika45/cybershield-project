"""
Authentication API routes: signup, login, and profile (me).
"""
from fastapi import APIRouter, HTTPException, status, Depends
from models.user import UserCreate, UserLogin, UserResponse, TokenResponse
from auth.auth_handler import (
    hash_password, verify_password, create_access_token, get_current_user
)
from services.database import get_db
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter()


@router.post("/signup", response_model=TokenResponse, status_code=201)
async def signup(user_data: UserCreate):
    """
    Register a new user. Stores hashed password in MongoDB.
    Returns a JWT token on success.
    """
    db = get_db()
    users = db["users"]

    # Check if email already exists
    existing = await users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists."
        )

    # Hash password and insert user document
    user_doc = {
        "full_name": user_data.full_name,
        "email": user_data.email,
        "hashed_password": hash_password(user_data.password),
        "created_at": datetime.now(timezone.utc)
    }
    result = await users.insert_one(user_doc)
    user_id = str(result.inserted_id)

    # Issue a JWT for the newly created user
    token_payload = {
        "user_id": user_id,
        "email": user_data.email,
        "full_name": user_data.full_name
    }
    access_token = create_access_token(token_payload)

    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=user_id,
            full_name=user_data.full_name,
            email=user_data.email))


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """
    Authenticate an existing user.
    Returns a JWT token on success.
    """
    db = get_db()
    users = db["users"]

    # Look up user by email
    user_doc = await users.find_one({"email": credentials.email})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Verify password
    if not verify_password(credentials.password, user_doc["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    user_id = str(user_doc["_id"])
    # Issue JWT
    token_payload = {
        "user_id": user_id,
        "email": user_doc["email"],
        "full_name": user_doc["full_name"]
    }
    access_token = create_access_token(token_payload)

    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=user_id,
            full_name=user_doc["full_name"],
            email=user_doc["email"]))


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    Return the currently authenticated user's profile.
    Requires a valid Bearer token in the Authorization header.
    """
    db = get_db()
    users = db["users"]

    user_doc = await users.find_one({"_id": ObjectId(current_user["user_id"])})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found.")

    return UserResponse(
        id=str(user_doc["_id"]),
        full_name=user_doc["full_name"],
        email=user_doc["email"]
    )
