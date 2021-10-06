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

logging.basicConfig(filename='parse.log', level=logging.DEBUG)

parameters = {
    'available': '1',
    'status': '55395790',
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
BASE_URL = "https://www.citilink.ru/catalog/videokarty/"


def get_response(url=BASE_URL, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response
    except ValueError as exp:
        logging.info(f'{__name__}, error: {exp}')


def make_path():
    date_str = datetime.strftime(datetime.today(), '%Y-%m-%d %H-%M')
    filename = "citilink_" + date_str + ".csv"
    full_path = os.path.join(os.path.dirname(__file__), 'data', filename)
    normalized_path = os.path.abspath(full_path)
    return normalized_path


def get_html(response):
    if response.status_code == 200:
        return response.text
    else:
        logging.info(f'get_html returns response status: {response.status_code}')


def next_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    link_to_last_page = soup.select('a.PaginationWidget__arrow_right')
    if link_to_last_page:
        return int(link_to_last_page[0]['data-page'])


def is_already_parsed(products_data, current_product_id):
    for already_parsed in products_data:
        if already_parsed['id'] == current_product_id:
            print(f'find duplicate {current_product_id}')
            return True
    return False


def get_picture(product):
    try:
        picture = product.select('img.ProductCardHorizontal__image')[0]['src']
        return picture
    except IndexError as exp:
        return None


def get_url(product):
    try:
        product_header = product.select('div.ProductCardHorizontal__header-block')[0]
        product_url = product_header.select('a.ProductCardHorizontal__title')[0]['href']
        current_product_url = 'https://www.citilink.ru' + product_url
        return current_product_url
    except IndexError as exp:
        return None


def parse_data(html):

    products_data = []

    soup = BeautifulSoup(html, 'html.parser')
    section = soup.select('section.ProductGroupList')[0]
    products_on_page = section.select('div.product_data__gtm-js')

    for product in products_on_page:
        current_product = json.loads(product['data-params'])
        if is_already_parsed(products_data, current_product['id']):
            continue

        current_product['picture'] = get_picture(product)
        current_product['url'] = get_url(product)
        products_data.append(current_product)

    return products_data


def parse_citilink(page=1):
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
        'id': 'shop_gpu_id',
        'categoryId': 'category_id',
        'price': 'price',
        'oldPrice': 'old_price',
        'shortName': 'name',
        'categoryName': 'category_name',
        'brandName': 'vendor',
        'clubPrice': 'club_price',
        'picture': 'picture',
        'url': 'url',
    }, axis=1, inplace=True)


    final_df['model'] = final_df['name'].apply(lambda x: x.split(', ')[-1].strip())

    final_path = os.path.join('data', make_path())
    final_df.to_csv(final_path, sep=';', encoding='utf-8', index=False)
    message = 'parsing citilink is done.'
    logging.info(message)
    print(message)
    result = {'message': message, 'status': 'success'}

    return result


if __name__ == "__main__":
    parse_citilink()
