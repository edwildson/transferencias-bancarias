# src/domain/models/conta.py


class Conta:
    def __init__(self, numero: int, saldo: float, nome=str):
        self.numero = numero
        self.saldo = saldo
        self.nome = nome

    def depositar(self, valor: float):
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")
        self.saldo += valor

    def sacar(self, valor: float):
        if valor <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")
        self.saldo -= valor
