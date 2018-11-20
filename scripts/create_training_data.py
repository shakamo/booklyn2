import argparse
import urllib.request as req
import zipfile

import app
from app import test

logger = app.get_module_logger(__name__)


def download():
    logger.info(app.get_input_path())

    test.download()


if __name__ == "__main__":
    logger.info('Start')

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', default='USDJPY')
    args = parser.parse_args()

    logger.info(args)
    download()
