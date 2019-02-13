import re

import scrapy

import app
from app import master_file
from app.lib import logger

logger = logger.get_module_logger(__name__)

# ジャンル一覧（取り方が２つあるが同じもの）
# https://www.amazon.co.jp/gp/search/other/ref=sr_sa_p_n_theme_browse-bin?rh=n%3A2351649051%2Cp_n_ways_to_watch%3A3746328051&bbn=2351649051&sort=date-desc-rank&pickerToList=theme_browse-bin&ie=UTF8&qid=1544453307
# https://www.amazon.co.jp/gp/search/other/ref=sr_sa_p_n_theme_browse-bin?rh=n:2351649051,p_n_ways_to_watch:3746328051&bbn=2351649051&sort=date-desc-rank&pickerToList=theme_browse-bin&ie=UTF8&qid=1544453307

# 16 * 400 = 6400

# ジャンル：アニメ
# https://www.amazon.co.jp/s/ref=sr_in_-2_p_n_theme_browse-bin_2?fst=as%3Aoff&rh=n%3A2351649051%2Cp_n_ways_to_watch%3A3746328051%2Cp_n_theme_browse-bin%3A4435524051&bbn=2351649051&sort=date-desc-rank&ie=UTF8&qid=1549894109&rnid=4435522051

# https://www.amazon.co.jp/dp/B07MWDNS4R


class BlogSpider(scrapy.Spider):
    name = 'blogspider'

    pattern = re.compile(r'[¥/]dp[¥/](.{10})')
    title_pattern = re.compile(r'[\s]*([0-9]{1,3})[.][\s]*(.*)')
    status = re.compile(r'[\s]*(.*)[\s]*')

    custom_settings = {
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_EXPIRATION_SECS': 0,
        'HTTPCACHE_DIR': 'httpcache',
        'HTTPCACHE_IGNORE_HTTP_CODES': [503, 404, 400, 401, 500],
        'HTTPCACHE_STORAGE': ('scrapy.extensions.httpcache'
                              '.FilesystemCacheStorage'),
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY': 3,
        'ROBOTSTXT_OBEY': True
    }

    start_urls = ['https://www.amazon.co.jp/gp/search/other/ref=sr_sa_p_n_theme_browse-bin?rh=n%3A2351649051%2Cp_n_ways_to_watch%3A3746328051&bbn=2351649051&sort=date-desc-rank&pickerToList=theme_browse-bin&ie=UTF8&qid=1544453307']

    def parse(self, response):
        """
        デフォルトメソッド
        """
        for page in response.css('.a-list-item > a.a-link-normal'):
            logger.info(page.css('::text').extract_first())
            if page.css('::text').extract_first() != 'アニメ' \
                    and page.css('::text').extract_first() != 'ドラマ':
                continue
            yield response.follow(page, self.parse_list)

    def parse_list(self, response):
        """
        デフォルトメソッド
        """
        # Masterファイルを読み込み（シングルトン）
        master = master_file.MasterFile()
        for page in response.css('div.a-row.a-spacing-small > div > a'):
            logger.info(*page.css('::text').extract())
            yield response.follow(page, self.parse_item)
        for page in response.css('#pagnNextLink'):
            yield response.follow(page, self.parse_list)
            master.save()

    def parse_item(self, response):
        key = BlogSpider.pattern.search(response.url).group(1)

        episodes = {}
        for html in response.css('.dv-episode-container'):
            yield self.parse_episode(episodes, html)

        value = {
            'title': app.sanitize(response.css(
                'section > h1::text')
                .extract_first()),
            'story': app.sanitize(response.css('div.av-synopsis.avu-full-width > p::text')
                                  .extract_first()),
            'release-year-badge': app.sanitize(response.css('[data-automation-id="release-year-badge"]::text')
                                               .extract_first()),
            'episodes': episodes
        }

        # Masterファイルを読み込み（シングルトン）
        master = master_file.MasterFile()
        master.append('amazon', key, value)

    def parse_episode(self, episodes, html):
        index = BlogSpider.title_pattern.search(html.css(
            '.dv-el-title::text').extract()[1]).group(1)
        title = BlogSpider.title_pattern.search(html.css(
            '.dv-el-title::text').extract()[1]).group(2)

        status = ''
        if html.css('.dv-el-status-text::text').extract_first() is not None:
            status = BlogSpider.status.search(
                html.css('.dv-el-status-text::text').extract_first())
            if status.group(1) is not None:
                status = status.group(1)
            else:
                status = ''

        episodes[index] = {
            'title': app.sanitize(title),
            'story': app.sanitize(html.css(
                'p.a-text-normal::text')
                .extract_first()),
            'data-aliases': app.sanitize(html.css(
                '.dv-episode-container::attr(data-aliases)')
                .extract_first()),
            'status': app.sanitize(status)
        }
