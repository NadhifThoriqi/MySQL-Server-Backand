from typing import Optional
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
	__tablename__ = "user"
	id: Optional[int] = Field(default=None, primary_key=True)
	username: Optional[str] = Field(default=None)
	email: Optional[str] = Field(default=None)
	password: Optional[str] = Field(default=None)