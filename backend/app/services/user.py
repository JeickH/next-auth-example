from sqlalchemy.orm import Session
from typing import Optional, List
from app import models, schemas
from app.core.security import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        document=user.document,
        document_type=user.document_type,
        plan=user.plan,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create empresa for the user
    empresa = models.Empresa(
        nombre=f"Empresa de {user.full_name or user.email}",
        user_id=db_user.id
    )
    db.add(empresa)
    db.commit()
    
    return db_user

def update_user(
    db: Session, db_user: models.User, user_update: schemas.UserUpdate
) -> models.User:
    user_data = user_update.dict(exclude_unset=True)
    
    if "password" in user_data:
        hashed_password = get_password_hash(user_data["password"])
        del user_data["password"]
        user_data["hashed_password"] = hashed_password
    
    for field, value in user_data.items():
        setattr(db_user, field, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
