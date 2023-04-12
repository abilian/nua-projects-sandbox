import logging
import sys

from flask import Flask
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


def configure_loguru(app: Flask):
    # register loguru as (sole) handler
    # level = app.config.get('LOG_LEVEL', 'INFO')
    if app.debug:
        level = "INFO"
    else:
        level = "SUCCESS"
    logger.remove(0)
    logger.add(sys.stderr, level=level)

    app.logger.handlers = []
    app.logger.addHandler(InterceptHandler())
