from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ServerSettings(BaseModel):
    DESCRIPTION: Optional[str] = 'Homologação'
    PROTOCOL: Optional[str] = 'https'
    DOMAIN: Optional[str] = 'api.bancoprimo.test'
    ALLOW_ORIGINS: Optional[List[str]] = [
        'http://127.0.0.1:8000',
        'http://localhost:8000/',
        'http://localhost',
    ]


class KAFKA(BaseModel):
    BOOTSTRAP_SERVERS: Optional[str] = 'kafka:9092'
