from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import List

from db.session import get_session
from models.user import User
from schemas.user import UserBase, UserCreate, UserUpdate, AdminShow, AdminUpdateUsers  # Asumsi ada schema ini
from core import security
from services import user_service

router = APIRouter()

"""
Users Global
"""
# 1. SIGNUP
@router.post("/signup", response_model=UserBase)
def signup(user_in: UserCreate, session: Session = Depends(get_session)):
    # Cek existing
    if user_service.get_user_by_email(session, user_in.email):
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")
    
    return user_service.create_user(session, user_in)

# 2. LOGIN
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    # OAuth2PasswordRequestForm menggunakan field 'username' untuk input email/username
    user = user_service.authenticate(session, email=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(data={"sub": str(user.id)}) # Gunakan ID sebagai sub (lebih stabil)
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

# 3. GET CURRENT USER (Protected)
@router.get("/me", response_model=UserBase)
async def read_current_user(current_user: User = Depends(security.get_current_user)):
    return current_user

# 4. UPDATE PROFILE (Protected & Secure)
@router.patch("/update-profile")
def update_profile(
    data: UserUpdate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(security.get_current_user)
):
    # 1. Cek email unik (Logika ini sudah benar)
    if data.email and data.email != current_user.email:
        if user_service.get_user_by_email(session, data.email):
            raise HTTPException(status_code=400, detail="Email sudah digunakan")
    
    # 2. Paksa gunakan ID dari token, bukan dari input user (Keamanan)
    updated_user = user_service.update_user(
        session=session, # Kirim session ke sini
        db_user=current_user, # Langsung kirim objek usernya
        data_in=data
    )
    return {"message": "Profil berhasil diperbarui", "user": updated_user}

"""
Admin Only
"""
# 1. GET ALL USERS (Admin Protected)
@router.get("/admin/users", response_model=List[AdminShow])
async def read_admin_all_users(
    session: Session = Depends(get_session),
    admin_user: User = Depends(security.validate_admin) # Langsung cek admin
):
    return user_service.get_admin_all_users(session=session, type_role=admin_user)

@router.get("/users/{user_id}", response_model=AdminUpdateUsers)
def get_user_by_id(
    user_id: int, 
    session: Session = Depends(get_session),
    # Baris sakti: Hanya admin yang bisa lewat sini
    admin_user: User = Depends(security.validate_admin) 
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
        
    return user

@router.patch("/admin/update-profile")
def admin_update_users(
    data: AdminUpdateUsers,
    session: Session = Depends(get_session),
    admin_user: User = Depends(security.validate_admin), # Memastikan yang akses adalah admin
):
    # 1. Cari user yang ingin di-update berdasarkan ID di dalam data
    db_user = session.get(User, data.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    # 2. Cek jika email baru sudah dipakai orang lain
    if data.email and data.email != db_user.email:
        if user_service.get_user_by_email(session, data.email):
            raise HTTPException(status_code=400, detail="Email sudah digunakan oleh user lain")
    
    # 3. Eksekusi update melalui service
    updated_user = user_service.update_user_by_admin(session, db_user, data)
    
    return {"message": "Data user berhasil diperbarui oleh admin", "user": updated_user}

# 5. DELETE ACCOUNT (Protected)
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_own_account(
    session: Session = Depends(get_session),
    current_user: User = Depends(security.get_current_user)
):
    await user_service.delete_user(session=session, db_user=current_user.id)
    return None