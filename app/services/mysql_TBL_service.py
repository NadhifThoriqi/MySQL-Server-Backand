from fastapi import HTTPException, Depends
from sqlmodel import SQLModel, Field, text, Session, select
from sqlalchemy.exc import SQLAlchemyError
from db import session as S
from sqlalchemy_utils import database_exists
from sqlalchemy import inspect
from typing import Dict, Optional, List, Any
import importlib

# Tables
def import_dinamis(use_db, table_name):
    module_path = f"models.{use_db}.{table_name}_model"
    try:
        # 2. Import modul secara dinamis
        module = importlib.import_module(module_path)
        
        # 3. Ambil kelas model dari modul tersebut menggunakan getattr
        # model_class_name adalah nama class di dalam file, misal "User" atau "Hero"
        return getattr(module, table_name.capitalize())
    
    except (ImportError, AttributeError) as e:
        print(f"Error: Modul atau Kelas tidak ditemukan! {e}")
        return None


def show_tables(
        use_db: str
    ):
    engine = S.run_engine(use_db)
    if not database_exists(engine.url):
        
        return {
            "status": "error", 
            "message": f"Database {use_db} tidak ditemukan!"
        }
    
    # Menggunakan SQLAlchemy Inspector
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    return tables

def create_table(
        use_db: str, 
        table_name: str, 
        columns_def: Dict[
            str, 
            str
        ]
    ):
    """
    Membuat kelas SQLModel secara dinamis dan tabel MySQL.
    input_data = {
        "product_name": "str",
        "price": "float",
        "is_available": "bool"
    }
    """
    try:
        annotations = {
            "id": Optional[int]
        }

        fields = {
            "id": Field(default=None, primary_key=True)
        }

        python_type_map = {
            "str": str,
            "int": int,
            "float": float,
            "bool": bool
        }

        for col_name, col_type in columns_def.items():
            col_type = python_type_map.get(col_type, str)
            annotations[col_name] = Optional[col_type]
            fields[col_name] = Field(default=None)


        class_attrs = {
            "__tablename__": table_name,
            "__annotations__": annotations,
            **fields,
        }
        
        dynamic_model = type(table_name, (SQLModel,), class_attrs, table=True)

        engine = S.run_engine(use_db)
        S.create_db_and_tables(engine)
        return True
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Gagal membuat tabel: {str(e)}")

def show_columns(
        use_database: Session, 
        table_name: str
    ):    
    """
    Menggunakan text() untuk mendefinisikan query SQL mentah \n
    Penggunaan :table_name sebagai parameter bind untuk keamanan (SQL Injection) \n
    Namun, karena SHOW COLUMNS tidak mendukung bind parameter untuk nama tabel, \n
    kita pastikan table_name bersih atau menggunakan f-string dengan hati-hati. 
    """
    query = text(f"SHOW FULL COLUMNS FROM `{table_name}`")
    result = use_database.exec(query)
    d = []
    for row in result:
        # Row biasanya berisi (Field, Type, Null, Key, Default, Extra)
        d.append(
            {
                "Nama": row[0],          # Field
                "Jenis": row[1],         # Type
                "Null": row[3],          # Null (Bisa kosong atau tidak)
                "Kunci": row[4],         # Key (PRI, UNI, MUL)
                "Bawaan": row[5],        # Default value
                "Ekstra": row[6],        # Extra (auto_increment, dll)
                "Komentar": row[8]       # Comment
            }
        )
    return d

def select_table(
        use_database: Session, 
        table_name: str
    ): 
    gen = use_database.get_bind().url.database
    TableClass = import_dinamis(gen, table_name)
    return use_database.exec(select(TableClass)).all()

def select_where(
        use_database: Session,
        columns:List[str], 
        table_name: str,
        filters: Dict[str, any]
    ):
    gen = use_database.get_bind().url.database

    # 1. Import Class Model secara dinamis
    # Misal: models.db_name.user_model -> class User
    TableClass = import_dinamis(gen, table_name)

    # 2. Bangun daftar kolom secara dinamis
    # Kita mengambil atribut class berdasarkan string di list 'columns'
    try:
        selected_columns = [getattr(TableClass, col) for col in columns]
    except AttributeError as e:
        raise HTTPException(status_code=400, detail=f"Kolom tidak valid: {str(e)}")
    
    # 4. Tambahkan semua filter ke dalam statement yang sama
    for key, value in filters.items():
        try:
            column_obj = getattr(TableClass, key)
            statement = statement.where(column_obj == value)
        except AttributeError:
            raise HTTPException(status_code=400, detail=f"Filter kolom '{key}' tidak ditemukan")
        
    return use_database.exec(statement).mappings().all()

def insert_into(
        dataIn: List[
            Any
        ], 
        db: Session, 
        table_name: str
    ):
    try:
        # PERINGATAN: Menjalankan query mentah karena table_name adalah string
        # Jika table_name adalah Class SQLModel, kodenya akan berbeda.
        
        # Contoh jika dataIn adalah nilai yang ingin diinsert:
        placeholders = ", ".join([f"'{str(x)}'" for x in dataIn])
        query = text(f"INSERT INTO {table_name} VALUES ({placeholders})")
        
        db.exec(query)
        db.commit()
        return {
            "status": "success"
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def update(
        use_db: Session, 
        table_name: str, 
        data_in: Dict[str, str]
    ):
    # 1. Ambil nama database dari engine aktif
    gen = use_db.get_bind().url.database

    # 2. Import class secara dinamis
    TableClass = import_dinamis(gen, table_name)

    if not TableClass:
        raise HTTPException(status_code=404, detail="Table model tidak ditemukan")
    
    # 3. Ambil ID dari data yang dikirim (Asumsi data_in punya kunci 'id')
    row_id = data_in.get("id")
    if "id" not in data_in:
        raise HTTPException(status_code=400, detail="Data harus menyertakan 'id' untuk update")
    
    # Ambil data lama dari database
    db_row = use_db.get(TableClass, row_id)
    if not db_row:
        raise HTTPException(status_code=404, detail="Data dengan ID tersebut tidak ditemukan")

    # Update objek secara massal (Fitur keren SQLModel)
    db_row.sqlmodel_update(data_in)
    
    use_db.add(db_row)
    use_db.commit()
    use_db.refresh(db_row)
    return data_in

def delete_table(
        use_database: Session, 
        table_name: str
    ):
    # engine = S.run_engine(use_database)
    statement = text(f"DROP TABLE IF EXISTS `{table_name}`")

    try:
        # with Session(engine) as session:
        use_database.exec(statement)
        use_database.commit()
        return True
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Gagal menghapus tabel: {str(e)}")