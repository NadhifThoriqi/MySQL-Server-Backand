from fastapi import APIRouter, HTTPException, Path, Depends
from services import mysql_TBL_service, file_service
from typing import Dict, Any, List, Optional
from db.session import validasi_karakter, get_session
from sqlmodel import Session

router = APIRouter()

# Tables
@router.get("/{use_database}/show-tables")
def show_tables(
    use_database: str = Depends(validasi_karakter)
):
    return mysql_TBL_service.show_tables(use_database)

@router.post("/{use_database}/create-table")
def create_table(
    table_name: str, 
    columns_def: Dict[str, str], 
    use_database: str = Path(..., description="Nama database yang ingin dilihat tabelnya")
):
    x = mysql_TBL_service.create_table(use_database, table_name, columns_def)
    if x:
        file_service.save_model(use_database, table_name, columns_def)
        return {
            "status": "success",
            "database": use_database,
            "table": table_name,
            "columns": list(columns_def.keys())
        } 

@router.get("/{use_database}/show-columns-from/{table_name}")
def show_columns_from(
    use_database: Session = Depends(get_session), 
    table_name: str = Depends(validasi_karakter)
):
  return mysql_TBL_service.show_columns(use_database, table_name)

@router.post("/{use_database}/insert-into/{table_name}/values")
def insert_into(
    values: Dict[str, str],
    use_database: Session = Depends(get_session),
    table_name: str = Depends(validasi_karakter)
):
    return mysql_TBL_service.insert_into(values, use_database, table_name)

@router.get("/{use_database}/selec-from/{table_name}")
def selec_from(
    selec: Optional[str],
    where: Optional[Any],
    use_database: Session = Depends(get_session),
    table_name: str = Depends(validasi_karakter)
):
    if not selec and not where:
        return mysql_TBL_service.select_table(use_database, table_name)
    else:
        return mysql_TBL_service.select_where(use_database, selec, table_name, where)

@router.post("/{use_database}/update/{table_name}")
def update(
    data_in: List[Any],
    use_database: Session = Depends(get_session),
    table_name: str = Depends(validasi_karakter)
):
    return mysql_TBL_service.update(use_database, table_name, data_in)

@router.delete("/{use_database}/drop-table/{del_name}")
def drop_table(
    use_database: Session = Depends(get_session), 
    table_name: str = Depends(validasi_karakter)
    # del_name: str = Path(..., description="Nama table yang ingin dihapus")
):
    # table_name = validasi_karakter(del_name)
    x = mysql_TBL_service.delete_table(use_database, table_name)

    if x:
        use_db = use_database.get_bind().url.database
        file_service.delete_model(use_db, table_name)
        file_service.delete_class(use_db, table_name.capitalize())
        return f"Tabel '{table_name}' berhasil dihapus (jika ada)."