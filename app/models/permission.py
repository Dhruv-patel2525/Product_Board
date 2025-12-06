from sqlalchemy import null, table
from sqlmodel import Field, SQLModel

class Permission(SQLModel,table=True):
    __tablename__="permission"
    id:int=Field(default=None,primary_key=True)
    code:str=Field(nullable=False)
    description:str|None=Field(default=None,nullable=True)
