import argparse
import re
import unicodedata
import urllib.request as req

import MeCab
import scrapy

import app
from app import scraping
from app.lib import logger

logger = logger.get_module_logger(__name__)


class BlogSpider(scrapy.Spider):
    name = 'blogspider'

    custom_settings = {
        'FEED_FORMAT': 'jsonlines',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_URI': 'output/scraped.json',
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_EXPIRATION_SECS': 0,
        'HTTPCACHE_DIR': 'httpcache',
        'HTTPCACHE_IGNORE_HTTP_CODES': [],
        'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.FilesystemCacheStorage'
    }

    start_urls = ['https://www.anikore.jp/chronicle/2018/autumn/']

    def parse(self, response):
        """
        デフォルトメソッド
        """
        for page in response.css('span.animeTitle > a'):
            yield response.follow(page, scraping.parse_item)
