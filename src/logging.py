import logging
import logging.config as logging_config

class CustomFormatter(logging.Formatter):
    green = "\x1b[32;20m"
    bold_green = "\x1b[32;1m"
    grey = "\x1b[38;20m"
    bold_dark_grey = "\x1b[30;1m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    light_blue = "\x1b[34;20m"
    reset = "\x1b[0m"
    
    time = grey +  "[" + reset + bold_dark_grey + "%(asctime)s.%(msecs)03d" + reset + grey + "]" + reset
    process = grey +  "[%(process)s] [" + bold_green + "%(processName)s" + reset + "-" + green + "(%(threadName)s)" + reset + grey + "]" + reset
    level = "[%(levelname)s] "
    message = "%(message)s"

    FORMATS = {
        logging.DEBUG:      time + " " + process + grey + " [" + grey + "%(levelname)s" + reset + grey + "] " + bold_dark_grey + message  + reset,
        logging.INFO:       time + " " + process + grey + " [" + light_blue + "%(levelname)s" + reset + grey + "] " + bold_dark_grey + message  + reset,
        logging.WARNING:    time + " " + process + grey + " [" + yellow + "%(levelname)s" + reset +  grey +"] " + yellow + message  + reset,
        logging.ERROR:      time + " " + process + grey + " [" + red + "%(levelname)s" + reset +  grey +"] " + red + message  + reset,
        logging.CRITICAL:   time + " " + process + grey + " [" + bold_red + "%(levelname)s" + reset +  grey +"] " + bold_red + message  + reset,
    }


    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %z %H:%M:%S")
        return formatter.format(record)

LOGGING_CONFIG = { 
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": { 
        "standard": { 
            "format": "%(asctime)s.%(msecs)03d [%(processName)s-(%(threadName)s)] [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %z %H:%M:%S"
        },
        "console": {
            "()": CustomFormatter
        }
    },
    "handlers": { 
        "console": { 
            "level": "INFO",
            "formatter": "console",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        }
    },
    "loggers": { 
        "default": {  # root logger
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False
        }
    } 
}

class Logger:
    
    def __init__(self, *, folder: str=None, debug: bool=False) -> None:
        config = LOGGING_CONFIG
        if isinstance(folder, str):
            config["handlers"]["file"] = {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "standard",
                "filename": "{}/logs.log".format(folder),
                "maxBytes": 50000,
                "backupCount": 3
            }
            config["loggers"]["default"]["handlers"].append("file")
        
        if isinstance(debug, bool) and debug == True:
            config["handlers"]["console"]["level"] = "DEBUG"
        
        logging_config.dictConfig(config)
        self._logger = logging.getLogger("default")
        
    def info(self, message: str) -> None:
        self._logger.info(message)
    
    def debug(self, message: str) -> None:
        self._logger.debug(message)
    
    def warning(self, message: str) -> None:
        self._logger.warning(message)
    
    def error(self, message: str) -> None:
        self._logger.error(message)
    
    def critical(self, message: str) -> None:
        self._logger.critical(message)
    
    def exception(self, message: str) -> None:
        self._logger.exception(message)
