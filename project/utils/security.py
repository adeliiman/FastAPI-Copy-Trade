from datetime import timedelta, datetime
from typing import Optional
from typing_extensions import Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from schemas.token_schemas import TokenDataSchema
from schemas.user_schemas import UserSchema
from database import get_db
from utils.config import setting
from models.user_models import UserModel


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= setting.api_prefix + "/user/login")


from redis import Redis
redis = Redis.from_url('redis://redis:6379/0')


def get_hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(setting.JWT_EXPIRATION)
    to_encode.update({'exp': expires})
    encoded_jwt = jwt.encode(to_encode, setting.JWT_SECRET_KEY, algorithm=setting.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(setting.JWT_REFRESH_EXPIRATION)
    to_encode.update({'exp': expires, 'grant_type': 'refresh_token'})
    encoded_jwt = jwt.encode(to_encode, setting.JWT_SECRET_KEY, algorithm=setting.JWT_ALGORITHM)
    return encoded_jwt


def revoke_token(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token,setting.JWT_SECRET_KEY, algorithms=[setting.JWT_ALGORITHM])
    # add token to blacklist
    #redis.sadd('revoked_tokens', token)


def decode_access_token(db, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
    status_code= status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,setting.JWT_SECRET_KEY, algorithms=[setting.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataSchema(username=username)
    except JWTError:
        raise credentials_exception
    user =  db.query(UserModel).filter(UserModel.username == token_data.username).first()
    
    if user is None:
        raise credentials_exception
    return user


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # check token is revoked
    if redis.sismember('revoked_tokens', token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='please login')
    return decode_access_token(db, token)


def get_current_active_user(current_user: Annotated[UserSchema, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return current_user


def get_current_super_user(current_user: Annotated[UserSchema, Depends(get_current_user)]):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User isnt admin")
    return current_user


