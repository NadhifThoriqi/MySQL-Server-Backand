from pydantic import EmailStr
from sqlmodel import SQLModel
from typing import Optional


# ==========================================================
# Schema untuk User (Bisa Lihat User Sendiri)         
# ==========================================================
# 1. Base Schema (Atribut umum)
class UserBase(SQLModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

# 2. Schema untuk Registrasi (User Baru)
class UserCreate(UserBase):
    password: str  # Frontend kirim 'password' polos

# 3. Schema untuk User Update Profil Sendiri
class UserUpdate(UserBase):
    password: Optional[str] = None


# ==========================================================
# Schema untuk Admin (Bisa Lihat apapun)
# ==========================================================
