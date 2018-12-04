import argparse
import re
import unicodedata
import urllib.request as req
import MeCab
import scrapy
import json
import uuid
import app
from app.lib import logger
from fastText import train_supervised, BOW
from . import master_file
from . import traning_file
import threading

logger = logger.get_module_logger(__name__)


def learn(uuid, wakati):
    # Masterファイルを読み込み（シングルトン）
    master = master_file.MasterFile()
    traning = traning_file.TraningFile()

    values = list()
    traning.append('__label__' + uuid + ' , ' + wakati)

    model = train_supervised(
        input=app.get_output_train_text(), epoch=25, lr=1.0, wordNgrams=2, verbose=2, minCount=1)

    print_results(*model.test(app.get_output_train_text()))
    model.save_model(app.get_output_fasttext_model())


def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))
