from pydantic import Field
from sqlalchemy import Table
from sqlmodel import SQLModel


class Organization(SQLModel,Table=True):
    id:Field(default=None,primary_key=True)
    