from dataclasses import field
from typing import Optional
from xmlrpc.client import boolean
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: str = Field(unique=True)
    hashed_password: str
    role: Optional[str] = Field(default="user")  # Bisa diisi 'user' atau 'admin'
    Status: Optional[boolean] = Field(default=1)
    phone_number: Optional[str] = field(default="0") # Tambahkan ini