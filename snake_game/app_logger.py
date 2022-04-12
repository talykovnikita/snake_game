import logging

_log_format = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
_log_level = logging.DEBUG
_log_file_name = "log.log"


def get_file_handler():
    file_handler = logging.FileHandler(_log_file_name)
    file_handler.setLevel(_log_level)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(_log_level)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(_log_level)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger
