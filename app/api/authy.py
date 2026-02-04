# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlmodel import Session
# from typing import List

# from db.session import get_session
# from models.user import owner
# from schemas.user import UserBase, UserCreate, UserUpdate  # Asumsi ada schema ini
# from core import security
# from services import user_service

# router = APIRouter()

# """
# Users Global
# """
# # 1. SIGNUP
# @router.post("/signup", response_model=UserBase)
# def signup(user_in: UserCreate, session: Session = Depends(get_session)):
#     # Cek existing
#     if user_service.get_user_by_email(session, user_in.email):
#         raise HTTPException(status_code=400, detail="Email sudah terdaftar")
    
#     return user_service.create_user(session, user_in)

# # 2. LOGIN
# @router.post("/login")
# def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
#     # OAuth2PasswordRequestForm menggunakan field 'username' untuk input email/username
#     user = user_service.authenticate(session, email=form_data.username, password=form_data.password)
    
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, 
#             detail="Email atau password salah",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     access_token = security.create_access_token(data={"sub": str(user.id)}) # Gunakan ID sebagai sub (lebih stabil)
#     return {"access_token": access_token, "token_type": "bearer", "role": user.role}

# # 3. GET CURRENT USER (Protected)
# @router.get("/me", response_model=UserBase)
# async def read_current_user(current_user: owner = Depends(security.get_current_user)):
#     return current_user

# # 4. UPDATE PROFILE (Protected & Secure)
# @router.patch("/update-profile")
# def update_profile(
#     data: UserUpdate, 
#     session: Session = Depends(get_session),
#     current_user: owner = Depends(security.get_current_user)
# ):
#     # 1. Cek email unik (Logika ini sudah benar)
#     if data.email and data.email != current_user.email:
#         if user_service.get_user_by_email(session, data.email):
#             raise HTTPException(status_code=400, detail="Email sudah digunakan")
    
#     # 2. Paksa gunakan ID dari token, bukan dari input user (Keamanan)
#     updated_user = user_service.update_user(
#         session=session, # Kirim session ke sini
#         db_user=current_user, # Langsung kirim objek usernya
#         data_in=data
#     )
#     return {"message": "Profil berhasil diperbarui", "user": updated_user}

# # 5. DELETE ACCOUNT (Protected)
# @router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_own_account(
#     session: Session = Depends(get_session),
#     current_user: owner = Depends(security.get_current_user)
# ):
#     await user_service.delete_user(session=session, db_user=current_user.id)
#     return None