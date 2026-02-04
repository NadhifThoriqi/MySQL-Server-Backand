from sqlmodel import text, create_engine
from db import session
from sqlalchemy_utils import database_exists, create_database, drop_database

# databases
def show_db():
    with session.engines.connect() as connection:
        # Menjalankan perintah SQL mentah
        result = connection.execute(text("SHOW DATABASES"))
        
        data = []

        for row in result:
            data.append(row[0])

        return data

def create_db(db_name: str):    
    # Membersihkan nama database agar aman
    db_url = f"{session.DEFAULT_DB_URL}{db_name}"
    
    temp_engine = create_engine(db_url)
    
    # 1. Pastikan Database Ada
    if not database_exists(temp_engine.url):
        create_database(temp_engine.url)
    else : 
        return {"status": "error", "message": f"Database '{db_name}' sudah pernah dibuat."}
    
    # 2. Pastikan Tabel Terupdate (Selalu jalankan ini!)
    # Ini tidak akan menghapus data yang sudah ada, hanya menambah tabel/kolom baru yang belum ada
    session.create_db_and_tables(temp_engine)
    
    return {"status": "success", "message": f"Database '{db_name}' berhasil dibuat dan siap digunakan."}

def delete_db(db_name:str):
    # 1. Bersihkan nama
    db_url = f"{session.DEFAULT_DB_URL}{db_name}"
    engine = create_engine(db_url)
    
    # Daftar database sistem yang tidak boleh disentuh
    protected_dbs = ["performance_schema", "sys", "information_schema", "mysql", "db_manajemen_buku"]

    # 2. Cek apakah database dilarang
    if db_name in protected_dbs:
        return {"status": "error", "message": f"Database '{db_name}' adalah database sistem/utama dan dilarang dihapus!"}

    # 3. Cek apakah database ada
    if not database_exists(engine.url):
        return {"status": "error", "message": f"Database '{db_name}' tidak ditemukan."}

    # 4. Jika lolos semua cek, barulah HAPUS
    try:
        drop_database(engine.url)
        return {"status": "success", "message": f"Database '{db_name}' berhasil dimusnahkan!"}
    except Exception as e:
        return {"status": "error", "message": f"Gagal menghapus: {str(e)}"}
