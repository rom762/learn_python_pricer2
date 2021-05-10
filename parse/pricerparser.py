import requests
import re
from bs4 import BeautifulSoup


class PricerParser:

    def __init__(self, *args, **kwargs):
        self.url = kwargs['url']

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

    def __str__(self):
        return f'url: {self.url}, status: {self.status}'


class Regard(PricerParser):

    def __init__(self, url):
        super().__init__(url)
        self.products = []
        self.pages = []

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

    def __str__(self):
        return f'{self.__class__}, {self.url}'


if __name__ == "__main__":
    urls = [
        'https://citilink.ru',
        'https://regard.ru',
    ]

    citilink = Citilink(url=urls[0])
    regard = Regard(url=urls[1])


    print(citilink)
    print('-'*10)
    print(regard)


