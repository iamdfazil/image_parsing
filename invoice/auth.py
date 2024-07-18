from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext
from invoice.utils import *
from invoice.models import *
from dotenv import load_dotenv
from datetime import timedelta
import os

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/V1/auth/login")

load_dotenv('.env')

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ.get('REFRESH_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, 
            detail="Incorrect username or password"
        )
    print(user.email)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    print(access_token_expires,refresh_token_expires)
    access_token = create_access_token(data={"sub": str(user.email)}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": str(user.email)}, expires_delta=refresh_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}




#@router.get('/me', response_model=User)
#def read_users_me(Authorize: AuthJWT = Depends()):
#    Authorize.jwt_required()
#
#    current_user = Authorize.get_jwt_subject()
#    user = get_user(fake_users_db, current_user)
#    if user is None:
#        raise HTTPException(status_code=404, detail="User not found")
#    return user

