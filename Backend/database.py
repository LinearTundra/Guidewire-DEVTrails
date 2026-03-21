from pymongo import AsyncMongoClient
from dotenv import load_dotenv
from typing import Any, Dict
from os import getenv


class Database :

    def __init__(self):
        load_dotenv()
        DB_USER = getenv("DB_USER")
        DB_PASSWORD = getenv("DB_PASSWORD")
        DB_URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@gigshield.u4mip69.mongodb.net/?appName=GigShield"
        self.__client: AsyncMongoClient[Dict[str, Any]] = AsyncMongoClient(DB_URI)

    def close(self):
        self.__client.close()

    # sync context manager
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    # async context manager
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.close()