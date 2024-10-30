# adapters/database/models.py
# Modelos do banco de dados (SQLAlchemy)

import enum
from sqlalchemy import Column, Integer, Float, Enum, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from src.adapters.database.base import Base
from datetime import datetime


class Conta(Base):
    __tablename__ = 'contas'

    numero = Column(Integer, primary_key=True, index=True, autoincrement=True)
    saldo = Column(Float, default=0.0)
    nome = Column(String)
    blocked_by = Column(Integer, ForeignKey('transacoes.id'), nullable=True)

    def __repr__(self):
        return f"<Conta(nome={self.nome}, numero={self.numero}, saldo={self.saldo})>"


class TipoTransacao(str, enum.Enum):
    DEPOSITO = "deposito"
    SAQUE = "saque"
    TRANSFERENCIA = "transferencia"


class StatusTransacao(str, enum.Enum):
    PENDENTE = "pendente"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"


class Transacao(Base):
    __tablename__ = 'transacoes'

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoTransacao))
    conta_origem = Column(Integer, ForeignKey('contas.numero'))
    conta_destino = Column(Integer, ForeignKey('contas.numero'), nullable=True)
    valor = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    conta_origem_rel = relationship("Conta", foreign_keys=[conta_origem])
    conta_destino_rel = relationship("Conta", foreign_keys=[conta_destino])

    status = Column(String, default="pendente")

    def __repr__(self):
        return f"<Transacao(id={self.id}, tipo={self.tipo}, valor={self.valor}, timestamp={self.timestamp})>"
