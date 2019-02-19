import re
import sys
import scrapy
import backtrace
import app
from app import master_file
from app.lib import logger
from scrapy.utils.response import open_in_browser

logger = logger.get_module_logger(__name__)

backtrace.hook(
    reverse=True,         # 逆順
    strip_path=True    # ファイル名のみ
)

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
    title_pattern = re.compile(r'[\s]*(.*)[.|:][\s]*(.*)')
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
        'ROBOTSTXT_OBEY': True,
        'LOG_LEVEL': 'INFO'
    }

    start_urls = ['https://www.amazon.co.jp/gp/search/other/ref=sr_sa_p_n_theme_browse-bin?rh=n%3A2351649051%2Cp_n_ways_to_watch%3A3746328051&bbn=2351649051&sort=date-desc-rank&pickerToList=theme_browse-bin&ie=UTF8&qid=1544453307']

    def parse(self, response):
        """
        デフォルトメソッド
        """
        for page in response.css('.a-list-item > a.a-link-normal'):
            # logger.info(page.css('::text').extract_first())
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
            # logger.info(*page.css('::text').extract())
            yield response.follow(page, self.parse_item)
        for page in response.css('#pagnNextLink'):
            yield response.follow(page, self.parse_list)
            master.save()

    def parse_item(self, response):
        try:
            key = BlogSpider.pattern.search(response.url).group(1)

            episodes = {}
            for html in response.css('.dv-episode-container'):
                self.parse_episode(episodes, html)

            value = {
                'title': app.sanitize(response.css(
                    'section > h1::text')
                    .extract_first()),
                'story': app.sanitize(response.css('div.av-synopsis.avu-full-width > p::text')
                                      .extract_first()),
                'year': app.sanitize(response.css('[data-automation-id="release-year-badge"]::text')
                                     .extract_first()),
                'episodes': episodes
            }

            # Masterファイルを読み込み（シングルトン）
            master = master_file.MasterFile()
            master.append('amazon', key, value)

            self.check_format(key, value)
        except TypeError as error:
            logger.error(str(error) + ' ' + response.url + ' ')
            tpe, v, tb = sys.exc_info()
            backtrace.hook(reverse=True, strip_path=True,
                           tb=tb, tpe=tpe, value=v)
            open_in_browser(response)
            pass

    def parse_episode(self, episodes, html):
        try:
            index = BlogSpider.title_pattern.search(html.css(
                '.dv-el-title::text').extract()[1]).group(1)
        except (TypeError, AttributeError) as error:
            logger.error(str(error) + ' ' +
                         str(html.css('.dv-el-title::text').extract()))
            raise

        title = BlogSpider.title_pattern.search(html.css(
            '.dv-el-title::text').extract()[1]).group(2)

        status = ''
        if html.css('.dv-el-prime').extract_first():
            status = 'Prime'
        elif html.css('.dv-el-status-text::text').extract_first():
            status = BlogSpider.status.search(
                html.css('.dv-el-status-text::text').extract_first())
            if status.group(1):
                status = status.group(1)
            else:
                status = ''
        elif html.css('.a-size-base.dv-el-3psub.a-text-normal::text').extract_first():
            status = html.css(
                '.a-size-base.dv-el-3psub.a-text-normal::text').extract_first()

        episodes[index] = {
            'title': app.sanitize(title),
            'story': app.sanitize(html.css(
                'p.a-text-normal::text')
                .extract_first()),
            'data-aliases': app.sanitize(html.css(
                '::attr(data-aliases)')
                .extract_first()),
            'status': app.sanitize(status)
        }

    def check_format(self, key, value):
        if not key  \
                or not value['title'] \
                or not value['story'] \
                or not value['year']:
            logger.info('incomplete content' + key + ' ' + str(value))

        for num in value['episodes']:
            if not value['episodes'][num]['title']  \
                    or not value['episodes'][num]['story'] \
                    or not value['episodes'][num]['status']:
                logger.info('incomplete episode ' + key +
                            ' ' + str(value['episodes'][num]))
