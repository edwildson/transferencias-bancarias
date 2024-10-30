# src/kafka_producer.py

import asyncio
import json
from aiokafka import AIOKafkaProducer
from aiokafka.errors import ProducerClosed
from settings import settings


class KafkaProducer:
    def __init__(self, loop):
        print(settings.KAFKA.BOOTSTRAP_SERVERS)
        self.loop = loop
        self.producer = AIOKafkaProducer(
            loop=loop,
            bootstrap_servers=settings.KAFKA.BOOTSTRAP_SERVERS,
            acks=1,
        )

    # async def start(self):
    #     a = await self.producer.start()
    #     print(a)
    async def start(self):
        """Inicia o produtor Kafka."""
        if not self.producer or self.producer._closed:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA.BOOTSTRAP_SERVERS,
                loop=self.loop,
                acks=1,
            )
            await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send_event(self, topic: str, value: dict):
        await self.start()

        async with self.producer as producer:
            try:
                # Verifica e inicia o produtor se ele estiver fechado
                if producer._closed:
                    await producer.start()

                value_json = json.dumps(value).encode('utf-8')  # Converte dict para JSON
                await producer.send(topic, value_json)
                # await producer.send(topic, value_json)
                await producer.stop()
            except ProducerClosed:
                print("Producer estava fechado, tentando reconectar...")
                await self.producer.stop()
                await self.producer.start()  # Tenta reiniciar o produtor
                await self.producer.send(topic, value_json)
            finally:
                await producer.stop()


kafka_producer = KafkaProducer
