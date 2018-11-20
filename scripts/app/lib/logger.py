from logging import getLogger, StreamHandler, DEBUG, Formatter


def get_module_logger(module_name):
    logger = getLogger(module_name)
    handler = StreamHandler()
    formatter = Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')

    handler.setFormatter(formatter)
    handler.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.setLevel(DEBUG)
    return logger
