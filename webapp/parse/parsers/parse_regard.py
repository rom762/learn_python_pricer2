import os
import re
from datetime import datetime
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_response(url):
    try:
        cur_res = requests.get(url, headers={'User-Agent': UserAgent().chrome})
        cur_res.raise_for_status()
        return cur_res
    except Exception as exp:
        print('bad connection', exp, exp.args)


def get_links_to_parse(response):
    pages = []
    soup = BeautifulSoup(response.text, 'html.parser')
    pagination = soup.select('div.pagination')[0].findAll('a')

    for page in pagination:
        if page.has_attr('href'):
            pages.append(page['href'])

    return pages


def get_products_on_page(soup):
    products = []
    products_on_page = soup.findAll('div', class_='block')

    for index, block in enumerate(products_on_page):
        current_product = {}

        img = block.select('div.block_img')[0].select('a')[0]['href']
        regard_id = int(block.find('div', class_='code').text.split()[-1])
        content = block.select('div.aheader')[0].find('span')
        name = content.attrs['content']
        vendor = content.attrs['data-brand']

        price_span = block.select('div.price')[0].findAll('span')[-1]
        price = float(''.join(re.findall(r'\d', price_span.text)))

        current_product['shop_gpu_id'] = regard_id
        current_product['vendor'] = vendor
        current_product['name'] = name
        current_product['picture'] = img
        current_product['price'] = price
        current_product['url'] = 'https://www.regard.ru/catalog/tovar' + str(regard_id) + '.htm'
        current_product['model'] = get_regard_model(name)
        products.append(current_product)

    return products


def get_regard_model(name):
    pattern = "\(([^)]*)"
    match = re.search(pattern, name)
    if match:
        return match[1]
    else:
        return 'delete'


def make_path():
    date_str = datetime.strftime(datetime.today(), '%Y-%m-%d %H-%M')
    filename = "regard_" + date_str + ".csv"
    full_path = os.path.join(os.path.dirname(__file__), 'data', filename)
    normalized_path = os.path.abspath(full_path)
    return normalized_path


def parse_regard():
    data = pd.DataFrame()
    BASE_URL = 'https://www.regard.ru/catalog/group4000.htm'
    splitted_url_parts = urlparse(BASE_URL)

    fetch_response_for_pagination = get_response(BASE_URL)
    pages_to_parse = get_links_to_parse(fetch_response_for_pagination)

    for page in pages_to_parse:
        url = splitted_url_parts.scheme + '://' + splitted_url_parts.netloc + page
        print(url, end=', ')
        response = get_response(url)
        print(response.status_code)

        soup = BeautifulSoup(response.text, 'html.parser')

        products_on_page = get_products_on_page(soup)

        df = pd.DataFrame.from_records(products_on_page)
        data = pd.concat([data, df], ignore_index=True, sort=False)

    normalized_path = make_path()
    data.to_csv(normalized_path, encoding='UTF-8', index=False, sep=';')
    return {'message': 'parsing regard is done', 'status': 'success'}


if __name__ == "__main__":
    parse_regard()
