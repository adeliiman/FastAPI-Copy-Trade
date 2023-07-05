from sqlalchemy.orm import Session
from models.user_models import UserModel
from utils.security import  get_hash_password
from models.user_models import UserModel
from fastapi import status, HTTPException


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()


def delete_users(username: str, db: Session):
    db_user = db.query(UserModel).where(UserModel.username==username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No User!")
    if db_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is Admin!")
    db.delete(db_user)
    db.commit()
    return "success"



def reset_password_by_admin(db: Session, username: str, new_passwd: str):
    db_user = db.query(UserModel).where(UserModel.username==username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_user.hashed_password = get_hash_password(plain_password=new_passwd)
    db.commit()
    db.refresh(db_user)
