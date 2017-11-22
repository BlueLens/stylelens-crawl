import stylelens_product
import os
import json
import logging

from scrapy.crawler import CrawlerProcess
from stylelens_crawl.services.DeBow import DeBow
from stylelens_crawl.services.DoubleSixGirls import DoubleSixGirls


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# TODO : Define Logging Level


class StylensCrawler(object):
    def __init__(self, service_name):
        self.service_name = service_name
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())
        # self.logger.setLevel(logging.DEBUG)
        self.process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'FEED_FORMAT': 'json',
            'FEED_EXPORT_ENCODING': 'UTF-8',
            'FEED_URI': 'out.json',
            'LOG_LEVEL': 'INFO'
        })
        self.api_instance = stylelens_product.ProductApi()

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
        self.logger.info('############################### Ended the finding product information.')
        self.save()
        return True

    def save(self):
        target_data = []
        with open(os.path.join(BASE_DIR, 'out.json'), 'r', encoding='UTF-8') as file:
            raw_data = json.loads(file.read())
            for data in raw_data:
                if 'is_exist' not in data:
                    for sub_data in raw_data:
                        if 'is_exist' in sub_data:
                            if sub_data['product_no'] == data['product_no']:
                                if isinstance(data['tags'], list):
                                    data['tags'] = data['tags'].extend(sub_data['tags'])
                                else:
                                    if isinstance(sub_data['tags'], list):
                                        data['tags'] = sub_data['tags']
                    target_data.append(data)

        self.logger.info('Item count: %d' % len(target_data))

        for data in target_data:
            result = self.api_instance.add_product(data)
            self.logger.info(result)



