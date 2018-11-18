# python fx_1_historical_data_downloader.py
# python fx_1_historical_data_downloader.py -f USDJPY -u http://tools.fxdd.com/tools/M1Data/USDJPY.zip

import argparse
import urllib.request as req
import zipfile

import app

logger = app.get_module_logger(__name__)


def download():
    logger.info(app.get_input_path())

    url='https://www.anikore.jp/chronicle/2018/autumn/'

