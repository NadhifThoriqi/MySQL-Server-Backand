from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Engine
from sqlmodel import create_engine, Session, SQLModel
from typing import Any
# from sqlalchemy import Column, String, Integer, Float, Boolean
# from sqlalchemy_utils import database_exists, create_database, drop_database
# from decouple import config
import re

# PENTING: Import semua model di sini agar terdaftar di metadata
# from models.user import User, Book  <-- Contoh

DEFAULT_DB_URL = "mysql+pymysql://root@localhost/"

def validasi_karakter(teks: str):
    # 1. Normalisasi
    teks = teks.replace(" ", "_").lower()

    # 2. Validasi Karakter (Hanya mengizinkan huruf, angka, dan underscore)
    if not re.match(r"^[a-z0-9_]+$", teks):
        raise HTTPException(status_code=400, detail="Nama database mengandung karakter terlarang")
    else:
        return teks

# ==================================================
# Engine default untuk session utama aplikasi
# ==================================================
engines = create_engine(DEFAULT_DB_URL)

def run_engine(databases:str):
    return create_engine(f"{DEFAULT_DB_URL}{databases}")

def create_db_and_tables(engine: str):
    # Digunakan untuk inisialisasi awal database utama
    return SQLModel.metadata.create_all(engine)

def get_session(use_database):
    # Logika run_engine Anda di sini
    # FastAPI otomatis mengambil 'use_database' dari path URL
    engine = run_engine(use_database)
    with Session(engine) as session:
        yield session

# Ini harus berupa instance, bukan fungsi
# tokenUrl="/api/auth/login" harus sesuai dengan path di router login kamu
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/logmysql/login")