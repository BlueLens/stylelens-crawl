import os
import json
import logging
import shutil

from scrapy.crawler import CrawlerProcess
from stylelens_crawl import BASE_DIR
from stylelens_crawl.util import get_shopping_information_from_csv
from stylelens_crawl.services import DeBow, DoubleSixGirls, Imvely, Stylenanda, Cafe24

class StylensCrawler(object):
    def __init__(self, options):
        if 'host_code' in options:
            self.service_name = options['host_code']
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'FEED_FORMAT': 'json',
            'FEED_EXPORT_ENCODING': 'UTF-8',
            'FEED_URI': os.path.join(BASE_DIR, 'out.json'),
            'LOG_LEVEL': 'INFO'
        })
        self.logger.info('The file location: %s' % os.path.join(BASE_DIR, 'out.json'))

    def start(self):

        # TODO : Change to Dictionary Type
        if self.service_name == 'HC0001':
            self.process.crawl(DoubleSixGirls)
        elif self.service_name == 'HC0002':
            self.process.crawl(DeBow)
        elif self.service_name == 'HC0003':
            self.process.crawl(Imvely)
        elif self.service_name == 'HC0004':
            self.process.crawl(Stylenanda)
        else:
            item = get_shopping_information_from_csv(self.service_name)
            if item:
                if item[1] == 'CAFE24':
                    self.process.crawl(Cafe24, shopping_mall_settings=item)
                else:
                    return False

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
