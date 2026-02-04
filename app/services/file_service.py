import os, ast

def models_file_path(use_database, table_name):
    folder = f"app/models/{use_database}"
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    return f"{folder}/{table_name}_model.py"

def schemas_file_path(use_database):
    folder = f"app/schemas/{use_database}"
    
    if not os.path.exists(folder):
        # os.makedirs(folder)
        content = [
            "from typing import Optional",
            "from sqlmodel import SQLModel, Field",
            "",
        ]
        with open(f"{folder}_schemas.py", "w") as f:
            f.write(f"\n".join(content))
    
    return f"{folder}_schemas.py"

def save_model(use_database: str, table_name: str, columns_def: dict):
    # 1. Tentukan nama file dan folder
    models_file = models_file_path(use_database, table_name)
    schemas_file = schemas_file_path(use_database)
    
    # 2. Mapping tipe data untuk penulisan string file
    # (Kita ingin menulis 'str', bukan <class 'str'>)
    type_str_map = {
        "str": "str",
        "int": "int",
        "float": "float",
        "bool": "bool"
    }

    # 3. Susun isi file sebagai string
    class_name = table_name.capitalize()
    models_content = [
        "from typing import Optional",
        "from sqlmodel import SQLModel, Field",
        "",
        f"class {class_name}(SQLModel, table=True):",
        f"\t__tablename__ = \"{table_name}\"",
        f"\tid: Optional[int] = Field(default=None, primary_key=True)"
    ]

    schemas_content = [
        f"",
        f"class {class_name}(SQLModel):"
    ]

    schemas_content_update = [
        f"",
        f"class {class_name}_update({class_name}):"
        f"\tid: Optional[int] = Field(default=None, primary_key=True)"
    ]
    # Tambahkan kolom dari dict
    for col_name, col_type in columns_def.items():
        python_type = type_str_map.get(col_type, "str")
        line = f"\t{col_name}: Optional[{python_type}] = Field(default=None)"
        models_content.append(line)
        schemas_content.append(line)

    # 4. Tulis ke file models
    with open(models_file, "w") as f:
        f.write(f"\n".join(models_content))
    
    # 4. Tulis ke file models
    with open(schemas_file, "a") as f:
        f.write(f"\n".join(schemas_content))
        f.w(schemas_content_update)

    return models_file

def delete_model(use_database: str, table_name: str):
    file_path = models_file_path(use_database, table_name)

    if os.path.exists(file_path):
        os.remove(file_path)
        # return "File dihapus setelah diproses."
        return True

def delete_class(use_database: str, class_name_to_remove: str):
    file_path = schemas_file_path(use_database)
    # 1. Baca isi file
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()
        if not source_code.strip(): # Cek jika file kosong
            return
        node = ast.parse(source_code)

    # 2. Transformer untuk menghapus class
    class ClassRemover(ast.NodeTransformer):
        def visit_ClassDef(self, node):
            # Jika nama class sesuai, kembalikan None untuk menghapusnya
            to_remove = [class_name_to_remove, f"{class_name_to_remove}_update"]
            if node.name in to_remove:
                return None
            
            return node
        
    # 3. Terapkan transformasi
    transformer = ClassRemover()
    modified_node = transformer.visit(node)
    
    # Perbaiki informasi baris/kolom (fix location)
    ast.fix_missing_locations(modified_node)

    # 4. Tulis kembali ke file (menggunakan ast.unparse untuk Python 3.9+)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(ast.unparse(modified_node))

    return True
