import sys
import time
from random import randint
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json
from pprint import pprint


data = pd.DataFrame()

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
    'monitors' : 'monitors',
    'cartridges': 'cartridges',
    'cactus' : 'cactus',
    'toners' : 'toners',
    'gpu': 'gpu',
}

# тут задаем категорию из которой парсим
CATEGORY = 'gpu'
base_url = urls[CATEGORY]
now = datetime.now()
filename = [str(now.year), str(now.month), str(now.day), file_names[CATEGORY]]
final_filename = '-'.join(filename) + '.csv'
print(base_url, final_filename)


def get_response(url=base_url, key=1):
    current_url = url + str(key)
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.text
        else:
            print(response.status_code)
            return None
    except ValueError as exp:
        print(exp)
        return None


def get_products_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    products_on_page = soup.select('div.product_data__gtm-js')
    products_data = []

    for product in products_on_page:
        current_product_params = json.loads(product['data-params'])
        try:
            current_product_picture = product.select('img.ProductCardHorizontal__image')[0]['src'] or \
                              product.select('img.ProductCardVertical__picture')[0]['src']
        except IndexError as exp:
            print(f'product has {current_product_params["id"]} has no picture')

        current_product_params['picture'] = current_product_picture
        products_data.append(current_product_params)

    return products_data


def parse_data(page=1):
    final_df = pd.DataFrame()
    while page < 2:
        print(f'current_page_number: {page}')
        html = get_response(key=page)
        if not html:
            break
        result = get_products_data(html)

        portion_df = pd.DataFrame(result)
        final_df = pd.concat([final_df, portion_df], ignore_index=True, sort=False)
        page += 1
        # citilink начинает возвращать 404 если парсить слишком быстро
        print('now sleeping...')
        time.sleep(randint(1, 4))

    final_df.to_csv(final_filename, sep=';', encoding='utf-8', index=False)
    print('Done!')


if __name__ == "__main__":
    parse_data(page=1)