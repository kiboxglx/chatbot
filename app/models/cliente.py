from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cnpj_cpf = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String, unique=True, nullable=False, comment="ID do WhatsApp")
    empresa_nome = Column(String, nullable=True)
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Cliente(nome={self.nome}, cnpj={self.cnpj_cpf})>"
