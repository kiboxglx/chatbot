from app.core.database import engine, Base
# Importar todos os modelos para que o SQLAlchemy os reconheça
from app.models.cliente import Cliente

def init_db():
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    init_db()
