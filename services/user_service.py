from sqlmodel import Session, select
from models.user import User
from schemas.user import UserCreate, UserUpdate, AdminUpdateUsers
from core.security import hash_password, verify_password

# memasukkan data ke database
def saveData(session: Session, dataIn: any):
    """
    Menambah data ke database sesuai dengan data yang diberikan. 
    """
    session.add(dataIn)
    session.commit()
    session.refresh(dataIn)
    return dataIn

# Menambahkan data
def create_user(session: Session, user_in: UserCreate):
    hashed = hash_password(user_in.password)
    
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed,
        role="user"
    )
    return saveData(session, db_user)

# Mengambil semua user
def get_admin_all_users(session: Session, type_role: str):
    if type_role.role == "admin":
        return session.exec(select(User)).all()

# Mengambil data berdasarkan email
def get_user_by_email(session: Session, email: str):
    return session.exec(select(User).where(User.email == email)).first()

def update_user(session: Session, db_user: User, data_in: UserUpdate):
    # Ambil data kiriman (exclude_unset agar yang None tidak nimpa)
    update_data = data_in.model_dump(exclude_unset=True)

    # Update objek secara massal (Fitur keren SQLModel)
    db_user.sqlmodel_update(update_data)

    # Jika ada logika hashing password, tambahkan di sini
    if "hashed_password" in update_data:
        db_user.hashed_password = hash_password(update_data["password"])

    return saveData(session, db_user)

def authenticate(session: Session, email: str, password: str):
    user = get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def update_user_by_admin(session: Session, db_user: User, data_in: AdminUpdateUsers):
    # Konversi schema ke dict, abaikan field yang tidak diisi (None)
    update_data = data_in.model_dump(exclude_unset=True)

    # Jika admin mengubah password user tersebut
    if "password" in update_data:
        password_polos = update_data.pop("password")
        db_user.hashed_password = hash_password(password_polos)

    # Update sisa field (username, email, role, is_active, dll)
    db_user.sqlmodel_update(update_data)

    return saveData(session, db_user)

# Menghapus data berdasarkan ID
def delete_user(session: Session, db_user: User):
    session.delete(db_user)
    session.commit()
    return db_user