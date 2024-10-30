# src/domain/services/conta_service.py

from src.domain.models.conta import Conta
from src.adapters.database.repository import ContaRepository


class ContaService:
    def __init__(self, repository: ContaRepository):
        self.repository = repository

    async def criar_conta(self, numero: int, saldo_inicial: float):
        if saldo_inicial < 0:
            raise ValueError("O saldo inicial não pode ser menor que 0.")
        conta = Conta(numero, saldo_inicial)
        await self.repository.create(conta)

    async def depositar(self, numero: int, valor: float):
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser maior que 0.")
        conta = await self.repository.get_by_numero(numero)
        conta.depositar(valor)
        await self.repository.update(conta)

    async def sacar(self, numero: int, valor: float):
        if valor <= 0:
            raise ValueError("O valor do saque deve ser maior que 0.")
        conta = await self.repository.get_by_numero(numero)
        conta.sacar(valor)
        await self.repository.update(conta)
