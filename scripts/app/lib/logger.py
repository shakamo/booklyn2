from logging import getLogger, StreamHandler, DEBUG, Formatter, INFO
import logging


def get_module_logger(module_name):
    logger = getLogger(module_name)

    handler = logging.FileHandler(filename="test.log")  #handler2はファイル出力
    formatter = Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(INFO)
    logger.addHandler(handler)

    logger.setLevel(INFO)

    return logger
