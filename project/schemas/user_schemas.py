
from pydantic import BaseModel
from pydantic import EmailStr
from typing import List


class UserBase(BaseModel):
    username: str



class UserCreateSchema(UserBase):
    password: str


class UserSchema(UserBase):
    is_active: bool
    api_key: str= None
    secret_key: str= None
    email: EmailStr= None
   
    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    api_key: str= None
    secret_key: str= None
    email: EmailStr= None

    class Config:
        orm_mode = True


class UserResetPasswd(BaseModel):
    old_passwd: str
    new_passwd: str
    
    class Config:
        orm_mode = True