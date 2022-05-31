import logging


class Log:
    def __init__(self, tag):
        self.tag = tag
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def get_logger(self):
        return logging.getLogger(self.tag)

    def error(self, message):
        log = self.get_logger()
        log.error(" {}".format(message))

    def warning(self, message):
        log = self.get_logger()
        log.warning(" {}".format(message))

    def debug(self, message):
        log = self.get_logger()
        log.debug(" {}".format(message))

    def info(self, message):
        log = self.get_logger()
        log.info(" {}".format(message))
