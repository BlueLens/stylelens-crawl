import json
import logging
import os
import shutil

from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from scrapy.crawler import CrawlerProcess

from stylelens_crawl import BASE_DIR, PKG_DIR
from stylelens_crawl.services import DeBow, DoubleSixGirls, Imvely, Stylenanda, Cafe24

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
            if os.path.exists('/tmp/gdoc_certi.json'):
                path = '/tmp/gdoc_certi.json'
            elif os.path.exists(os.path.join(PKG_DIR, 'cred/f3c4bf11ae96.json')):
                path = os.path.join(PKG_DIR, 'cred/f3c4bf11ae96.json')
            else:
                return False

            credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
            service = discovery.build('sheets', 'v4', credentials=credentials)

            result = service.spreadsheets().values().get(spreadsheetId=SPREAD_SHEET_ID,
                                                         range="'크롤링_쇼핑몰'!A2:P3000").execute()
            values = result.get('values', [])
            for item in values:
                if self.service_name == item[0]:
                    if item[1] == 'CAFE24':
                        self.process.crawl(Cafe24, shopping_mall_settings=item)
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
