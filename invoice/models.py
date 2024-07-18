from pydantic import BaseModel
import os

class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None

class UserInDB(User):
    hashed_password: str

class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("SECRET_KEY", "supersecret")