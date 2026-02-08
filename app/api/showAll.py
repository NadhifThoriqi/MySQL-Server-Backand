from fastapi import APIRouter
from services import mysql_DB_service, mysql_TBL_service

router = APIRouter()

@router.get("/show-databases/show-tables")
def all_show():
    result_final = []

    # 1. Ambil semua daftar database
    databases = mysql_DB_service.show_db()

    for db in databases:
        # Skip database sistem jika perlu agar tidak berat
        # if db in ['information_schema', 'performance_schema', 'mysql', 'sys']:
        #     continue
            
        try:
            # 2. Ambil semua tabel untuk database ini
            # Gunakan nama variabel yang berbeda dari nama fungsi (misal: current_tables)
            current_tables = mysql_TBL_service.show_tables(db)

            # 3. Masukkan ke dalam list hasil dengan format { "nama_db": [tabel1, tabel2] }
            result_final.append({
                "database": db,
                "tables": current_tables
            })
        except Exception as e:
            # Jika satu DB error (misal: hak akses), aplikasi tidak akan berhenti total
            result_final.append({
                "database": db, 
                "tables": [], 
                "error": str(e)
            })

    # 4. Return hasil penggabungan
    return result_final