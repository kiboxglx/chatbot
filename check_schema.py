from app.core.database import SessionLocal
from app.models.cliente import Cliente
from sqlalchemy import inspect

def check_schema():
    db = SessionLocal()
    inspector = inspect(db.get_bind())
    columns = inspector.get_columns('clientes')
    print("--- SCHEMA DA TABELA CLIENTES ---")
    for column in columns:
        print(f"Name: {column['name']} | Type: {column['type']} | Nullable: {column['nullable']}")
    db.close()

if __name__ == "__main__":
    check_schema()
