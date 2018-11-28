import argparse
import re
import unicodedata
import urllib.request as req
import MeCab
import scrapy
import json
import uuid
import app
from app import scraping
from app.lib import logger
from fastText import train_supervised, BOW

logger = logger.get_module_logger(__name__)

with open(app.get_output_unknown_file(), 'r') as f:
    df = json.load(f)

app.remove_output_fasttext_model()
app.remove_output_train_text()

with open(app.get_output_train_text(), 'w') as f:
    for data in df:
        id = str(uuid.uuid4())
        print('__label__' + id + ', ' + data['fastText'], file=f)


model = train_supervised(
    input=app.get_output_train_text(), epoch=200, lr=0.7, wordNgrams=2,
    loss="hs", dim=100
)


def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))

print_results(*model.test(app.get_output_train_text()))
model.save_model(app.get_output_fasttext_model())
