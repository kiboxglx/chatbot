from app.core.database import SessionLocal
from app.models.cliente import Cliente

def corrigir_usuario():
    db = SessionLocal()
    
    # Dados do Usuário
    nome = "Guilherme Nunes (Sem 9)"
    empresa = "Guilherme Tech Ltda"
    cnpj = "99.999.999/0001-99" # CNPJ diferente para teste
    
    # Versão SEM o 9 (comum em APIs)
    telefone_sem_9 = "553182119605"
    
    # Verifica se já existe
    cliente_existente = db.query(Cliente).filter(Cliente.telefone == telefone_sem_9).first()
    
    if cliente_existente:
        print(f"Cliente {cliente_existente.nome} já existe (sem 9)!")
    else:
        novo_cliente = Cliente(
            nome=nome,
            telefone=telefone_sem_9,
            empresa_nome=empresa,
            cnpj_cpf=cnpj
        )
        db.add(novo_cliente)
        print(f"Cliente {nome} cadastrado com sucesso (versão sem 9)!")
    
    db.commit()
    db.close()

if __name__ == "__main__":
    corrigir_usuario()
