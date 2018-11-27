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


class AnikoreScraping:
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
