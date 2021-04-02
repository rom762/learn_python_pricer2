import logging
from functools import reduce
import os
from glob import glob
import csv
import re
from pathlib import Path
import pandas as pd
from glob import glob
from webapp import create_app
from webapp.model import db, Shop
from webapp.gpu.models import Regard, Citilink, GPU, GpuPrice, GpuLink
from pprint import pprint
from datetime import datetime

models = {'citilink': Citilink, 'regard': Regard}


def get_latest_file(shop=''):
    mask = '*' + shop + '*.csv'
    basedir = os.path.abspath(os.path.dirname(__file__))
    datapath = os.path.join(basedir, 'data', mask)
    list_of_files = glob(datapath)
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


def get_fields(full_path):
    with open(full_path, 'r') as ff:
        line = ff.readline().strip()
        fields = line.split(';')
    return fields


def get_products_from_csv(full_path, fields):
    with open(full_path, 'r', encoding='UTF-8') as ff:
        reader = csv.DictReader(ff, fields, delimiter=';')
        products = []
        for row in reader:
            if row['price'] == 'price':
                continue
            try:
                row['price'] = float(row['price'])
                products.append(row)
            except (ValueError, AttributeError) as exp:
                print(exp, exp.args, row['price'])

        return products


def get_gpu_model(name, shop_name='citilink'):
    if shop_name == 'regard':
        return crop_regard_model_from_name(name)
    else:
        return name.split(', ')[-1].strip()


def crop_regard_model_from_name(name):
    pattern = "\(([^)]*)"
    match = re.search(pattern, name)
    if match:
        return match[1]
    else:
        return 'delete'


def write_to_db(model, data, need_returns=False):
    try:
        returns = db.session.bulk_insert_mappings(model, data, return_defaults=need_returns)
        db.session.commit()
        return returns
    except BaseException as exp:
        print(exp, exp.args)


def merge_data_from_shops_csv():

    # regard_file = "regard_2021-03-27 20-21.csv"
    regard_file = get_latest_file('regard')
    # citilink_file = "citilink 2021-3-27-gpu.csv"
    citilink_file = get_latest_file('citilink')

    citilink_df = pd.read_csv(citilink_file, encoding="UTF-8", sep=';')
    # citilink_df['model'] = citilink_df['short_name'].apply(lambda x: x.split(', ')[-1].strip())

    regard_df = pd.read_csv(regard_file, encoding="UTF-8", sep=';')
    # regard_df['model'] = regard_df['name'].apply(lambda x: crop_regard_model_from_name(x))
    regard_df = regard_df.loc[regard_df['model'] != 'delete']

    gpu = pd.merge(citilink_df, regard_df, how='inner', on='model', suffixes=('_citilink', '_regard'))

    return gpu


def write_merged_data_to_db(gpu, db_table='GPU'):

    gpu = gpu.drop(['citilink_id', 'category_id', 'price_citilink', 'old_price',
                    'category_name', 'club_price', 'url_citilink', 'regard_id', 'brand',
                    'name', 'picture_regard', 'price_regard', 'url_regard'],
                   axis=1)

    gpu.columns = ['name', 'vendor', 'picture', 'model']

    try:
        gpu.to_sql(name=db_table, con=db.engine, index=False, if_exists='append')
        logging.info('gpus in da base!')

    except Exception as exp:
        logging.info(f'{__name__} something goes wrong in {write_merged_data_to_db.__name__}')


def fill_shops_tables(shop='regard'):
    """
    тут мы заполняем из последнего прайса таблицы citilink и regard
    вообще плохо пониманию зачем они нам?

    """
    db_model = models[shop]
    if db_model:
        latest_file = get_latest_file('*' + shop + '*.csv')
        print(f'latest file: {latest_file}')
        fields = get_fields(latest_file)
        # print(f'fields: {fields}')
        products = get_products_from_csv(latest_file, fields)
        # print('Products========================================')
        # pprint(products)
        app = create_app()
        with app.app_context():
            write_to_db(db_model, products)


def fill_shops_table():
    shops = [{
            'name': 'regard',
            'url': 'https://regard.ru'
        }, {
            'name': 'citilink',
            'url': 'https://citilink.ru'
        },
        ]
    app = create_app()
    with app.app_context():
        write_to_db(Shop, shops)
    print('done!')


def has_id(model):
    gpu = GPU.query.filter(GPU.model == model).first()
    if gpu:
        return gpu.id


def find_shop_by_name(search_str):
    t1 = search_str.split('\\')
    t2 = t1[-1].split('_')[0].strip()

    try:
        shop = Shop.query.filter(Shop.name == t2).first()
        return shop.id
    except AttributeError as exp:
        print(exp, exp.args, t2)


def get_new_products_from_file(filename):
    # вот тут как то можно наверное по другому.
    # нужно просто выбрать столбец model оттуда и кинуть в список
    # надо спросить в чате
    # gpus = pd.read_sql('SELECT GPU.model FROM GPU', con=db.session.bind)
    # gpus_model_list = gpus['model'].to_list()

    gpus = db.session.query(GPU.model).all()
    gpus_model_list = reduce(lambda x, y: list(x) + list(y), gpus)
    gpus2db = []
    gpu2url = []
    with open(filename, 'r', encoding='UTF-8') as ff:
        fields = ff.readline().strip().split(';')
        reader = csv.DictReader(ff, fields, delimiter=';')
        for row in reader:
            model = row['model']
            # gpu_id = has_id(model)
            if model not in gpus_model_list:
                # gpu = GPU(vendor=row['vendor'], name=row['name'], picture=row['picture'], model=model)
                # db.session.add(gpu)
                gpu = {'vendor': row['vendor'], 'name': row['name'], 'picture': row['picture'], 'model': model}

                gpus2db.append(gpu)
                gpus_model_list.append(model)
            #     print(f'gpu {model} added')
            # else:
            #     print(f'{model} already in da base')
        db.session.bulk_insert_mappings(GPU, gpus2db, return_defaults=True)
        db.session.commit()
        return gpus2db


def get_new_prices(filename, shop_id):
    parsed_df = pd.read_csv(filename, encoding='UTF-8', sep=';')
    parsed_df['shop_id'] = shop_id
    parsed_df = parsed_df.loc[:, ['price', 'model', 'shop_id']]

    gpu_in_db_df = pd.read_sql_table('GPU', con=db.session.bind)
    gpu_in_db_df = gpu_in_db_df.loc[:, ['id', 'model']]

    final = parsed_df.merge(gpu_in_db_df)

    final.rename(columns={'id': 'gpu_id'}, inplace=True)
    final.drop(columns=['model'], inplace=True)
    final['created_on'] = datetime.now()
    try:
        final.to_sql('gpu_prices', if_exists='append', index=False, con=db.session.bind)
        print(f'{final["gpu_id"].count()} was added to prices')
    except Exception as exp:
        final.to_csv(r'data/final.csv', encoding='ansi', sep=';', index=False)
        print(exp, exp.args)


def get_urls(filename):
    parsed_df = pd.read_csv(filename, encoding='UTF-8', sep=';')
    parsed_df['shop_id'] = shop_id
    # parsed_df = parsed_df.loc[:, ['url', 'price', 'model', 'shop_id']]

    gpu_in_db_df = pd.read_sql_table('GPU', con=db.session.bind)
    gpu_in_db_df = gpu_in_db_df.loc[:, ['id', 'model']]

    final = parsed_df.merge(gpu_in_db_df)
    final = final.loc[:, ['id', 'shop_id', 'shop_gpu_id', 'url']]
    final.rename(columns={'id': 'gpu_id'}, inplace=True)

    records = final.to_dict('records')
    write_to_db(GpuLink, records)
    return records


if __name__ == '__main__':
    app = create_app()
    with app.app_context():

        filename = get_latest_file(shop='regard')
        print(f'filename: {filename}')
        shop_id = find_shop_by_name(filename)
        if shop_id:
            new_gpu = get_new_products_from_file(filename)
            print(f'added {len(new_gpu)} gpus')
            get_new_prices(filename, shop_id)
            records = get_urls(filename)
            print(f'{len(records)} added to links')
        else:
            print('Shop not found!')

