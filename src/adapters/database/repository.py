# adapters/database/repository.py
# Lógica de acesso a dados (repositório)

from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.adapters.database.models import Conta
from src.adapters.database.models import Transacao, TipoTransacao, StatusTransacao
from src.adapters.database.base import Base
from sqlalchemy.ext.asyncio import AsyncSession


class ContaRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_conta(self, nome: str, saldo: float = 0.0) -> Conta:
        conta = Conta(nome=nome, saldo=saldo)
        self.db.add(conta)
        await self.db.commit()
        await self.db.refresh(conta)
        return conta

    async def get_conta(self, numero: int) -> Conta:
        query = select(Conta).where(Conta.numero == numero)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def update_conta(self, numero: int, nome: str) -> Conta:
        conta = await self.get_conta(numero)
        if conta:
            conta.nome = nome
            await self.db.commit()
            await self.db.refresh(conta)
        return conta


class TransacaoRepository:
    def __init__(self, db: Session):
        self.db = db

    async def abrir_transacao(self, tipo: TipoTransacao, conta_origem: int, valor: float, conta_destino: int = None) -> Transacao:
        transacao = Transacao(
            tipo=tipo,
            conta_origem=conta_origem,
            conta_destino=conta_destino,
            valor=valor,
            status=StatusTransacao.PENDENTE
        )

        self.db.add(transacao)
        await self.db.commit()
        await self.db.refresh(transacao)
        return transacao

    async def efetuar_transacao(
        self,
        tipo: TipoTransacao,
        conta_origem: int,
        valor: float,
        transacao_id: int,
        conta_destino: int = None,
    ) -> Transacao:
        if tipo == TipoTransacao.SAQUE:
            await self.atualizar_saldo(conta_origem, -valor)
        elif tipo == TipoTransacao.TRANSFERENCIA:
            await self.atualizar_saldo(conta_origem, -valor)
            await self.atualizar_saldo(conta_destino, valor)

        query = select(Transacao).where(Transacao.id == transacao_id)
        result = await self.db.execute(query)
        transacao = result.scalars().first()

        transacao.status = StatusTransacao.CONCLUIDA
        await self.db.commit()
        await self.db.refresh(transacao)
        return transacao

    async def atualizar_saldo(self, numero_conta: int, valor: float) -> None:
        query = select(Conta).where(Conta.numero == numero_conta)
        result = await self.db.execute(query)
        conta = result.scalars().first()

        if conta:
            conta.saldo += valor
            await self.db.commit()
            await self.db.refresh(conta)
        return conta

    async def get_transacoes(self, conta_numero: int):
        # query = self.db.query(Transacao).filter((Transacao.conta_origem == conta_numero) | (Transacao.conta_destino == conta_numero)).all()
        query = select(Transacao).filter((Transacao.conta_origem == conta_numero) | (Transacao.conta_destino == conta_numero))
        result = await self.db.execute(query)
        return result.scalars().all()
