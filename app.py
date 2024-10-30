# Ponto de entrada da aplicação
import fastapi
import fastapi.middleware
import fastapi.middleware.cors
from fastapi.responses import JSONResponse


from src.adapters.database.models import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# routes
from src.adapters.http.router_transacoes import router as router_transacoes
from src.adapters.http.router_conta import router as router_conta

import uvicorn
# Importe o kafka_producer
from src.adapters.kafka.producer import kafka_producer
from src.adapters.kafka.consumer import kafka_consumer
import asyncio

from settings import settings

from src.utils.logging import logger, set_context_request_id

log = logger.getChild(__name__)
log.setLevel('DEBUG')

loop = asyncio.get_event_loop()
kafka_producer = kafka_producer(loop)

consumer_task = None
# Configurações do banco de dados
DATABASE_URL = settings.DATABASE_URL


# Criação da tabela no banco de dados
# Create a session maker
async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


# Função para criar tabelas
async def create_tables():
    async with async_engine.begin() as conn:
        # Cria as tabelas
        await conn.run_sync(Base.metadata.create_all)


app = fastapi.FastAPI(
    title='Banco PRIMO test',
    description='Serviço de Integração',
    openapi_url='/docs/openapi.json',
)

app.include_router(router_conta)
app.include_router(router_transacoes)


app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=settings.SERVER.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_middleware(request, call_next):
    set_context_request_id()
    try:
        return await call_next(request)
    except Exception as exc:
        status_code = 500
        if isinstance(exc, fastapi.exceptions.HTTPException):
            status_code = exc.status_code

        return fastapi.responses.JSONResponse(
            status_code=status_code,
            content={
                'exc': repr(exc),
                'detail': str(exc.args),
            }
        )


@app.exception_handler(422)
async def handle_422(request, exc):
    return JSONResponse(status_code=422, content={
        'exc': repr(exc),
        'detail': str(exc.args),
    })


@app.exception_handler(403)
async def handle_403(request, exc):
    return JSONResponse(status_code=403, content={
        'exc': repr(exc),
        'detail': str(exc.args),
    })


@app.on_event("startup")
async def startup_event():
    global consumer_task
    await create_tables()
    await kafka_producer.start()
    global consumer_task
    await kafka_consumer.start()  # Inicializa o consumidor dentro de um contexto assíncrono
    consumer_task = asyncio.create_task(kafka_consumer.consume_events())


@app.on_event("shutdown")
async def shutdown_event():
    await kafka_producer.stop()
    if kafka_consumer.consumer:
        await kafka_consumer.consumer.stop()
    if consumer_task:
        consumer_task.cancel()  # Cancela a tarefa de consumo de eventos


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, host='0.0.0.0',
                port=8000, log_level='debug', access_log=True)
