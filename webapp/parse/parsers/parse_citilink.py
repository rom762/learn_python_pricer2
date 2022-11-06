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

# logging.basicConfig(filename='parse.log', level=logging.DEBUG)


def get_logger(filename: str = "citilink_parse.log", level: str = "INFO") -> logging.getLogger():
    root = logging.getLogger()
    root.setLevel(level)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(filename=filename, mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root.addHandler(file_handler)
    root.addHandler(stream_handler)
    return root


params = {
    'available': '1',
    'status': '55395790',
    'country': 'Все',
    'sorting': 'rating_desc',
    'p': 1,
}

categories_info = {
    # 'monitors': {
    #     'url': 'https://www.citilink.ru/catalog/computers_and_notebooks/monitors/',
    #     'section_tag': 'ProductGroupList',
    # },
    # 'ssd': {
    #     'url': 'https://www.citilink.ru/catalog/ssd-nakopiteli/',
    #     'section_tag': 'GroupGrid',
    # },
    # 'gpu': {
    #     'url': 'https://www.citilink.ru/catalog/videokarty/',
    #     'section_tag': 'ProductGroupList',
    # },
    'hdd': {
        'url': 'https://www.citilink.ru/catalog/zhestkie-diski/',
        'section_tag': 'ProductGroupList',
    },
    # 'cartridges': 'https://www.citilink.ru/catalog/computers_and_notebooks/monitors_and_office/cartridges/?',
    # 'cactus' : 'https://www.citilink.ru/catalog/computers_and_notebooks/monitors_and_office/cartridges/?available=1&status=55395790&p=1&f=2521_77CACTUS',
    # 'toners': 'https://www.citilink.ru/catalog/computers_and_notebooks/monitors_and_office/toners/?',
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


def get_response(url: str = BASE_URL, params: dict = None):
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


def get_next_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    link_to_last_page = soup.select('a.PaginationWidget__arrow_right')
    if link_to_last_page:
        return int(link_to_last_page[0]['data-page'])


def is_already_parsed(products, current_id):
    for already_parsed in products:
        if already_parsed['id'] == current_id:
            print(f'find duplicate {current_id}')
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


def get_products_on_page(html: str, section_tag: str = 'ProductGroupList'):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        section = soup.select(f'section.{section_tag}')[0]
    except IndexError as e:
        logging.error(e, e.args)
    else:
        raw_products = section.select('div.product_data__gtm-js')
        logging.info(f'found {len(raw_products)} on page')
        products = []
        for product in raw_products:
            try:
                current_product = json.loads(product['data-params'])
                if is_already_parsed(products, current_product['id']):
                    continue
                current_product['picture'] = get_picture(product)
                current_product['url'] = get_url(product)
                products.append(current_product)
            except Exception as e:
                print(e, e.args)
                print(f'product: {product}')

        return products


def parse_one_page(url: str, parameters: dict = None, tag: str = 'ProductGroupList'):
    if parameters is None:
        parameters = params

    response = get_response(url=url, params=parameters)
    html = get_html(response)
    next_page = get_next_page(html)
    result = get_products_on_page(html, tag)
    portion_df = pd.DataFrame(result)
    portion_df.rename(
        {
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
        }, axis=1, inplace=True
    )

    portion_df['model'] = portion_df['name'].apply(
        lambda x: x.split(', ')[-1].strip())
    return portion_df, next_page


def save_portion(category_path: str, category_name: str, portion: pd.DataFrame):
    portion['processed_dttm'] = datetime.now()
    try:
        portion.to_csv(category_path, mode='a', sep=';', encoding='utf-8', index=False)
        logging.info(f'{params["p"]} portion of category {category_name.upper()} has been saved to {category_path}')
    except Exception as e:
        logging.error(e, e.args)


def make_path(category):
    date_str = datetime.strftime(datetime.today(), '%Y-%m-%d-%H-%M')
    filename = "citilink_" + category + '_' + date_str + ".csv"
    full_path = os.path.join(os.path.dirname(__file__), 'data', filename)
    normalized_path = os.path.abspath(full_path)
    return normalized_path


def main():
    for category in categories_info.keys():
        url = categories_info[category]['url']
        tag = categories_info[category]['section_tag']
        logging.info(f'now parsing category: {category.upper()}')

        category_path = make_path(category)
        logging.info(f'path for {category} is {category_path}')

        params['p'] = 1
        while True:
            portion, next_page = parse_one_page(url=url, tag=tag)
            logging.info(f'there is {len(portion)} items in the portion')
            save_portion(category_path=category_path, category_name=category, portion=portion)
            if not next_page:
                break
            else:
                params['p'] = next_page

        logging.info(f'end parsing {category}')
        time.sleep(randint(1, 3))


if __name__ == "__main__":
    logger = get_logger()
    main()
