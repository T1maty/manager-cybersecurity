from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field, validator
from passlib.context import CryptContext
import re


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
        username:str | None = None


class UserBaseRegister(BaseModel):
     username:str = Field(..., min_length=5, max_length=28)
     email: EmailStr
     password: str = Field(...,min_length=8, max_length=20)
     first_name: str = Field(..., min_length=5, max_length=10)
     last_name: str = Field(..., min_length=5, max_length=10)

     @validator("username")
     def validate_username(cls, value):
         if "/^[^\s@]+@[^\s@]+\.[^\s@]{2,6}$/" in value:
             raise ValueError("Username must not contain spaces")
         return value
     
     @validator("email")
     def validate_password(cls, value):
         if "" in value:
             raise ValueError("This field cannot be empty")
         return value

     @validator("password")
     def validate_password(cls, value):
        # Ensure the password contains at least one uppercase letter, one lowercase letter, and one number
        if not re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{8,20}$", value):
            raise ValueError(
                "Password must contain at least one uppercase letter, one lowercase letter, and one number"
            )
        return value
     
 
class UserBaseLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=20)


    @validator("password")
    def validate_password(cls, value):
        if " " in value:
            raise ValueError("Password must not contain spaces")
        return value

class UserCreate(UserBaseRegister):
    pass

class UserResponse(UserBaseRegister):
   id: int


   class Config:
        orm_mode = True


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_sheme = OAuth2PasswordBearer(tokenUrl="token")