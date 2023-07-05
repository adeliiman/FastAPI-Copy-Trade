
from typing import List, Union, Dict
from typing_extensions import Annotated
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from crud.admin_crud import get_user_by_email, get_all_users, delete_users, reset_password_by_admin
from crud.user_crud import  add_user, update_users, reset_password, get_user, authenticate_user
from database import get_db
from models.user_models import UserModel
from models.admin_models import AdminModel
from schemas.user_schemas import UserSchema, UserCreateSchema, UserUpdateSchema, UserResetPasswd
from schemas.admin_schemas import AdminSchema
from schemas.token_schemas import TokenSchema
from utils.security import create_access_token, get_current_super_user, oauth2_scheme, revoke_token
from utils.config import setting
from datetime import timedelta
from starlette.status import HTTP_401_UNAUTHORIZED


router = APIRouter(tags=['admin'])


@router.post("/get_all_users", response_model=List[UserSchema], summary="Get All Users")
async def users(current_user: Annotated[UserSchema, Depends(get_current_super_user)], 
          db: Session = Depends(get_db)):
    users = get_all_users(db)
    return list(users)



@router.get("/email", summary="Get User by Email")
def get_user_by(current_user: Annotated[UserSchema, Depends(get_current_super_user)], 
             email: str, 
             db: Session = Depends(get_db)
             ) -> Union[UserSchema, Dict]:
    user = get_user_by_email(db, email)
    if user:
        return user
    else:
        return {'message': 'user not found'}
    

@router.get("/{username:str}", summary="Get User by username")
def get_user_by_username(current_user: Annotated[UserSchema, Depends(get_current_super_user)], 
             username: str, 
             db: Session = Depends(get_db)
             ) -> Union[UserSchema, Dict]:
    user = get_user(db, username)
    if user:
        return user
    else:
        return {'message': 'user not found'}


@router.post("/register", response_model=UserSchema, summary="Add New User")
def register(user_data: UserCreateSchema, 
             current_user: Annotated[UserModel, Depends(get_current_super_user)],
             db: Session = Depends(get_db)):
    
    user = get_user(db, user_data.username)
    if user:
        raise HTTPException(status_code=409, detail="user exist",)
    new_user = add_user(db, user_data)
    return new_user


@router.post("/login", response_model=TokenSchema)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = authenticate_user(db, form_data.username, form_data.password)
    if not user_data:
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_expires_date = timedelta(minutes=setting.JWT_EXPIRATION)
    access_token = create_access_token(
        data={'sub': user_data.username},
        expires_delta=token_expires_date,
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post("/logout")
def user_logout(current_user: Annotated[UserModel, Depends(get_current_super_user)], token: str = Depends(oauth2_scheme)):
    revoke_token(token)
    return {"message": "Token revoked"}


@router.put("/update/{username:str}", summary="Update User by Admin")
def update_user(current_user: Annotated[UserModel, Depends(get_current_super_user)], 
                username: str,
                db: Session = Depends(get_db),
                data= Depends(UserUpdateSchema),
                ):
    return update_users(username, db, data)


@router.delete("/delete/{username:str}")
def delete_user(username: str, current_user: Annotated[UserModel, Depends(get_current_super_user)], 
                db: Session = Depends(get_db),
                ):
    return delete_users(username, db)


@router.post("/reset_password")
def reset_passwd(current_user: Annotated[UserModel, Depends(get_current_super_user)], 
                data: UserResetPasswd,
                db: Session = Depends(get_db),
                token: str = Depends(oauth2_scheme)
                ):
    reset_password(current_user, db, data)
    revoke_token(token)
    return {"message": "Password reset"}


@router.post("/reset_password/user/{username:str}")
def reset_passwd_by_admin(current_user: Annotated[UserModel, Depends(get_current_super_user)], 
                username: str,
                new_password: str,
                db: Session = Depends(get_db),
                ):
    reset_password_by_admin(db, username, new_password)
    return {"message": "password reset"}


@router.post("/setting")
def admin_setting(current_user: Annotated[UserModel, Depends(get_current_super_user)],
            data: AdminSchema,
            db: Session = Depends(get_db)):
    db_set = db.query(AdminModel).all()
    for set in db_set:
        db.delete(set)
        db.commit()
        db.refresh(set)
    set = AdminModel(percent=data.percent, leverage=data.leverage)
    db.add(set)
    db.commit()
    db.refresh(set)
    return set



