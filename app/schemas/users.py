from typing import List, Optional
from xmlrpc.client import boolean
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name:str=Field(example="You Name")
    username:str=Field(example="Your email of unique username")
    password:str=Field(min_length=8,max_length=30)

class UserOut(BaseModel):
    id:int
    name:str
    username:str
    class Config:
        from_attributes=True

class UserUpdate(BaseModel):
    name:str=Field(example="Updated Name")
    username:str=Field(example="Updated username")
    is_active:boolean=Field(default=True)
    
class AuthenticatedUser(UserOut):
    is_active:bool=True
    org_permissions: Optional[List[str]] = None  
