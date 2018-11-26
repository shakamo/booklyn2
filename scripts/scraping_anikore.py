import argparse
import re
import unicodedata
import urllib.request as req

import fastText as ft
import MeCab
import scrapy

import app
from app import scraping
from app.lib import logger

logger = logger.get_module_logger(__name__)


class BlogSpider(scrapy.Spider):
    name = 'blogspider'

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_URI': 'output/unknown.json',
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_EXPIRATION_SECS': 0,
        'HTTPCACHE_DIR': 'httpcache',
        'HTTPCACHE_IGNORE_HTTP_CODES': [],
        'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.FilesystemCacheStorage'
    }

    if app.exists_output_fasttext_model():
        classifier = ft.load_model(app.get_output_fasttext_model())

    start_urls = ['https://www.anikore.jp/chronicle/']

    def parse(self, response):
        """
        デフォルトメソッド
        """
        for page in response.css('.chronicle_title > a'):
            yield response.follow(page, self.parse_season)

    def parse_season(self, response):
        """
        デフォルトメソッド
        """
        for page in response.css('.subMenuListSeason > li > a'):
            yield response.follow(page, self.parse_list)

    def parse_list(self, response):
        """
        デフォルトメソッド
        """
        for page in response.css('span.animeTitle > a'):
            yield response.follow(page, self.parse_item)
        for page in response.css('a.next'):
            yield response.follow(page, self.parse_list)

    def parse_item(self, response):
        if app.exists_output_fasttext_model():
            result = self.classifier.predict(self.get_surfaces(response.css('.animeDetailCommonHeadTitle > h2 > a::text').extract_first()[1:-1]))
            print()
            print(result)
            print(self.format_text(response.css('.animeDetailCommonHeadTitle > h2 > a::text').extract_first()[1:-1]))
            print(self.get_surfaces(response.css('.animeDetailCommonHeadTitle > h2 > a::text').extract_first()[1:-1]))
            print()
            print()
        yield {
            'title': self.format_text(response.css('.animeDetailCommonHeadTitle > h2 > a::text').extract_first()[1:-1]),
            'fastText': self.get_surfaces(response.css('.animeDetailCommonHeadTitle > h2 > a::text').extract_first()[1:-1]),
            'story': response.css('blockquote::text').extract_first()
        }

    def get_surfaces(self, row):
        """
        文書を分かち書きし単語単位に分割
        """
        print(row)
        content = self.format_text(row)
        tagger = MeCab.Tagger(
            '-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        return tagger.parse(content).replace(' \n', '')

    def format_text(self, text):
        """
        サニタイズ処理 UTF-8-MAC を UTF-8 に変換
        """
        return unicodedata.normalize('NFC', text)
