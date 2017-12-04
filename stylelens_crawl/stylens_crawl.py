import os
import json
import logging

from scrapy.crawler import CrawlerProcess
from stylelens_crawl.services.DeBow import DeBow
from stylelens_crawl.services.DoubleSixGirls import DoubleSixGirls


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
            'FEED_URI': 'out.json',
            'LOG_LEVEL': 'INFO'
        })

        if os.path.exists(os.path.join(BASE_DIR, 'out.json')):
            os.remove(os.path.join(BASE_DIR, 'out.json'))

    def start(self):

        if self.service_name == 'HC0001':
            self.process.crawl(DoubleSixGirls)
        elif self.service_name == 'HC0002':
            self.process.crawl(DeBow)
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
