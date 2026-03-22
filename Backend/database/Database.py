from pymongo import AsyncMongoClient
from dotenv import load_dotenv
from typing import Any, Dict
from os import getenv


class Database:
    """
    Manages the MongoDB connection for the GigShield platform.
    Uses AsyncMongoClient for non-blocking database operations.
    
    A module-level singleton instance `db` is created at the bottom of this file.
    Import `db` directly instead of instantiating this class manually.
    
    Connection is kept alive for the lifetime of the application — do not
    open and close per request. Close only on application shutdown via
    FastAPI lifespan or try/finally in scripts.
    
    Usage:
        from database.Database import db
        await db.get_database().workers.find_one({...})
    """

    def __init__(self):
        """
        Loads environment variables and initialises the AsyncMongoClient.
        Does not open a connection immediately — Motor connects lazily on first operation.
        """
        load_dotenv()
        DB_USER = getenv("DB_USER")
        DB_PASSWORD = getenv("DB_PASSWORD")
        DB_URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@gigshield.u4mip69.mongodb.net/?appName=GigShield"
        self._client: AsyncMongoClient[Dict[str, Any]] = AsyncMongoClient(DB_URI)

    def get_database(self):
        """
        Returns the gigshield database instance.
        Use this to access collections e.g. db.get_database().workers
        
        Returns:
            AsyncIOMotorDatabase: The gigshield database
        """
        return self._client["gigshield"]

    async def close(self):
        """
        Closes the MongoDB connection pool.
        Call this on application shutdown via FastAPI lifespan or try/finally in scripts.
        Never call this between requests.
        """
        await self._client.close()


# module level singleton — import this directly, never instantiate Database manually
db = Database()