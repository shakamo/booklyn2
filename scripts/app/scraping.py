import argparse
import urllib.request as req
import re
import MeCab

import unicodedata
import scrapy

from .lib import logger

logger = logger.get_module_logger(__name__)


def parse_item(response):
    yield {
        'title': format_text(response.css('.animeDetailCommonHeadTitle > h2 > a::text').extract_first()[1:-1]),
        'fastText': get_surfaces(response.css('.animeDetailCommonHeadTitle > h2 > a::text').extract_first()[1:-1]),
        'story': response.css('blockquote::text').extract_first()
    }


def get_surfaces(row):
    """
    文書を分かち書きし単語単位に分割
    """
    print(row)
    content = format_text(row)
    tagger = MeCab.Tagger('')
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
