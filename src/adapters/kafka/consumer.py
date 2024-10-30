# adapters/kafka/consumer.py

import asyncio
import json
from aiokafka import AIOKafkaConsumer
from kafka.errors import KafkaError
from settings import Settings
from src.adapters.database.repository import TransacaoRepository,  AsyncSession
from src.domain.services.transacao_service import TransacaoService
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine



settings = Settings()



async def get_db() -> AsyncSession:
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        yield session


class KafkaEventConsumer:
    def __init__(self):
        self.consumer = None  # Inicialize como None

    async def start(self):
        # Inicialize o consumidor dentro de um contexto assíncrono
        self.consumer = AIOKafkaConsumer(
            'transacoes',
            bootstrap_servers=settings.KAFKA.BOOTSTRAP_SERVERS,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            max_poll_records=100,
            group_id=1,
            session_timeout_ms=30000,  # aumenta para 30s
            heartbeat_interval_ms=10000  # aumenta para 10s
        )
        await self.consumer.start()

    async def consume_events(self):
        try:
            async for event in self.consumer:
                event_data = event.value

                try:
                    await self.process_event(event_data)
                    await self.consumer.commit()
                except Exception as e:
                    print(f"Erro ao processar evento: {e}. Offset não será atualizado para reprocessamento.")
        except KafkaError as e:
            print(f"Erro no Kafka: {e}")
        finally:
            await self.consumer.stop()
            print("Consumo de eventos encerrado.")

    async def process_event(self, event_data):
        print(f"Processando evento: {event_data}")
        async for db in get_db():
            transacao_service = TransacaoService(db)
            tipo = event_data.get("tipo")
            valor = event_data.get("valor")
            conta_origem = event_data.get("conta_origem")
            conta_destino = event_data.get("conta_destino")
            transacao_id = event_data.get("transacao_id")

            if tipo == "deposito":
                await transacao_service.depositar(conta_destino, valor, transacao_id)
            elif tipo == "saque":
                await transacao_service.sacar(conta_origem, valor, transacao_id)
            elif tipo == "transferencia":
                await transacao_service.transferir(conta_origem, conta_destino, valor, transacao_id)
            else:
                print(f"Tipo de evento desconhecido: {tipo}")
            break


kafka_consumer = KafkaEventConsumer()
