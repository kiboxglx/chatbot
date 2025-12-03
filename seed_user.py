from app.core.database import SessionLocal
from app.models.cliente import Cliente

def cadastrar_usuario():
    db = SessionLocal()
    
    # Dados do Usuário
    telefone = "5531982119605"
    nome = "Guilherme Nunes"
    empresa = "Guilherme Tech Ltda"
    cnpj = "12.345.678/0001-90"
    
    # Verifica se já existe
    cliente_existente = db.query(Cliente).filter(Cliente.telefone == telefone).first()
    
    if cliente_existente:
        print(f"Cliente {cliente_existente.nome} já existe no banco de dados!")
        # Atualiza dados se necessário
        cliente_existente.nome = nome
        cliente_existente.empresa_nome = empresa
        print("Dados atualizados.")
    else:
        novo_cliente = Cliente(
            nome=nome,
            telefone=telefone,
            empresa_nome=empresa,
            cnpj_cpf=cnpj
        )
        db.add(novo_cliente)
        print(f"Cliente {nome} cadastrado com sucesso!")
    
    db.commit()
    db.close()

if __name__ == "__main__":
    cadastrar_usuario()
