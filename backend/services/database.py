"""
MongoDB async connection using Motor.
Provides a shared `db` object used across all services.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DATABASE_NAME", "cybershield")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
client: AsyncIOMotorClient = None
async def connect_to_mongo():
    """Called on app startup to create the MongoDB connection pool."""
    global client
    client = AsyncIOMotorClient(MONGO_URI)
    print(f"[DB] Connected to MongoDB at {MONGO_URI}, database='{DB_NAME}'")


async def close_mongo_connection():
    """Called on app shutdown to cleanly close the connection."""
    if client:
        client.close()
        print("[DB] MongoDB connection closed.")


def get_db():
    """Returns the database handle."""
    return client[DB_NAME]
