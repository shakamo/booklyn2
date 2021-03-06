from logging import getLogger, Formatter, INFO
import logging


def get_module_logger(module_name):
    logger = getLogger(module_name)

    handler = logging.FileHandler(filename="output/app.log")
    formatter = Formatter('%(asctime)s %(levelname)s %(name)s %(funcName)s %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(INFO)
    logger.addHandler(handler)

    logger.setLevel(INFO)

    return logger
