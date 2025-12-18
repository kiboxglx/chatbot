from app.core.database import engine, Base
# Importar todos os modelos para que o SQLAlchemy os reconheça
from app.models.cliente import Cliente
from app.models.expense import Expense

def init_db():
    try:
        print("Criando tabelas no banco de dados...")
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"❌ ERRO CRÍTICO AO INICIAR DB: {e}")
        # Importante: Não damos raise aqui para permitir que a API suba
        # Isso ajuda a diagnosticar se o problema é só banco ou aplicação inteira startando.

if __name__ == "__main__":
    init_db()
