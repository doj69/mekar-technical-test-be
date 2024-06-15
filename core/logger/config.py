import logging

from pydantic import BaseModel

from core.config.app import settings


# FILTER WARNINGS AND BELOW ONLY
def warnings_and_below_filter(level):
    level = getattr(logging, level)

    def filter(record):
        return record.levelno <= level

    return filter


structure_logging_formatter = "core.logger.formatter.StructureLogFormatter"
stream_class_handler = "logging.StreamHandler"
stream_ext_stdout = "ext://sys.stdout"
stream_ext_stderr = "ext://sys.stderr"


class StructureLogConfig(BaseModel):
    # STRUCTURE LOGGING CONFIG
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "stream_log_format": {
            "class": structure_logging_formatter,
            "fmt": "%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    filters: dict = {
        "warnings_and_below": {
            "()": warnings_and_below_filter,
            "level": "WARNING",
        }
    }
    handlers: dict = {
        "default_handler": {
            "formatter": "stream_log_format",
            "class": stream_class_handler,
            "stream": stream_ext_stdout,
            "filters": ["warnings_and_below"],
        },
        "default_error_handler": {
            "formatter": "stream_log_format",
            "level": "ERROR",
            "class": stream_class_handler,
            "stream": stream_ext_stderr,
        },
    }
    root: dict = {
        "handlers": [
            "default_handler",
            "default_error_handler",
        ],
        "level": settings.SEVERITY_LEVEL,
    }
