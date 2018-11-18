import sys, os
from logging import getLogger, StreamHandler, DEBUG, Formatter
from pathlib import Path



ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))


def get_module_logger(module_name):
    logger = getLogger(module_name)
    handler = StreamHandler()
    formatter = Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')

    handler.setFormatter(formatter)
    handler.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.setLevel(DEBUG)
    return logger


def get_input_path():
    os.makedirs(ROOT.joinpath('input'), exist_ok=True)
    return ROOT.joinpath('input')


def get_output_path():
    os.makedirs(ROOT.joinpath('output'), exist_ok=True)
    return ROOT.joinpath('output')
