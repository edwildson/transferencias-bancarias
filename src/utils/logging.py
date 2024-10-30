import contextvars
import logging
import uuid
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import colorlog
from settings import settings

unique_request_id = contextvars.ContextVar('unique_request_id', default=None)

logging.getLogger('watchfiles').setLevel(logging.WARNING)


def set_context_request_id() -> str:
    context_request_id = str(uuid.uuid4())
    unique_request_id.set(context_request_id)
    return context_request_id


class LoggerFormatter(colorlog.ColoredFormatter):
    def format(self, record: logging.LogRecord) -> str:
        current_request_id = unique_request_id.get()
        if current_request_id:
            return f'({current_request_id}) {super().format(record)}'
        return super().format(record)


def init_logger():
    logging_level = settings.LOGGING_LEVEL
    color_formatter = LoggerFormatter(
        '%(asctime)s %(log_color)s[%(name)s %(levelname)-8s] %(reset)s %(message)s',
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
            'API_COMMUNICATION': 'blue',
            'INITIALIZATION': 'purple',
        },
        secondary_log_colors={},
        style='%'
    )

    # Define novos níveis de log
    API_COMMUNICATION = 15
    logging.addLevelName(API_COMMUNICATION, "API_COMMUNICATION")

    def api(self, message):
        if self.isEnabledFor(API_COMMUNICATION):
            self._log(API_COMMUNICATION, message, args=[])
    logging.Logger.api = api

    INITIALIZATION_LOG_LEVEL = 9
    logging.addLevelName(INITIALIZATION_LOG_LEVEL, "INITIALIZATION")

    def initialization(self, message):
        if self.isEnabledFor(INITIALIZATION_LOG_LEVEL):
            self._log(INITIALIZATION_LOG_LEVEL, message, args=[])
    logging.Logger.initialization = initialization

    # Cria um manipulador de console com coloração
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    console_handler.setFormatter(color_formatter)

    # Configura o logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(logging_level)
    root_logger.handlers = []  # Remove handlers existentes
    root_logger.addHandler(console_handler)

    # Cria um manipulador de arquivo com rotação de tempo
    if settings.LOGGING_FILE == True:
        Path('logs').mkdir(exist_ok=True)
        file_handler = TimedRotatingFileHandler('logs/api_log.log', when='midnight', backupCount=15)
        file_handler.setLevel(logging_level)
        file_formatter = logging.Formatter('%(asctime)s [%(name)s %(levelname)-8s] %(message)s')
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    # Configura loggers específicos para 'uvicorn' se necessário
    for logger_name in ["uvicorn.error", "uvicorn.access"]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging_level)
        logger.handlers = []  # Remove handlers existentes
        logger.addHandler(console_handler)

    return root_logger


logger = init_logger()
