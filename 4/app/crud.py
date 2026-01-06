from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app import models, schemas, auth


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: str, user_update: schemas.UserUpdate) -> Optional[models.User]:  # 修改参数类型
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not db_user:
        return None
    
    if user_update.email is not None:
        db_user.email = user_update.email
    
    if user_update.password is not None:
        db_user.hashed_password = auth.get_password_hash(user_update.password)
    
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user


def add_login_history(db: Session, user_id: str, user_agent: Optional[str] = None):  # 修改参数类型
    login_history = models.LoginHistory(
        user_id=user_id,
        user_agent=user_agent
    )
    db.add(login_history)
    db.commit()
    return login_history


def get_login_history(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[models.LoginHistory]:  # 修改参数类型
    return (
        db.query(models.LoginHistory)
        .filter(models.LoginHistory.user_id == user_id)
        .order_by(models.LoginHistory.login_time.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )