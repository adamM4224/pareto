import logging
import logging.config

config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "formatter1": {
            "format": "%(message)s"
        },
        "formatter2": {
            "format": "%(message)s"
        }
    },
    "handlers": {
        "fileHandler1": {
            "class": "logging.FileHandler",
            "formatter": "formatter1",
            "filename": "logs/pareto.log",
            "level": "INFO",
            "mode": "w",
        },
        "fileHandler2": {
            "class": "logging.FileHandler",
            "formatter": "formatter2",
            "filename": "logs/gridLog.log",
            "level": "INFO",
            "mode": "w",
        }
    },
    "loggers": {
        "paretoLogger": {
            "handlers": ["fileHandler1"],
            "level": "INFO",
            "propagate": False,
        },
        "gridLogger": {
            "handlers": ["fileHandler2"],
            "level": "INFO",
            "propagate": False,
        }
    },
}


logging.config.dictConfig(config)

def getLogger(name):
    if name not in ['paretoLogger', 'gridLogger']:
        raise ValueError(f'{name} is not a valid logger')
    return logging.getLogger(name)