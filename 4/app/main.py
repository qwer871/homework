from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import timedelta

from app import crud, schemas, auth
from app.database import get_db
from app.dependencies import get_current_active_user
from app.redis_client import redis_client
from app.config import settings

app = FastAPI(title="Auth Service", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get user agent from request
def get_user_agent(request: Request) -> str:
    return request.headers.get("user-agent", "")


@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return crud.create_user(db=db, user=user)


@app.post("/login", response_model=schemas.Token)
def login(
    login_data: schemas.LoginRequest,
    db: Session = Depends(get_db),
    user_agent: str = Depends(get_user_agent)
):
    user = crud.get_user_by_email(db, email=login_data.email)
    
    if not user or not auth.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Add login history
    crud.add_login_history(db, user.id, user_agent)
    
    # Create tokens
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    refresh_token = auth.create_refresh_token(data={"sub": str(user.id)})
    
    # Store refresh token in Redis
    redis_client.store_refresh_token(str(user.id), refresh_token)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@app.post("/refresh", response_model=schemas.Token)
def refresh_token(token_data: schemas.RefreshTokenRequest, db: Session = Depends(get_db)):
    # Verify refresh token
    token_info = auth.verify_token(token_data.refresh_token)
    if not token_info or not token_info.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Check if refresh token is blacklisted
    if redis_client.is_blacklisted(token_data.refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been invalidated"
        )
    
    # Verify stored refresh token
    stored_token = redis_client.get_refresh_token(token_info.user_id)
    if not stored_token or stored_token != token_data.refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Create new tokens
    user_id = token_info.user_id
    access_token = auth.create_access_token(data={"sub": user_id})
    refresh_token = auth.create_refresh_token(data={"sub": user_id})
    
    # Update stored refresh token
    redis_client.store_refresh_token(user_id, refresh_token)
    
    # 计算刷新令牌的过期时间（以秒为单位）
    refresh_token_expire_seconds = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
    
    # Blacklist old refresh token
    redis_client.add_to_blacklist(token_data.refresh_token, refresh_token_expire_seconds)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@app.put("/user/update", response_model=schemas.UserResponse)
def update_user(
    user_update: schemas.UserUpdate,
    current_user: schemas.UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if user_update.email:
        existing_user = crud.get_user_by_email(db, email=user_update.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    updated_user = crud.update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user


@app.get("/user/history", response_model=List[schemas.LoginHistoryResponse])
def get_login_history(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    history = crud.get_login_history(db, current_user.id, skip=skip, limit=limit)
    return history


@app.post("/logout")
def logout(
    current_user: schemas.UserResponse = Depends(get_current_active_user),
    request: Request = None
):
    # Get token from authorization header
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        # Add token to blacklist with 1 hour expiration
        redis_client.add_to_blacklist(token, 3600)
    
    # Delete refresh token from Redis
    redis_client.delete_refresh_token(str(current_user.id))
    
    return {"message": "Successfully logged out"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}