from fastapi import APIRouter, HTTPException, Path
from services import mysql_DB_service
from db.session import validasi_karakter

router = APIRouter()

# Databases
@router.get("/show-databases")
def show_databases():
    return mysql_DB_service.show_db()

@router.post("/create-database")
def create_database(
    db_name: str = Path(..., description="Nama database yang ingin dibuat")
):
    db_name = db_name.replace(" ", "_").lower()
    return mysql_DB_service.create_db(validasi_karakter(db_name))

@router.delete("/drop-database")
def delete_database(
    db_name:str = Path(..., description="Nama database yang ingin dihapus")
):
    db_name = db_name.replace(" ", "_").lower()
    result = mysql_DB_service.delete_db(validasi_karakter(db_name))
    
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
        
    return result