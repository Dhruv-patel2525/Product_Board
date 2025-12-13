import json
from typing import List, Optional
from xmlrpc.client import boolean
from pydantic import ConfigDict, BaseModel, Field


class UserCreate(BaseModel):
    name:str=Field(json_schema_extra={"example":"You Name"})
    username:str=Field(json_schema_extra={"example":"Your email of unique username"})
    password:str=Field(min_length=8,max_length=30)

class UserOut(BaseModel):
    id:int
    name:str
    username:str
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    name:Optional[str]=Field(default=None,json_schema_extra={"example":"Updated Name"})
    username:Optional[str]=Field(default=None,json_schema_extra={"example":"Updated username"})
    is_active:Optional[boolean]=Field(default=None)
    
class AuthenticatedUser(UserOut):
    is_active:bool=True
    org_permissions: Optional[List[str]] = None  
