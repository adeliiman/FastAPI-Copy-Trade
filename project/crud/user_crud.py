from sqlalchemy.orm import Session
from models.user_models import UserModel
from schemas.user_schemas import UserCreateSchema, UserUpdateSchema, UserResetPasswd
from utils.security import verify_password, get_hash_password, revoke_token
from models.user_models import UserModel
from fastapi import status, HTTPException
from typing import Union


def get_user(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()


def add_user(db: Session, user: UserCreateSchema):
    hashed_password = get_hash_password(user.password)
    db_user = UserModel(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_users(username: str, db: Session, data: UserUpdateSchema):
    db_user = db.query(UserModel).where(UserModel.username==username).first()
    db_user.api_key = data.api_key
    db_user.secret_key = data.secret_key
    db_user.email = data.email
    db.commit()
    return db_user




def reset_password(user: UserModel, db: Session, data: UserResetPasswd):
    db_user = db.query(UserModel).where(UserModel.username==user.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(plain_password=data.old_passwd, hashed_password=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Password not correct')
    db_user.hashed_password = get_hash_password(plain_password=data.new_passwd)
    db.commit()
    db.refresh(db_user)


def authenticate_user(db: Session, username: str, password: str) -> Union[bool, UserModel]:
    user: UserModel = get_user(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user