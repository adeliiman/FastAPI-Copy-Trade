from typing_extensions import Annotated
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from crud.user_crud import  add_user, update_users, get_user, reset_password, authenticate_user
from database import get_db
from models.user_models import UserModel
from schemas.user_schemas import UserSchema, UserCreateSchema, UserUpdateSchema, UserResetPasswd
from schemas.token_schemas import TokenSchema
from utils.security import get_current_active_user, create_access_token, get_current_user,oauth2_scheme, \
                            revoke_token, decode_access_token
from utils.config import setting
from datetime import timedelta
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import datetime


router = APIRouter(tags=['user'])



@router.get("/me", response_model=UserSchema)
def read_logged_in_user(current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
   """return user settings for current user"""
   return current_user


@router.post("/register", response_model=UserSchema, summary="Add New User")
def register(user_data: UserCreateSchema, 
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


@router.post("/refresh")
async def create_refresh_token(request: Request, db: Session = Depends(get_db)):
    try:
        if request.method == 'POST':
            form = await request.json()
            if form.get('grant_type') == 'refresh_token':
                token = form.get('refresh_token')
                payload = decode_access_token(token)
                # Check if token is not expired
                if datetime.utcfromtimestamp(payload.get('exp')) > datetime.utcnow():
                    username = payload.get('sub')
                    # Validate email
                    db_user = get_user(db, username)
                    if db_user.username:
                        access_token = create_access_token(data={'sub': username},
                                                            expires_delta=setting.JWT_EXPIRATION,
                                                            )
                        return {'access_token': access_token, 'token_type': 'bearer'}

    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/logout")
def user_logout(token: str = Depends(oauth2_scheme)):
    revoke_token(token)
    return {"message": "Token revoked"}


@router.put("/update")
def update_user(current_user: Annotated[UserModel, Depends(get_current_active_user)], 
                db: Session = Depends(get_db),
                data= Depends(UserUpdateSchema)):
    return update_users(current_user.username, db, data)



@router.post("/reset_password")
def reset_passwd(current_user: Annotated[UserModel, Depends(get_current_user)], 
                data: UserResetPasswd,
                db: Session = Depends(get_db),
                token: str = Depends(oauth2_scheme)
                ):
    reset_password(current_user, db, data)
    revoke_token(token)
    return {"message": "Password reset"}


