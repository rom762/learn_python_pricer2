import datetime
import os
from pprint import pprint

import requests
import re
from bs4 import BeautifulSoup


class PricerParser:

    def __init__(self, *args, **kwargs):
        pprint(kwargs)

        self.url = kwargs['url']
        self.shop = kwargs['shop_name']

    def get_html(self, params=None):
        try:
            response = requests.get(self.url, params=params)
            print(response.status_code)
            if response.status_code == 200:
                self.status = response.status_code
                return response.text

        except requests.exceptions.RequestException as exp:
            print(response.raise_for_status())
            print(exp, exp.args)
        return None

    def save_to_db(self):
        pass

    def make_path(self):
        date_str = datetime.strftime(datetime.today(), '%Y-%m-%d %H-%M')
        filename = self.shop + "_" + date_str + ".csv"
        full_path = os.path.join(os.path.dirname(__file__), 'data', filename)
        normalized_path = os.path.abspath(full_path)
        return normalized_path

    def __str__(self):
        return f'url: {self.url}, status: {self.status}'


class Regard(PricerParser):
    def __init__(self, url):
        self.products = []
        self.pages = []
        self.shop_name = 'regard'
        self.url = url

    def get_pages_to_parse(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'html.parser')
        pagination = soup.select('div.pagination')[0].findAll('a')

        for page in pagination:
            if page.has_attr('href'):
                self.pages.append(page['href'])

    def parse_product(self, block):
        current_product = {}

        img = block.select('div.block_img')[0].select('a')[0]['href']
        regard_id = int(block.find('div', class_='code').text.split()[-1])
        content = block.select('div.aheader')[0].find('span')
        name = content.attrs['content']
        brand = content.attrs['data-brand']

        price_span = block.select('div.price')[0].findAll('span')[-1]
        price = float(''.join(re.findall(r'\d', price_span.text)))

        current_product['regard_id'] = regard_id
        current_product['brand_name'] = brand
        current_product['name'] = name
        current_product['picture'] = img
        current_product['price'] = price
        current_product['url'] = 'https://www.regard.ru/catalog/tovar' + str(
            regard_id) + '.htm'
        current_product['model'] = self.get_regard_model(name)
        return current_product

    def get_products_on_page(self, soup):

        products_on_page = soup.find_all('div', class_='block')

        for index, block in enumerate(products_on_page):
            current_product = self.parse_product(block)
            self.products.append(current_product)

    @staticmethod
    def get_regard_model(name):
        pattern = "\(([^)]*)"
        match = re.search(pattern, name)
        if match:
            return match[1]
        else:
            return None

    def __str__(self):
        return f'{self.__class__}, {self.url}'


class Citilink(PricerParser):
    def __init__(self, url):
        self.shop = 'citilink'
        self.url = url

    def __str__(self):
        return f'{self.__class__}, {self.url}'


if __name__ == "__main__":
    urls = [
        'https://citilink.ru',
        'https://regard.ru',
    ]

    citilink = Citilink(url=urls[0])
    regard = Regard(url=urls[1])


    print(f'citilink: {citilink}')
    print('-'*10)
    print(f'regard: {regard}')


