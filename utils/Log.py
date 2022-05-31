import logging
import os

from utils.constants import LOGGER_FORMAT, LOGS_DIR


class Log:
    def __init__(self, tag):
        self.tag = tag

        logging.basicConfig(
            level=logging.NOTSET,
            format=LOGGER_FORMAT
        )

        self.create_logs_dir()
        self.setup_logger()

    @staticmethod
    def create_logs_dir():
        if not os.path.exists(LOGS_DIR):
            os.makedirs(LOGS_DIR)

    def setup_logger(self):
        logger = logging.getLogger(self.tag)
        file_handler = logging.FileHandler("{0}/{1}.log".format(LOGS_DIR, self.tag))
        file_handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
        logger.addHandler(file_handler)

    def get_logger(self):
        return logging.getLogger(self.tag)

    def error(self, message):
        log = self.get_logger()
        log.error(message)

    def warning(self, message):
        log = self.get_logger()
        log.warning(message)

    def debug(self, message):
        log = self.get_logger()
        log.debug(message)

    def info(self, message):
        log = self.get_logger()
        log.info(message)

    def critical(self, message):
        log = self.get_logger()
        log.critical(message)
