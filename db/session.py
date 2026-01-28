from fastapi.security import OAuth2PasswordBearer
from sqlmodel import create_engine, Session, SQLModel
from decouple import config
# IMPORT SEMUA MODEL DI SINI AGAR TERDAFTAR DI METADATA
from models.user import User

# Ambil URL dari .env (atau tulis langsung jika belum pakai .env)
# Format: mysql+pymysql://user:password@host/nama_db

DATABASE_URL = config("DATABASE_URL", default="mysql+pymysql://root@localhost/name_db")
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    # Ini akan membuat tabel berdasarkan model yang terdaftar di SQLModel
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# Ini harus berupa instance, bukan fungsi
# tokenUrl="/api/auth/login" harus sesuai dengan path di router login kamu
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")