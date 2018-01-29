from scrapy import Spider, Request
from stylelens_crawl.util import make_url, get_netloc
import urllib.request
import urllib.parse
import json

class HANDSOME(Spider):
    target_domain = 'thehandsome.com'
    netloc = 'http://thehandsome.com'

    def __init__(self, shopping_mall_settings, *args, **kwargs):
        self.host_code = shopping_mall_settings['host_code']
        self.name = shopping_mall_settings['brand_name']
        self.brand_code = shopping_mall_settings['brand_code']
        self.shopping_mall_settings = shopping_mall_settings
        self.logger.info('Host Code: %s\nHost Name: %s\nBrand Code: %s\nNetwork Location: %s\nSettings: %s' % (
            self.host_code, self.name, self.brand_code, self.netloc, self.shopping_mall_settings))
        super(HANDSOME, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(url=self.netloc)

    def parse(self, response):
        url = self.netloc + '/c/categoryList?brandCode=br' + self.brand_code + '&categoryCode=br' + self.brand_code + '&productOrderCode=NEW&pageNum=1&pageSize=1000'
        res = urllib.request.urlopen(url)

        try:
            string = res.read().decode('utf-8')
            json_obj = json.loads(string)

            if len(json_obj['results']) > 0:
                brand_name = json_obj['results'][0]['productBrandName']
                # print('brand : ' + brand_name + '\nhandsome_brand_code : ' + str(self.brand_code))
            print(len(json_obj['results']))

            for product in json_obj['results']:
                yield Request(
                    url=self.netloc + '/p/' + product['productStyleCode'],
                    callback=self.detail_parse)
        except:
            # print('brand : ' + str(brand_name))
            print('Brand not found !')

    def detail_parse(self, response):
        sub_images = []
        # for url in response.css('div#prdDetail img::attr(src)').extract():
        #     sub_images.append(make_url(self.netloc, url))

        product = {
            'host_url': self.netloc + '/c/br' + self.brand_code + '/br' + self.brand_code,
            'host_code': self.host_code,
            'host_name': self.name,
            'name': response.css('meta[property="recopick:title"]::attr(content)').extract_first(),
            'product_url': response.css('meta[property="og:url"]::attr(content)').extract_first(),
            'tags': response.css('meta[property="og:description"]::attr(content)').extract_first(),
            'price': int(response.css('meta[property="recopick:price"]::attr(content)').extract_first()),
            'currency_unit': response.css(
                'meta[property="recopick:price:currency"]::attr(content)').extract_first(),
            'product_no': self.brand_code,
            'nation': 'kr',
            'main_image': response.css('meta[property="og:image"]::attr(content)').extract_first(),
            'sub_images': sub_images,
        }
        yield product

    @staticmethod
    def get_host_with_service_name(host_code):
        if host_code == 'HC1001':
            return {'host_code': host_code, 'brand_name': "TIME", 'brand_code': '01'}
        if host_code == 'HC1002':
            return {'host_code': host_code, 'brand_name': "MINE", 'brand_code': '02'}
        if host_code == 'HC1003':
            return {'host_code': host_code, 'brand_name': "SYSTEM", 'brand_code': '03'}
        if host_code == 'HC1004':
            return {'host_code': host_code, 'brand_name': "SJSJ", 'brand_code': '04'}
        if host_code == 'HC1005':
            return {'host_code': host_code, 'brand_name': "TIME HOMME", 'brand_code': '06'}
        if host_code == 'HC1006':
            return {'host_code': host_code, 'brand_name': "SYSTEM HOMME", 'brand_code': '07'}
        if host_code == 'HC1007':
            return {'host_code': host_code, 'brand_name': "the CASHMERE", 'brand_code': '08'}
        if host_code == 'HC1008':
            return {'host_code': host_code, 'brand_name': "MM6", 'brand_code': '11'}
        if host_code == 'HC1009':
            return {'host_code': host_code, 'brand_name': "EACHxOTHER", 'brand_code': '12'}
        if host_code == 'HC1010':
            return {'host_code': host_code, 'brand_name': "ELEVENTY", 'brand_code': '13'}
        if host_code == 'HC1011':
            return {'host_code': host_code, 'brand_name': "BIRD by JUICY COUTURE", 'brand_code': '14'}
        if host_code == 'HC1012':
            return {'host_code': host_code, 'brand_name': "Tom GreyHound", 'brand_code': '15'}
        if host_code == 'HC1013':
            return {'host_code': host_code, 'brand_name': "MUE", 'brand_code': '16'}
        if host_code == 'HC1014':
            return {'host_code': host_code, 'brand_name': "JUICY COUTURE", 'brand_code': '17'}
        if host_code == 'HC1015':
            return {'host_code': host_code, 'brand_name': "IRO", 'brand_code': '24'}
        if host_code == 'HC1016':
            return {'host_code': host_code, 'brand_name': "THE KOOPLES", 'brand_code': '25'}
        if host_code == 'HC1017':
            return {'host_code': host_code, 'brand_name': "FOURM STUDIO", 'brand_code': '30'}
        if host_code == 'HC1018':
            return {'host_code': host_code, 'brand_name': "LÄTT BY T", 'brand_code': '31'}
        if host_code == 'HC1019':
            return {'host_code': host_code, 'brand_name': "FOURM MEN'S LOUNGE", 'brand_code': '32'}
        if host_code == 'HC1020':
            return {'host_code': host_code, 'brand_name': "FOURM ATELIER", 'brand_code': '34'}
        if host_code == 'HC1021':
            return {'host_code': host_code, 'brand_name': "FOURM THE STORE", 'brand_code': '35'}
        if host_code == 'HC1022':
            return {'host_code': host_code, 'brand_name': "PORTS 1961", 'brand_code': '40'}
