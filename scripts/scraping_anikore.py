import argparse
import re
import unicodedata
import urllib.request as req

import MeCab
import scrapy

import app
from app import learning, master_file
from app.lib import logger
import logging

logger = logger.get_module_logger(__name__)


class BlogSpider(scrapy.Spider):
    name = 'blogspider'

    pattern = re.compile(r'[^/]+(?=/$|$)')

    custom_settings = {
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_EXPIRATION_SECS': 0,
        'HTTPCACHE_DIR': 'httpcache',
        'HTTPCACHE_IGNORE_HTTP_CODES': [],
        'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.FilesystemCacheStorage'
    }

    start_urls = ['https://www.anikore.jp/chronicle/']

    def parse(self, response):
        """
        デフォルトメソッド
        """
        for page in response.css('.chronicle_title > a'):
            logger.info(page.css('::text').extract())
            yield response.follow(page, self.parse_season)

    def parse_season(self, response):
        """
        デフォルトメソッド
        """
        for page in response.css('.subMenuListSeason > li > a'):
            logger.info(page.css('::text').extract())
            yield response.follow(page, self.parse_list)

    def parse_list(self, response):
        """
        デフォルトメソッド
        """
        # Masterファイルを読み込み（シングルトン）
        master = master_file.MasterFile()
        for page in response.css('span.animeTitle > a'):
            logger.info(*page.css('::text').extract())
            yield response.follow(page, self.parse_item)
        for page in response.css('a.next'):
            yield response.follow(page, self.parse_list)
            master.save()

    def parse_item(self, response):
        # if len(response.css('.animeDetailCommonHeadTitle > h2 > a::text').extract_first()[1:-1]) <= 3:
        #     return
        key = BlogSpider.pattern.search(response.url).group(0)
        value = {
            'title': app.sanitize(response.css('.animeDetailCommonHeadTitle > h2 > a::text').extract_first()[1:-1]),
            'story': app.sanitize(response.css('blockquote::text').extract_first())
        }

        logger.info(value)
        # Masterファイルを読み込み（シングルトン）
        master = master_file.MasterFile()
        master.append('anikore', key, value)
