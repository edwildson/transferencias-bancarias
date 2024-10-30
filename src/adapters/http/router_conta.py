# adapters/http/routes.py
# Definições das rotas da API

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.adapters.database.repository import ContaRepository, AsyncSession
from src.adapters.database.models import Conta



router = APIRouter(
    prefix='/conta',
    tags=['Contas'],
    include_in_schema=True
)


# Dependência para obter a sessão do banco de dados
async def get_db() -> AsyncSession:
    from app import async_session
    async with async_session() as session:
        yield session


@router.post("/")
async def criar_conta(nome: str, saldo: float = 0.0, db: Session = Depends(get_db)):
    conta_repo = ContaRepository(db)
    conta = await conta_repo.create_conta(nome=nome, saldo=saldo)
    return conta


@router.get("/{numero}")
async def ler_conta(numero: int, db: Session = Depends(get_db)):
    conta_repo = ContaRepository(db)
    conta = await conta_repo.get_conta(numero=numero)
    if conta is None:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return conta


@router.put("/{numero}")
async def atualizar_conta(numero: int, nome: str, db: Session = Depends(get_db)):
    conta_repo = ContaRepository(db)
    conta = await conta_repo.update_conta(numero=numero, nome=nome)
    if conta is None:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return conta


@router.delete("/{numero}")
def excluir_conta(numero: int, db: Session = Depends(get_db)):
    conta_repo = ContaRepository(db)
    conta_repo.delete_conta(numero)
    return {"detail": "Conta excluída com sucesso"}
