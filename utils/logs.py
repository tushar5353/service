
import logging
from logging.config import dictConfig
import sys

from service.utils.config import Config

config_obj = Config()
log_file_name = config_obj.get_config('environment')['log_file']
consumer_log_file_name = config_obj.get_config('environment')['consumer_log_file']

def configure_logging() -> None:
    dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': True,
            'filters': {  # correlation ID filter must be added here to make the %(correlation_id)s formatter work
                'correlation_id': {
                    '()': 'asgi_correlation_id.CorrelationIdFilter',
                    'uuid_length': 32,
                    'default_value': '-',
                },
            },
            'formatters': {
                'console': {
                    'class': 'logging.Formatter',
                    'datefmt': '%H:%M:%S',
                    # formatter decides how our console logs look, and what info is included.
                    # adding %(correlation_id)s to this format is what make correlation IDs appear in our logs
                    'format': '%(levelname)s:\t%(asctime)s %(name)s:%(lineno)d [%(correlation_id)s] [%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s',
                    "datefmt": "%Y-%m-%d %H:%M:%S"
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    # Filter must be declared in the handler, otherwise it won't be included
                    'stream': sys.stdout,
                    'filters': ['correlation_id'],
                    'formatter': 'console',
                },
                'file': {
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'level': 'INFO',
                    'formatter': 'console',
                    'filename': log_file_name,
                    'when': 'midnight',
                    'interval': 1,
                    'backupCount': 15,
                    'filters': ['correlation_id']
                },
                'file_consumer': {
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'level': 'INFO',
                    'formatter': 'console',
                    'filename': consumer_log_file_name,
                    'when': 'midnight',
                    'interval': 1,
                    'backupCount': 15,
                    'filters': ['correlation_id']
                },
            },
            # Loggers can be specified to set the log-level to log, and which handlers to use
            'loggers': {
                # project logger
                'app': {'handlers': ['file', 'console'], 'level': 'DEBUG', 'propagate': False},
                'consumer': {'handlers': ['file_consumer', 'console'], 'level': 'DEBUG', 'propagate': False},
                # third-party package loggers
                'databases': {'handlers': ['console'], 'level': 'WARNING'},
                'httpx': {'handlers': ['console'], 'level': 'INFO'},
                'asgi_correlation_id': {'handlers': ['console'], 'level': 'WARNING'},
            },
        }
    )

    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        """
        Modifying log message to replace next line with <N> to easily
        grep the logs on same line
        """
        message = ""
        record = old_factory(*args, **kwargs) # get the unmodified record
        record.msg = record.msg.replace("\n", "<N>") # change the original `lineno` attribute
        return record

    logging.setLogRecordFactory(record_factory)
