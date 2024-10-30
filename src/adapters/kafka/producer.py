# src/kafka_producer.py

import asyncio
import json
from aiokafka import AIOKafkaProducer
from settings import settings


class KafkaProducer:
    def __init__(self, loop):
        print(settings.KAFKA.BOOTSTRAP_SERVERS)
        self.producer = AIOKafkaProducer(
            loop=loop,
            bootstrap_servers=settings.KAFKA.BOOTSTRAP_SERVERS,
        )

    async def start(self):
        a = await self.producer.start()
        print(a)

    async def stop(self):
        await self.producer.stop()

    async def send_event(self, topic: str, value: dict):
        # Serializa o valor para JSON
        async with self.producer as producer:
            # await producer.send_and_wait("topic", "mensagem")
            value_json = json.dumps(value).encode('utf-8')  # Converte dict para JSON
            await producer.send_and_wait(topic, value_json)


kafka_producer = KafkaProducer
