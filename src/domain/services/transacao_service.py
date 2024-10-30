# src/domain/services/transacao_service.py

from fastapi import Depends
from src.adapters.database.repository import TransacaoRepository, ContaRepository
from src.adapters.database.models import TipoTransacao
from sqlalchemy.orm import Session


class TransacaoService:
    def __init__(self, db: Session):
        self.transacao_repo = TransacaoRepository(db)
        self.conta_repo = ContaRepository(db)

    async def depositar(self, numero_conta, valor, transacao_id):
        """Processa um depósito na conta especificada."""
        if valor <= 0:
            raise ValueError("O valor deve ser maior que 0.")

        await self.transacao_repo.atualizar_saldo(numero_conta, valor)
        return await self.transacao_repo.efetuar_transacao(TipoTransacao.DEPOSITO, numero_conta, valor, transacao_id)

    async def sacar(self, numero_conta, valor, transacao_id):
        """Processa um saque da conta especificada."""
        if valor <= 0:
            raise ValueError("O valor deve ser maior que 0.")

        conta = await self.conta_repo.get_conta(numero_conta)

        if conta.saldo < valor:
            raise ValueError("Saldo insuficiente para realizar o saque.")

        return await self.transacao_repo.efetuar_transacao(TipoTransacao.SAQUE, conta.numero, valor, transacao_id)

    async def transferir(self, conta_origem, conta_destino, valor, transacao_id):
        """Processa uma transferência entre as contas especificadas."""
        if valor <= 0:
            raise ValueError("O valor deve ser maior que 0.")

        conta = await self.conta_repo.get_conta(conta_origem)

        if conta.saldo < valor:
            raise ValueError("Saldo insuficiente para realizar a transferência.")

        # Cria a transação de transferência
        return await self.transacao_repo.efetuar_transacao(
            TipoTransacao.TRANSFERENCIA,
            conta_origem=conta_origem,
            valor=valor,
            conta_destino=conta_destino,
            transacao_id=transacao_id
        )
