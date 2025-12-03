from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.core.database import get_db
from app.models.cliente import Cliente

router = APIRouter()

# --- Pydantic Models ---
class ClienteBase(BaseModel):
    nome: str
    telefone: str
    empresa_nome: str
    cnpj_cpf: str

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    empresa_nome: Optional[str] = None
    cnpj_cpf: Optional[str] = None

from datetime import datetime

class ClienteResponse(ClienteBase):
    id: int
    data_cadastro: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Endpoints ---

@router.get("/clients", response_model=List[ClienteResponse])
def read_clients(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    clients = db.query(Cliente).offset(skip).limit(limit).all()
    return clients

@router.post("/clients", response_model=ClienteResponse)
def create_client(client: ClienteCreate, db: Session = Depends(get_db)):
    db_client = db.query(Cliente).filter(Cliente.telefone == client.telefone).first()
    if db_client:
        raise HTTPException(status_code=400, detail="Telefone já cadastrado.")
    
    db_client_cnpj = db.query(Cliente).filter(Cliente.cnpj_cpf == client.cnpj_cpf).first()
    if db_client_cnpj:
        raise HTTPException(status_code=400, detail="CNPJ/CPF já cadastrado.")
    
    new_client = Cliente(
        nome=client.nome,
        telefone=client.telefone,
        empresa_nome=client.empresa_nome,
        cnpj_cpf=client.cnpj_cpf
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@router.put("/clients/{client_id}", response_model=ClienteResponse)
def update_client(client_id: int, client: ClienteUpdate, db: Session = Depends(get_db)):
    db_client = db.query(Cliente).filter(Cliente.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    if client.nome: db_client.nome = client.nome
    if client.telefone: db_client.telefone = client.telefone
    if client.empresa_nome: db_client.empresa_nome = client.empresa_nome
    if client.cnpj_cpf: db_client.cnpj_cpf = client.cnpj_cpf
    
    db.commit()
    db.refresh(db_client)
    return db_client

@router.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(Cliente).filter(Cliente.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    db.delete(db_client)
    db.commit()
    return {"ok": True}
