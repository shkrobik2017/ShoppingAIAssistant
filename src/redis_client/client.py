import json
from typing import Any, Optional

import redis.asyncio as redis
from settings import settings


class RedisCache:
    """
    Asynchronous Redis cache handler for storing and retrieving JSON-serializable data.
    """

    def __init__(self) -> None:
        """
        Initialize Redis client with connection parameters from settings.
        """
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True
        )

    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from Redis by key.

        Args:
            key (str): The cache key.

        Returns:
            Optional[Any]: The deserialized value if found, otherwise None.
        """
        value = await self.client.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, expire: int = 3600) -> None:
        """
        Store a value in Redis with optional expiration.

        Args:
            key (str): The cache key.
            value (Any): The data to cache (must be JSON-serializable).
            expire (int, optional): Expiration time in seconds. Defaults to 3600.
        """
        await self.client.set(key, json.dumps(value), ex=expire)


# Singleton cache instance
cache = RedisCache()
