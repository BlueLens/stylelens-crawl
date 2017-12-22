from scrapy import Spider, Request
from stylelens_crawl.util import make_url


class Stylenanda(Spider):
    name = 'Stylenanda'
    target_domain = 'stylenanda.com'
    netloc = 'http://stylenanda.com'

    def start_requests(self):
        yield Request(url=self.netloc)

    def parse(self, response):
        # 이게 표준 인듯
        sub_urls = response.css('ul.xans-layout-category a::attr(href)').extract()

        for url in sub_urls:
            yield Request(url=self.netloc + url, callback=self.sub_parse)

    def sub_parse(self, response):
        item_urls = response.css('div.xans-product-normalpackage li.item div.name a::attr(href)').extract()
        next_page = response.css('div.xans-product-normalpaging p a::attr(href)').extract()[-1]

        self.logger.info(next_page)

        for url in item_urls:
            yield Request(url=self.netloc + url, callback=self.detail_parse)

        if next_page != '#none':
            yield Request(url=self.netloc + '/product/list.html' + next_page, callback=self.sub_parse)

    def detail_parse(self, response):
        sub_images = []

        # Subimages의 경로가 다름
        for url in response.css('div#prdDscp img::attr(src)').extract():
            sub_images.append(make_url(self.netloc, url))

        find_no = response.url[response.url.find('product_no'):]
        find_no = find_no[:find_no.find('&')].split('=')[-1]

        product = {
            'host_url': self.target_domain,
            'host_code': 'HC0001',
            'host_name': self.name,
            'name': response.css('meta[property="og:title"]::attr(content)').extract_first(),
            'tags': [response.css('meta[name="keywords"]::attr(content)').extract_first().split(',')[-1].strip()],
            'price': int(response.css('meta[property="product:sale_price:amount"]::attr(content)').extract_first()),
            'currency_unit': response.css(
                'meta[property="product:sale_price:currency"]::attr(content)').extract_first(),
            'product_url': response.url,
            'product_no': find_no,
            'nation': 'kr',
            'main_image': response.css('meta[property="og:image"]::attr(content)').extract_first(),
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
