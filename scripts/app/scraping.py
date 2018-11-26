import argparse
import urllib.request as req
import re
import MeCab
import json
import scrapy
import codecs
import uuid
from .lib import logger

logger = logger.get_module_logger(__name__)

df = {}


def load():
    global df
    try:
        with codecs.open('output/test.json', 'r', "utf-8") as f:
            df = json.load(f)
            logger.info('jjjjjjjjjjjjjjjjjjjjjjjjj')
    except IOError:
        df = {}
        logger.info('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')


def parse_item(response):
    logger.info('hhhhhhhhhhhhhhhhhhhhhhhh')
    global df
    df[str(uuid.uuid4())] = response


def flush():
    with codecs.open('output/test.json', 'w', "utf-8") as f:
        json.dump(df, f, ensure_ascii=False)


def get_surfaces(row, dic_path):
    """
    文書を分かち書きし単語単位に分割
    """
    print(row)
    content = format_text(row)
    tagger = MeCab.Tagger('-Owakati -d {}'.format(dic_path))
    node = tagger.parse(content)

    str = ''
    for n in node.split('\n'):
        value = n.split('\t')[0]
        if value != "" and value != "EOS":
            str += ' ' + value
    return str


def format_text(text):
    """
    サニタイズ処理 UTF-8-MAC を UTF-8 に変換
    """
    return unicodedata.normalize('NFC', text)
