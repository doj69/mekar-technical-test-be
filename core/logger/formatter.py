import logging

from pydantic_core import ValidationError

from core.errors import ApplicationError
from core.logger.json_formater import JsonFormatter

trace_id = ""


class StructureLogFormatter(JsonFormatter):
    EXTRA_PREFIX = "extra_"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        # update the timestamp format
        log_record["severity"] = record.levelname
        trace = self._get_trace_id(record)

        if trace:
            log_record["spanId"] = trace

        self.set_extra_keys(record, log_record, self._skip_fields)

    @staticmethod
    def is_private_key(key):
        return hasattr(key, "startswith") and key.startswith("_")

    @staticmethod
    def is_extra_key(key):
        return hasattr(key, "startswith") and key.startswith(
            StructureLogFormatter.EXTRA_PREFIX
        )

    def set_extra_keys(self, record, log_record, reserved):
        """
        Add the extra data to the log record.
        prefix will be added to all custom tags.
        """
        record_items = list(record.__dict__.items())
        records_filtered_reserved = [
            item for item in record_items if item[0] not in reserved
        ]
        records_filtered_private_attr = [
            item
            for item in records_filtered_reserved
            if not StructureLogFormatter.is_private_key(item[0])
        ]
        app_err = self._handle_error(record, log_record)
        if app_err:
            log_record.update(app_err)

        for key, value in records_filtered_private_attr:
            if not StructureLogFormatter.is_extra_key(key) and isinstance(
                value, (dict, list)
            ):

                log_record[key] = value

    @staticmethod
    def _get_trace_id(record: logging.LogRecord):
        """
        The trace id can be used for tracing logs across multiple services.
        It's fetched from the headers of the request.
        Should be implemented according to the tracing mechanism of the service.
        e.g in flask or fastapi:
        trace_id = request.headers.get("X-Trace-Id")
        """
        global trace_id
        trace_id = getattr(record, "spanId", trace_id)
        return trace_id

    def _handle_error(self, record: logging.LogRecord, log_record: dict):
        json_app_error = dict()
        if (
            record.levelno == logging.ERROR
            and record.exc_info
            and isinstance(record.exc_info[1], ApplicationError)
        ):
            app_err: ApplicationError = record.exc_info[1]
            json_app_error.update(
                {
                    "application": {
                        "code": app_err.error.code,
                        "message": app_err.error.message,
                        "stackTrace": self.formatException(record.exc_info),
                    }
                }
            )
        elif (
            record.levelno == logging.ERROR
            and record.exc_info
            and isinstance(record.exc_info[1], (ValueError, ValidationError))
        ):
            json_app_error.update(
                {
                    "application": {
                        "stackTrace": self.formatException(record.exc_info),
                    }
                }
            )
        elif (
            record.levelno == logging.ERROR
            and record.exc_info
            and isinstance(record.exc_info[1], Exception)
        ):
            unknown_err: Exception = record.exc_info[1]
            json_app_error.update(
                {
                    "stack_trace": self.formatException(record.exc_info),
                    "message": unknown_err.args[0],
                    "severity": "ERROR",
                }
            )
        return json_app_error
