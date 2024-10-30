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


# Dependência para obter a sessão do banco de dados
async def get_db() -> AsyncSession:
    # Cria o motor assíncrono
    engine = create_async_engine(settings.DATABASE_URL, echo=True)

    # Cria uma fábrica de sessões assíncronas
    AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:  # Usando async with para garantir a sessão
        yield session  # Retorna a sessão para ser usada


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
            group_id='primo',
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

            if tipo == "deposito":
                await transacao_service.depositar(conta_destino, valor)
            elif tipo == "saque":
                await transacao_service.sacar(conta_origem, valor)
            elif tipo == "transferencia":
                await transacao_service.transferir(conta_origem, conta_destino, valor)
            else:
                print(f"Tipo de evento desconhecido: {tipo}")
            break


kafka_consumer = KafkaEventConsumer()
