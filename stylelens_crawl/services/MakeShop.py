from scrapy import Spider, Request
from stylelens_crawl.util import make_url, get_netloc


class MakeShop(Spider):
    def __init__(self, shopping_mall_settings, *args, **kwargs):

        self.host_code = shopping_mall_settings['host_code']
        self.name = shopping_mall_settings['name']
        self.scheme, self.netloc, _ = get_netloc(shopping_mall_settings['web_url'])
        self.domain = '%s://%s' % (self.scheme, self.netloc)
        self.shopping_mall_settings = shopping_mall_settings
        self.logger.info('Host Code: %s\nHost Name: %s\nHost Domain: %s\nNetwork Location: %s\nSettings: %s' % (
            self.host_code, self.name, self.domain, self.netloc, self.shopping_mall_settings))
        super(Cafe24, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(url=self.domain)

    def parse(self, response):
        sub_urls = response.css(self.shopping_mall_settings['category']).extract()

        for url in sub_urls:
            yield Request(url=self.domain + url, callback=self.sub_parse)

    def sub_parse(self, response):
        item_urls = response.css(self.shopping_mall_settings['product_url']).extract()
        next_page = response.css(self.shopping_mall_settings['next_page_btn']).extract()[
            int(self.shopping_mall_settings['next_page_idx'])]
        item_thum = response.css('div.xans-product-listnormal div.box')
        item_thum_cnt = len(item_thum)
        _, _, current_page = get_netloc(response.url)
        for i, url in enumerate(item_urls):
            meta = {}
            if (i + 1) <= item_thum_cnt:
                meta['thum_img'] = item_thum[i]

            yield Request(url=self.domain + url, callback=self.detail_parse, meta=meta)

        if next_page != '#none':
            yield Request(url=self.domain + current_page + next_page, callback=self.sub_parse)

    def detail_parse(self, response):
        sub_images = []

        for url in response.css(self.shopping_mall_settings['product_subimages']).extract():
            sub_images.append(make_url(self.domain, url))

        relation_product = []
        relation_product_items = response.css('div.xans-product-relation a::attr(href)').extract()

        if relation_product_items:
            for item in relation_product_items:
                item = item[item.find(self.shopping_mall_settings['product_var']):]
                item = item[:item.find('&')].split('=')[-1].strip()
                if item:
                    if item not in relation_product:
                        relation_product.append(item)

        tags = []
        for tag in response.css(self.shopping_mall_settings['product_tags']).extract_first().split(','):
            tag = tag.strip()
            if tag:
                tags.append(tag)

        find_no = response.url[response.url.find(self.shopping_mall_settings['product_var']):]
        find_no = find_no[:find_no.find('&')].split('=')[-1]

        product = {
            'host_url': self.netloc,
            'host_code': self.host_code,
            'host_name': self.name,
            'name': response.css(self.shopping_mall_settings['product_name']).extract()[-1],
            'cate': [response.css(self.shopping_mall_settings['product_tags']).extract_first().split(',')[-1].strip()],
            'tags': tags,
            'price': int(response.css(self.shopping_mall_settings['product_price']).extract_first()),
            'sale_price': int(response.css(self.shopping_mall_settings['product_sale_price']).extract_first()),
            'currency_unit': response.css(self.shopping_mall_settings['product_currency_unit']).extract_first(),
            'product_url': response.url,
            'product_no': find_no,
            'related_product': relation_product,
            'nation': 'kr',
            'thumbnail': None,
            'main_image': response.css(self.shopping_mall_settings['product_main_image']).extract()[-1],
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

        if 'thum_img' in response.meta:
            product['thumbnail'] = make_url(self.domain,
                                            response.meta['thum_img'].css('img::attr(src)').extract_first())

        yield product
