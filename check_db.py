from app.core.database import SessionLocal
from app.models.cliente import Cliente

def listar_clientes():
    db = SessionLocal()
    clientes = db.query(Cliente).all()
    print(f"--- CLIENTES NO BANCO ({len(clientes)}) ---")
    for c in clientes:
        print(f"ID: {c.id} | Nome: {c.nome} | Tel: {c.telefone}")
    db.close()

if __name__ == "__main__":
    listar_clientes()
