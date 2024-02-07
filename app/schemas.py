from pydantic import BaseModel, validator, EmailStr, constr, UUID4
from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import Optional
from datetime import datetime, timedelta
from uuid import UUID
import re


#USER

# Define User model
class User(BaseModel):
    first_name: str
    last_name: str
    username: str

    # @validator('first_name', 'last_name')
    # def name_must_be_string(cls, v):
    #     if not v.isalpha():
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Name must contain only alphabetic characters')
    #     return v
    
    # @validator('username')
    # def validate_email(cls, v):
    #     # Regular expression pattern for validating email format
    #     email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        
    #     if not re.match(email_pattern, v):
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid email format')
        
    #     return v


class userCreate(User):
    password: str

    # @validator('password')
    # def password_rules(cls, v):
    #     print(f"========================== v ===================== {v}")
    #     if len(v) < 8 or len(v) > 32:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Password must be between 8 and 32 characters long')
        
    #     if not any(char.isupper() for char in v):
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Password must contain atleast one Upper case character')
        
    #     if not any(char.isdigit() for char in v):
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Password must contain at least one digit')
        
    #     return v


#Get user information
class getUser(User):
    first_name: str
    last_name: str
    username: str
    password: str
    class Config():
        orm_mode = True


class showUser(User):
    #id: Optional[int]
    id: str
    account_created: Optional[datetime] = None
    account_updated: Optional[datetime] = None
    class Config():
        orm_mode = True

class updateUser(BaseModel):
    password: str   
    first_name: str
    last_name: str
    class Config():
        orm_mode = True


