import logging
from pathlib import Path
from typing import Any

from helper.config import Config

LOGFILE = 'simple-led.log'


class LogManager:
    """
    Example:
        from helper.log_manager import LogManager
        LOGMAN = LogManager('module_name')
        LOGMAN.info('Test')
    """
    mapping = {'debug': logging.DEBUG,
               'info': logging.INFO,
               'warning': logging.WARNING,
               'error': logging.ERROR,
               'critical': logging.CRITICAL}

    def __init__(self, module_name: str):
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s", "%Y-%m-%d %H:%M:%S")

        # stdout logging
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        # file logging
        f_handler = logging.FileHandler(LOGFILE)
        f_handler.setFormatter(formatter)

        self.logger = logging.getLogger(module_name)

        # get loglevel
        config = Config.read(Path('config.yaml'))
        log_level = (config['general']['log_level']).lower()

        self.logger.setLevel(self.mapping.get(log_level, logging.ERROR))

        # add handler for stdout and file
        self.logger.addHandler(handler)
        self.logger.addHandler(f_handler)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.critical(msg, *args, **kwargs)