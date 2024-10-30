import pytest
from src.domain.models.conta import Conta


def test_depositar_valor_invalido():
    conta = Conta(123, 100.0, "Fulano")
    with pytest.raises(ValueError, match="O valor do depósito deve ser positivo."):
        conta.depositar(-50)


def test_sacar_valor_invalido():
    conta = Conta(123, 100.0, "Ciclano")
    with pytest.raises(ValueError, match="O valor do saque deve ser positivo."):
        conta.sacar(-30)


def test_sacar_saldo_insuficiente():
    conta = Conta(123, 50.0, "Beltrano")
    with pytest.raises(ValueError, match="Saldo insuficiente."):
        conta.sacar(100)


def test_depositar_sucesso():
    conta = Conta(123, 100.0, "Fulano")
    conta.depositar(50)
    assert conta.saldo == 150.0


def test_sacar_valor_sucesso():
    conta = Conta(123, 100.0, "Ciclano")
    conta.sacar(30)
    assert conta.saldo == 70.0


def test_sacar_saldo_sucesso():
    conta = Conta(123, 50.0, "Beltrano")
    conta.sacar(50)
    assert conta.saldo == 0.0
