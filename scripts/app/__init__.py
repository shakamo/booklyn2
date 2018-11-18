import sys, os
from logging import getLogger, StreamHandler, DEBUG, Formatter
from pathlib import Path


ROOT = Path(__file__).parent.parent


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
    os.mkdir(ROOT.joinpath('input'))
    os.mkdir(ROOT.joinpath('output'))
    return ROOT.joinpath('input')


def get_output_path():
    Path.mkdir(ROOT.joinpath('output'))
    return ROOT.joinpath('output')
