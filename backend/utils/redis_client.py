import redis.asyncio as redis
import json
import os

class RedisClient:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.client = None
    
    async def connect(self):
        self.client = await redis.from_url(self.redis_url, encoding="utf-8", decode_responses=True)
    
    async def close(self):
        if self.client:
            await self.client.close()
    
    async def publish(self, channel: str, message: dict):
        await self.client.publish(channel, json.dumps(message))
    
    async def set_cache(self, key: str, value: dict, expire: int = 3600):
        await self.client.setex(key, expire, json.dumps(value))
    
    async def get_cache(self, key: str):
        value = await self.client.get(key)
        return json.loads(value) if value else None