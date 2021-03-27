import os
import logging
import json
import sys
import time
from datetime import datetime
from pprint import pprint
from random import randint

import pandas as pd
import requests
from bs4 import BeautifulSoup

#data = pd.DataFrame()

logging.basicConfig(filename='parse.log', level=logging.DEBUG)

parameters = {
    'available' : '1',
    'status': '55395790', # Это там где хит новинка распродажа конкретно этот "любой"
    'country': 'Все',
    'sorting': 'rating_desc'
}

urls = {
    'monitors': 'https://www.citilink.ru/catalog/computers_and_notebooks/monitors/?available=1&status=55395790',
    'cartridges': 'https://www.citilink.ru/catalog/computers_and_notebooks/monitors_and_office/cartridges/?',
    'cactus' : 'https://www.citilink.ru/catalog/computers_and_notebooks/monitors_and_office/cartridges/?available=1&status=55395790&p=1&f=2521_77CACTUS',
    'toners': 'https://www.citilink.ru/catalog/computers_and_notebooks/monitors_and_office/toners/?',
    'gpu': 'https://www.citilink.ru/catalog/videokarty/',
}

file_names = {
    'monitors': 'monitors',
    'cartridges': 'cartridges',
    'cactus': 'cactus',
    'toners': 'toners',
    'gpu': 'gpu',
}

# тут задаем категорию из которой парсим
CATEGORY = 'gpu'
base_url = urls[CATEGORY]
filename = datetime.strftime(datetime.utcnow(), '%Y-%m-%d-%H-%M-%S')
final_filename = 'citilink_' + filename + '.csv'

print(base_url, 'data', final_filename, sep='\n')


def get_response(url=base_url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response
    except ValueError as exp:
        logging.info(f'{__name__}, error: {exp}')


def get_html(response):
    if response.status_code == 200:
        return response.text
    else:
        logging.info(f'get_html returns response status: {response.status_code}')
        return None


def next_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    link_to_last_page = soup.select('a.PaginationWidget__arrow_right')
    if link_to_last_page:
        return int(link_to_last_page[0]['data-page'])


def parse_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    section = soup.select('section.ProductGroupList')[0]
    products_on_page = section.select('div.product_data__gtm-js')
    products_data = []

    for product in products_on_page:
        current_product = json.loads(product['data-params'])

        try:
            picture = product.select('img.ProductCardHorizontal__image')[0]['src']
            current_product['picture'] = picture
        except IndexError as exp:
            print(f'product with {current_product["id"]} has no picture')

        try:
            product_header = product.select('div.ProductCardHorizontal__header-block')[0]
            product_url = product_header.select('a.ProductCardHorizontal__title')[0]['href']
            current_product['url'] = 'https://www.citilink.ru' + product_url
        except IndexError as exp:
            print(f'product with {current_product["id"]} has no detailed page')

        products_data.append(current_product)

    return products_data


def collect_data(page=1):
    final_df = pd.DataFrame()

    while page:
        print(f'current_page_number: {page}')
        response = get_response(params={'p': page})
        html = get_html(response)
        result = parse_data(html)

        portion_df = pd.DataFrame(result)
        final_df = pd.concat([final_df, portion_df], ignore_index=True, sort=False)
        page = next_page(html)
        # citilink начинает возвращать 404 если парсить слишком быстро
        print('now sleeping...')
        time.sleep(randint(1, 4))

    final_df.rename({
        'id': 'citilink_id',
        'categoryId': 'category_id',
        'price': 'price',
        'oldPrice': 'old_price',
        'shortName': 'short_name',
        'categoryName': 'category_name',
        'brandName': 'brand_name',
        'clubPrice': 'club_price',
        'picture': 'picture',
        'url': 'url'
    }, axis=1, inplace=True)
    final_path = os.path.join('data', final_filename)
    final_df.to_csv(final_path, sep=';', encoding='utf-8', index=False)
    logging.info('parsing citilink is done.')
    print('parsing citilink is done.')


if __name__ == "__main__":
    collect_data()



