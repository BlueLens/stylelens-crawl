import js2xml
import requests
from bs4 import BeautifulSoup

from scrapy import Spider, Request
from stylelens_crawl.services import make_url


class DoubleSixGirls(Spider):
    name = '66girls'
    target_domain = '66girls.co.kr'
    netloc = 'http://66girls.co.kr'
    crawled_product = []

    def start_requests(self):
        yield Request(url=self.netloc)

    def parse(self, response):
        sub_urls = response.css('div.side_contents ul li a::attr(href)').extract()

        for url in sub_urls:
            yield Request(url=self.netloc + url, callback=self.sub_parse)

    def sub_parse(self, response):
        item_urls = response.css('div.xans-product-normalpackage li p.name a::attr(href)').extract()
        next_page = response.css('div.xans-product-normalpaging p a::attr(href)').extract()[-2]

        for url in item_urls:
            product_no = None
            try:
                product_no = url[url.find('product_no') + 11:].split(sep='&')[0]
            except Exception as ex:
                self.logger.error(ex)
            if product_no in self.crawled_product:
                yield Request(
                    url=self.netloc + url,
                    callback=self.detail_parse,
                    meta={'is_exist': True})
            else:
                if product_no is not None:
                    self.crawled_product.append(product_no)
                review_url = 'http://widgets1.cre.ma/66girls.co.kr/products/reviews?iframe=1&product_code=%s' % product_no
                yield Request(
                    url=review_url,
                    callback=self.review_parse,
                    meta={'item_url': self.netloc + url, 'page': 1, 'reviews': [], 'review_url': review_url})

        if next_page != '#none':
            yield Request(url=self.netloc + '/product/list.html' + next_page, callback=self.sub_parse)

    def review_parse(self, response):
        reviews = response.meta['reviews']
        self.logger.debug(response.meta)
        if len(response.css('li.product_review__container')) and response.meta['page'] <= 5:
            for product_review in response.css('li.product_review__container'):
                review_image = []
                for img in product_review.css('ul.images li img::attr(src)').extract():
                    review_image.append(make_url('http://assets1.cre.ma', img.replace('thumbnail_', '')))

                writer = {
                    'id': product_review.css('div.product_review__info_container li div.value::text').extract()[0],
                    'grade': product_review.css('div.product_review__info_container li div.value::text').extract()[
                        1].strip(),
                    'height': 0,
                    'my_size': '',
                    'product_size': '',
                    'color': ''
                }
                self.logger.debug('############################# %s' % product_review.css(
                    'li::attr(data-expand-url)').extract_first())
                expanded_review_response = requests.get(
                    'http://widgets1.cre.ma%s' % product_review.css('li::attr(data-expand-url)').extract_first(),
                    headers={'Accept': 'text/javascript'})
                parse = js2xml.parse(expanded_review_response.text, 'UTF-8')
                element = parse.xpath('//object/identifier[@name="$review_content_expanded"]')[0]
                parsed = BeautifulSoup(
                    element.getparent().getparent().getparent().getparent().find('arguments/string').text, 'lxml')
                for option_value in parsed.find_all('div', class_='review-option'):
                    option = option_value.find('div', class_='review-option-title').text.strip()
                    value = option_value.find('div', class_='review-option-content')
                    if option == '키':
                        try:
                            height_values = value.text.strip().split('~')
                            if height_values[0] == '':
                                writer['height'] = int(height_values[-1])
                            else:
                                writer['height'] = int(height_values[0])
                        except Exception as ex:
                            self.logger.error(ex)
                    elif option.find('사이즈') > -1:
                        writer['my_size'] = value.text.strip()
                    elif option == '선택한 옵션':
                        for sub_option in value.find_all('span', class_='review-product-option'):
                            if len(sub_option.find('span', class_='option-key')):
                                sub_option_value = sub_option.find('span', class_='option-key').text.strip()
                                if sub_option_value == 'COLOR:':
                                    writer['color'] = sub_option.find('span', class_='option-value').text.strip()
                                if sub_option_value == 'SIZE:':
                                    writer['product_size'] = sub_option.find('span', class_='option-value').text.strip()

                review = {
                    'photo': review_image,
                    'text': parsed.find('div', class_='message').text,
                    'write_data': '',
                    'total_count': 0,
                    'likes': int(product_review.css('span.like-score::text').extract_first()),
                    'writer': writer
                }

                reviews.append(review)

            response.meta['page'] = response.meta['page'] + 1
            response.meta['reviews'] = reviews

            yield Request(url='%s&page=%s' % (response.meta['review_url'], response.meta['page']),
                          callback=self.review_parse, meta=response.meta)
        else:
            yield Request(url=response.meta['item_url'], callback=self.detail_parse,
                          meta={'reviews': response.meta['reviews'], 'is_exist': False})

    def detail_parse(self, response):
        sub_images = []
        product_no = response.css('span[id="snackbe_item_id"]::text').extract_first()
        if response.meta['is_exist']:
            self.logger.debug('Exist: %s' % response.url)

            yield {
                'is_exist': True,
                'product_no': product_no,
                'tags': [response.css('meta[name="keywords"]::attr(content)').extract_first().split(',')[-1].strip()],
            }
        else:
            for url in response.css('div#prdDetail img::attr(src)').extract():
                sub_images.append(make_url(self.netloc, url))
            self.logger.debug('Not exist: %s' % response.url)
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
                'product_no': product_no,
                'nation': 'kr',
                'main_image': response.css('meta[property="og:image"]::attr(content)').extract_first(),
                'sub_images': sub_images,
                'feedback': response.meta['reviews']
            }

            yield product
