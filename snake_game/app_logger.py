import logging

_log_format = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
_log_file_name = "log.log"


def get_file_handler(level):
    file_handler = logging.FileHandler(_log_file_name)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler(level):
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(
    name,
    log_in_file=False,
    log_in_console=True,
    level=logging.DEBUG,
):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if log_in_file:
        logger.addHandler(get_file_handler(level))
    if log_in_console:
        logger.addHandler(get_stream_handler(level))
    return logger
