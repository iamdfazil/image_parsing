from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from passlib.context import CryptContext
from fastapi_jwt_auth import AuthJWT
from invoice.models import *
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv('.env')

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# app = FastAPI(title='Image_Parser', version='1.0.0')

# In-memory storage for demonstration purposes
fake_users_db = {
    "mspl": {
        "username": "mspl",
        "full_name": "mspl",
        "email": "mspl@gmail.com",
        "hashed_password": pwd_context.hash("mspl"),
        "disabled": False,
    }
}

# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
    
#     openapi_schema = get_openapi(
#         title="Your API",
#         version="1.0.0",
#         description="API with JWT authentication",
#         routes=app.routes,
#     )
#     openapi_schema["components"]["securitySchemes"] = {
#         "OAuth2PasswordBearer": {
#             "type": "oauth2",
#             "flows": {
#                 "password": {
#                     "tokenUrl": "api/V1/auth/login",
#                     "scopes": {}
#                 }
#             }
#         }
#     }
#     openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# app.openapi = custom_openapi


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire })
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire })
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt