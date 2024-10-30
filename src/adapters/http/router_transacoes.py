# adapters/http/routes.py
# Definições das rotas da API

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.adapters.database.repository import TransacaoRepository, ContaRepository, AsyncSession
from src.adapters.database.models import Transacao, TipoTransacao

import json

router = APIRouter(
    prefix='/transacoes',
    tags=['Contas'],
    include_in_schema=True
)


# Dependência para obter a sessão do banco de dados
async def get_db() -> AsyncSession:
    from app import async_session
    async with async_session() as session:
        yield session


@router.post("/deposito")
async def deposito(numero_conta: int, valor: float, db: Session = Depends(get_db)):
    conta_repo = ContaRepository(db)
    conta = await conta_repo.get_conta(numero_conta)
    if conta is None:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    # Criar evento de depósito
    transacao_repo = TransacaoRepository(db)
    transacao = await transacao_repo.abrir_transacao(TipoTransacao.TRANSFERENCIA, conta_origem=numero_conta, valor=valor)

    evento = {
        "tipo": "transferencia",
        "conta_origem": numero_conta,
        "valor": valor,
        "transacao_id": transacao.id,
    }

    from app import kafka_producer
    await kafka_producer.send_event("transacoes", evento)
    return {"status": "Transação de depósito publicada no Kafka"}


@router.post("/saque")
async def saque(numero_conta: int, valor: float, db: Session = Depends(get_db)):
    conta_repo = ContaRepository(db)
    conta = await conta_repo.get_conta(numero_conta)
    if conta is None:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    # Criar evento de saque
    transacao_repo = TransacaoRepository(db)
    transacao = await transacao_repo.abrir_transacao(TipoTransacao.TRANSFERENCIA, conta_origem=numero_conta, valor=valor)

    evento = {
        "tipo": "transferencia",
        "conta_origem": numero_conta,
        "valor": valor,
        "transacao_id": transacao.id,
    }

    from app import kafka_producer
    await kafka_producer.send_event("transacoes", evento)
    return {"status": "Transação de saque publicada no Kafka"}


@router.post("/transferencia")
async def transferencia(conta_origem: int, conta_destino: int, valor: float, db: Session = Depends(get_db)):
    conta_repo = ContaRepository(db)
    conta_origem_data = await conta_repo.get_conta(conta_origem)
    conta_destino_data = await conta_repo.get_conta(conta_destino)

    if conta_origem_data is None or conta_destino_data is None:
        raise HTTPException(status_code=404, detail="Uma ou ambas as contas não foram encontradas")

    transacao_repo = TransacaoRepository(db)
    transacao = await transacao_repo.abrir_transacao(TipoTransacao.TRANSFERENCIA, conta_origem, valor, conta_destino)

    evento = {
        "tipo": "transferencia",
        "conta_origem": conta_origem,
        "conta_destino": conta_destino,
        "valor": valor,
        "transacao_id": transacao.id,
    }

    from app import kafka_producer
    await kafka_producer.send_event("transacoes", evento)
    return {"status": "Transação de transferência publicada no Kafka"}


@router.get("/conta/{numero_conta}")
async def listar_transacoes(numero_conta: int, db: Session = Depends(get_db)):
    transacao_repo = TransacaoRepository(db)
    transacoes = await transacao_repo.get_transacoes(numero_conta)
    return transacoes
