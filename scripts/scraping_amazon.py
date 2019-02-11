import re

import scrapy

import app
from app import master_file
from app.lib import logger

logger = logger.get_module_logger(__name__)

# ジャンル一覧
# https://www.amazon.co.jp/gp/search/other/ref=sr_sa_p_n_theme_browse-bin?rh=n%3A2351649051%2Cp_n_ways_to_watch%3A3746328051&bbn=2351649051&sort=date-desc-rank&pickerToList=theme_browse-bin&ie=UTF8&qid=1544453307
# https://www.amazon.co.jp/gp/search/other/ref=sr_sa_p_n_theme_browse-bin?rh=n:2351649051,p_n_ways_to_watch:3746328051&bbn=2351649051&sort=date-desc-rank&pickerToList=theme_browse-bin&ie=UTF8&qid=1544453307

# https://www.amazon.co.jp/s/ref=sr_in_-2_p_n_theme_browse-bin_20?fst=as:off&rh=n:2351649051,p_n_ways_to_watch:3746328051,p_n_theme_browse-bin:4435529051&bbn=2351649051&sort=date-desc-rank&ie=UTF8&qid=1544453313&rnid=4435522051
# https://www.amazon.co.jp/s/s/ref=sr_nr_p_n_feature_twenty_b_0?fst=as:off&rh=n:2351649051,p_n_ways_to_watch:3746328051,p_n_theme_browse-bin:4435529051,p_n_feature_twenty_browse-bin:2317600051&bbn=2351649051&sort=relevancerank&ie=UTF8&qid=1544453540&rnid=2317599051


class BlogSpider(scrapy.Spider):
    name = 'blogspider'

    pattern = re.compile(r'[^/]+(?=/$|$)')
    title_pattern = re.compile(r'(.*)[（(][^)）]*[)）]$')

    custom_settings = {
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_EXPIRATION_SECS': 0,
        'HTTPCACHE_DIR': 'httpcache',
        'HTTPCACHE_IGNORE_HTTP_CODES': [],
        'HTTPCACHE_STORAGE': ('scrapy.extensions.httpcache'
                              '.FilesystemCacheStorage')
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

        title = app.sanitize(response.css(
            '.animeDetailCommonHeadTitle > h2 > a::text')
            .extract_first()[1:-1])
        result = BlogSpider.title_pattern.search(title)
        if result:
            title = result.group(0)

        value = {
            'title': title,
            'story': app.sanitize(response.css('blockquote::text')
                                  .extract_first())
        }

        logger.info(value)
        # Masterファイルを読み込み（シングルトン）
        master = master_file.MasterFile()
        master.append('anikore', key, value)
