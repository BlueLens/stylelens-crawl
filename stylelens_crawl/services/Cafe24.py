from scrapy import Spider, Request
from stylelens_crawl.util import make_url, get_netloc


class Cafe24(Spider):
    def __init__(self, shopping_mall_settings, *args, **kwargs):

        self.host_code = shopping_mall_settings[0]
        self.name = shopping_mall_settings[2]
        self.domain = shopping_mall_settings[3]
        self.netloc = get_netloc(self.domain)
        self.shopping_mall_settings = shopping_mall_settings
        self.logger.info('Host Code: %s\nHost Name: %s\nHost Domain: %s\nNetwork Location: %s\nSettings: %s' % (
                            self.host_code, self.name, self.domain, self.netloc, self.shopping_mall_settings))
        super(Cafe24, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(url=self.domain)

    def parse(self, response):
        sub_urls = response.css(self.shopping_mall_settings[6]).extract()

        for url in sub_urls:
            yield Request(url=self.domain + url, callback=self.sub_parse)

    def sub_parse(self, response):
        item_urls = response.css(self.shopping_mall_settings[7]).extract()
        next_page = response.css(self.shopping_mall_settings[8]).extract()[int(self.shopping_mall_settings[9])]

        for url in item_urls:
            yield Request(url=self.domain + url, callback=self.detail_parse)

        if next_page != '#nzone':
            yield Request(url=self.domain + self.shopping_mall_settings[4] + next_page, callback=self.sub_parse)

    def detail_parse(self, response):
        sub_images = []

        for url in response.css(self.shopping_mall_settings[15]).extract():
            sub_images.append(make_url(self.domain, url))

        find_no = response.url[response.url.find(self.shopping_mall_settings[5]):]
        find_no = find_no[:find_no.find('&')].split('=')[-1]

        product = {
            'host_url': self.netloc,
            'host_code': self.host_code,
            'host_name': self.name,
            'name': response.css(self.shopping_mall_settings[10]).extract()[-1],
            'tags': [response.css(self.shopping_mall_settings[11]).extract_first().split(',')[-1].strip()],
            'price': int(response.css(self.shopping_mall_settings[12]).extract_first()),
            'currency_unit': response.css(self.shopping_mall_settings[13]).extract_first(),
            'product_url': response.url,
            'product_no': find_no,
            'nation': 'kr',
            'main_image': response.css(self.shopping_mall_settings[14]).extract()[-1],
            'sub_images': sub_images,
            # 'feedback':
            # {
            #     'photo': '',
            #     'text': '',
            #     'write_data': '',
            #     'total_count': 10,
            #     'likes': 7,
            #     'writer': {
            #         'id': 'fsdfa',
            #         'grade': 'fds',
            #         'height': 444,
            #         'my_size': 'XXL',
            #         'product_size': 'Small',
            #         'color': 'red'
            #     }
            # }
        }
        yield product
