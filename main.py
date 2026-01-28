from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, time

from api import authy # Import router dari modul api
from db.session import create_db_and_tables
from logger import setup_exception_handlers, logger

# Buat tabel saat aplikasi jalan
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Aplikasi sedang berjalan, membuat tabel...") # --- Kode di sini dijalankan saat STARTUP ---
    create_db_and_tables()
    
    yield # Jeda di sini: Aplikasi berjalan melayani request...

    print("Aplikasi sedang dimatikan...") # --- Kode di sini dijalankan saat SHUTDOWN ---

# 2. Inisialisasi FastAPI dengan parameter lifespan
app = FastAPI(title="Sistem Manajemen Buku", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

# Daftarkan handler global
setup_exception_handlers(app)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # 1. Catat waktu mulai
    request.state.start_time = time.perf_counter()
    return await call_next(request)

# API Router
app.include_router(authy.router, prefix="/api/auth", tags=["Authentication"])

# 3. Run FastAPI app
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True) # gunakan localhost:2600/docs untuk mengecek api yang ada