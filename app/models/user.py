from dataclasses import field
from typing import Optional
from xmlrpc.client import boolean
from sqlmodel import SQLModel, Field

class owner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    hashed_password: str