import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from decouple import config
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from db.session import get_session, oauth2_scheme
from models.user import User

# Konfigurasi dari .env 
SECRET_KEY = config("SECRET_KEY", default="kode-rahasia-perpustakaan")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Hashing password
def hash_password(password: str) -> str:
    # Bcrypt butuh data dalam bentuk bytes
    pwd_bytes = password.encode('utf-8')
    # Generate salt dan hash
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

# Verifikasi password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# Membuat token JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Mengambil user dari token
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = session.get(User, int(user_id))
    if user is None:
        raise credentials_exception
    return user

# Validasi apakah user adalah admin
def validate_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Akses ditolak: Fitur ini hanya untuk Admin"
        )
    return current_user