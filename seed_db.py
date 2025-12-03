import sys
import os

# Adiciona o diretório atual ao sys.path para garantir que o módulo 'app' seja encontrado
sys.path.append(os.getcwd())

from app.core.database import SessionLocal
from app.models.cliente import Cliente
from sqlalchemy.exc import IntegrityError

def criar_cliente_teste():
    db = SessionLocal()
    try:
        # Dados do cliente fictício
        cliente_data = {
            "nome": "Empresa Teste Ltda",
            "cnpj_cpf": "00000000000191",
            "telefone": "5511999999999",
            "empresa_nome": "Tech Solutions"
        }

        # Verifica se já existe para evitar erro de duplicidade (idempotência)
        cliente_existente = db.query(Cliente).filter(Cliente.cnpj_cpf == cliente_data["cnpj_cpf"]).first()
        
        if cliente_existente:
            print(f"Cliente já existe: {cliente_existente}")
            return

        novo_cliente = Cliente(**cliente_data)
        db.add(novo_cliente)
        db.commit()
        db.refresh(novo_cliente)
        print(f"Cliente criado com sucesso: {novo_cliente}")

    except IntegrityError as e:
        db.rollback()
        print(f"Erro de integridade ao criar cliente: {e}")
    except Exception as e:
        db.rollback()
        print(f"Erro inesperado: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    criar_cliente_teste()
