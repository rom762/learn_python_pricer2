import sys
import time

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
BASE_URL = urls[CATEGORY]
now = datetime.now()
filename = [str(now.year), str(now.month), str(now.day), file_names[CATEGORY]]
final_filename = '-'.join(filename) + '.csv'
print(BASE_URL, final_filename)


# def get_soup(url):
#     r = requests.get(url, headers={'User-Agent': UserAgent().chrome})
#     if r.status_code != 200:
#         print(f'Attention! Status is {r.status_code}')
#         return 'stop'
#     else:
#         soup = BeautifulSoup(r.text, 'html.parser')
#         return soup.body


def save_page(url='https://www.citilink.ru/catalog/videokarty/?p='):
    key = 1
    url = url + str(key)
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        with open('../citilink.html', 'w') as ff:
            ff.write(html)
            print('done!')

# save_page()
def get_local_citilink():
    with open('../citilink.html', 'r', encoding='cp1251') as ff:
        return BeautifulSoup(ff.read(), 'html.parser')


def get_response(url=BASE_URL, key=1):
    current_url = url + str(key)
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.text
        else:
            print(response.status_code)
            return False
    except ValueError as exp:
        print(exp)
        return False


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    products_on_page = soup.select('div.product_data__gtm-js')
    dicts_list = []

    for i in range(len(products_on_page)):
        product_params = json.loads(products_on_page[i]['data-params'])
        try:
            product_picture = products_on_page[i].select('img.ProductCardHorizontal__image')[0]['src'] or \
                              products_on_page[i].select('img.ProductCardVertical__picture')[0]['src']
        except IndexError as exp:
            print(i, exp, exp.args)

        product_params['picture'] = product_picture
        # if i % 10 == 0:
        #     print(product_params)
        dicts_list.append(product_params)

    return dicts_list


current_page_number = 1

while current_page_number < 10:
    print(f'current_page_number: {current_page_number}')
    html = get_response(key=current_page_number)
    if html:
        result = parse_html(html)
        df = pd.DataFrame(result)
        data = pd.concat([data, df], ignore_index=True, sort=False)
        print(data['id'].count)
        filename = f'citilink_{current_page_number}.csv'
        data.to_csv(filename, sep=';', encoding='utf-8', index=False)
    else:
        break

    current_page_number += 1
    time.sleep(4)
    # вот тут круто было бы пока спим писать в файл бэкап но это асинхрон, я туда не умею :(

data.to_csv('citilink.csv', sep=';', encoding='utf-8', index=False)


