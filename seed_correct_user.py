from app.core.database import SessionLocal
from app.models.cliente import Cliente

def cadastrar_correto():
    db = SessionLocal()
    
    # Dados Corretos
    nome = "Guilherme Nunes (Correto)"
    empresa = "Guilherme Tech Ltda"
    cnpj = "88.888.888/0001-88" # CNPJ único
    
    # Seu número CORRETO
    telefone_com_9 = "5538984024318"
    telefone_sem_9 = "553884024318" # Versão sem o 9 (por garantia)
    
    numeros = [telefone_com_9, telefone_sem_9]
    
    for tel in numeros:
        cliente_existente = db.query(Cliente).filter(Cliente.telefone == tel).first()
        
        if cliente_existente:
            print(f"Cliente {cliente_existente.nome} já existe ({tel})!")
        else:
            novo_cliente = Cliente(
                nome=nome,
                telefone=tel,
                empresa_nome=empresa,
                cnpj_cpf=cnpj if tel == telefone_com_9 else "77.777.777/0001-77" # CNPJ diferente pra não dar erro
            )
            db.add(novo_cliente)
            print(f"Cliente {nome} cadastrado com sucesso: {tel}")
    
    db.commit()
    db.close()

if __name__ == "__main__":
    cadastrar_correto()
