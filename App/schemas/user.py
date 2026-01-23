from pydantic import BaseModel, field_validator , EmailStr , Field
from fastapi import HTTPException,status
from typing import Literal,Optional,List
from datetime import date,datetime
from decimal import Decimal

import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    HEALTHWORKER = "worker"
    PARENT = "parent"

class UserWorker(BaseModel):
    name:str
    email: EmailStr
    nin_id:str
    institution_name:str
    type_institution:str
    password: str
    role:UserRole


class UserCreate(BaseModel):
    name:str
    email: EmailStr
    password: str
    role:UserRole
    

    # @field_validator("password")
    # def validate_password(cls,value):
    #     if len(value)<8:
    #         raise ValueError ("Password must contains 8 chars")
    
    class Config:
        from_attributes = True
        
class UserRead(BaseModel):
    name:str
    email:EmailStr
    role:UserRole
    is_active:bool

class DeactivateConfirmation(BaseModel):
    confirm:bool

class Token(BaseModel):
    access_token: str
    token_type: str
    role:str

class TokenData(BaseModel):
    email: Optional[str]=None

class TokenResponse(Token):
    pass

class UserLogin(BaseModel):
    email:EmailStr
    password:str

    @field_validator("password")
    def validate_password(cls,value):
        if len(value)<8:
            raise ("Password must have 8 characters")
        
class UserDelete(BaseModel):
    username:str
    password:str

    @field_validator("password")
    def validate_password(cls,value):
        if len(value)<8:
            raise ("Password must have 8 characters")

