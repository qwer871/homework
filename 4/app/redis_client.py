import redis
from typing import Optional
from app.config import settings


class RedisClient:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )
    
    def add_to_blacklist(self, token: str, expire_seconds: int = 3600):
        """Add token to blacklist"""
        self.redis_client.setex(f"blacklist:{token}", expire_seconds, "1")
    
    def is_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted"""
        return self.redis_client.exists(f"blacklist:{token}") == 1
    
    def store_refresh_token(self, user_id: str, refresh_token: str):
        """Store refresh token for user"""
        key = f"refresh_token:{user_id}"
        self.redis_client.setex(key, settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600, refresh_token)
    
    def get_refresh_token(self, user_id: str) -> Optional[str]:
        """Get stored refresh token for user"""
        return self.redis_client.get(f"refresh_token:{user_id}")
    
    def delete_refresh_token(self, user_id: str):
        """Delete refresh token for user"""
        self.redis_client.delete(f"refresh_token:{user_id}")


redis_client = RedisClient()