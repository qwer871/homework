from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app import crud, schemas, auth
from app.database import get_db
from app.redis_client import redis_client

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    
    # Check if token is blacklisted
    if redis_client.is_blacklisted(token):
        raise credentials_exception
    
    token_data = auth.verify_token(token)
    if token_data is None or token_data.user_id is None:
        raise credentials_exception
    
    # 使用 crud 函数获取用户
    from app import models
    user = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    
    return user


def get_current_active_user(current_user: schemas.UserResponse = Depends(get_current_user)):
    return current_user