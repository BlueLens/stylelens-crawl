import logging
import os
import shutil
import json

from stylelens_crawl.util.data import SpreadSheets
from scrapy.crawler import CrawlerProcess

from stylelens_crawl import BASE_DIR, PKG_DIR
from stylelens_crawl.services import DeBow, DoubleSixGirls, Imvely, Stylenanda, Cafe24, MakeShop, HANDSOME

scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREAD_SHEET_ID = '1In9_1IbEyzU-nU57WxF1JbjXTki2yHkwIJfXZRY7ZjQ'


class StylensCrawler(object):
    def __init__(self, options):
        if 'host_code' in options:
            self.service_name = options['host_code']
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        settings = {
            'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'FEED_FORMAT': 'json',
            'FEED_EXPORT_ENCODING': 'UTF-8',
            'FEED_URI': os.path.join(BASE_DIR, 'out.json'),
            'LOG_LEVEL': 'INFO'
        }

        if 'job_dir' in options:
            if options['job_dir']:
                settings['JOBDIR'] = os.path.join(BASE_DIR, 'job')

        self.process = CrawlerProcess(settings)
        self.logger.info('The file location: %s' % os.path.join(BASE_DIR, 'out.json'))

    def start(self):
        if self.service_name == 'HC0008':
            self.process.crawl(DoubleSixGirls)
        elif self.service_name == 'HC0808':
            self.process.crawl(DeBow)
        elif self.service_name == 'HC0004':
            self.process.crawl(Imvely)
        elif self.service_name == 'HC0001':
            self.process.crawl(Stylenanda)
        else:
            host_code = int(self.service_name.replace('HC', ''))
            # HANDSOME
            if 1000 < host_code < 1050:
                host = HANDSOME.get_host_with_service_name(self.service_name)
                print(host)
                self.process.crawl(HANDSOME, shopping_mall_settings=host)
            else:
                shopping_mall_list = SpreadSheets(
                    sheet_id='1In9_1IbEyzU-nU57WxF1JbjXTki2yHkwIJfXZRY7ZjQ').get_rows_with_header(
                    "'크롤링'!A9:AD3000")
                for item in shopping_mall_list:
                    if self.service_name == item['host_code']:
                        if item['platform'] == 'CAFE24':
                            self.process.crawl(Cafe24, shopping_mall_settings=item)
                            break
                        elif item['platform'] == 'MAKESHOP':
                            self.process.crawl(MakeShop, shopping_mall_settings=item)
                            break

        self.process.start()
        self.logger.info('############################### completed')

        return True

    @staticmethod
    def get_items():
        if os.path.exists(os.path.join(BASE_DIR, 'out.json')):
            with open(os.path.join(BASE_DIR, 'out.json'), 'r', encoding='UTF-8') as file:
                raw_data = json.loads(file.read())
            return raw_data
        else:
            raise RuntimeError('The result file dose not exist.')

    @staticmethod
    def delete_temp_file():
        """
        Mostly you don't need to call this function,
        if you use micro service architecture.
        :return:
        """
        if os.path.exists(BASE_DIR):
            return shutil.rmtree(BASE_DIR)
        return False
