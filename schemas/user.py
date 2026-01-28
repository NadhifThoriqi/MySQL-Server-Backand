from pydantic import EmailStr
from sqlmodel import SQLModel
from typing import Optional


# ==========================================================
# Schema untuk User (Bisa Lihat User Sendiri)         
# ==========================================================
# 1. Base Schema (Atribut umum)
class UserBase(SQLModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

# 2. Schema untuk Registrasi (User Baru)
class UserCreate(UserBase):
    password: str  # Frontend kirim 'password' polos

# 3. Schema untuk User Update Profil Sendiri
class UserUpdate(UserBase):
    phone_number: Optional[str] = None
    password: Optional[str] = None


# ==========================================================
# Schema untuk Admin (Bisa Lihat apapun)
# ==========================================================
class AdminBase(SQLModel):
    id: int 
    username: Optional[str] = None
    email: Optional[EmailStr] = None

# 4. Schema untuk Admin (Bisa Lihat apapun)
class AdminShow(AdminBase):
    is_active: Optional[bool] = None
    phone_number: Optional[str] = None

# 5. Schema untuk Admin (Bisa ubah apapun)
class AdminUpdateUsers(AdminShow):
    phone_number: Optional[str] = None 
    role: Optional[str] = None
    