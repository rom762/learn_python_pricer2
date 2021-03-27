import logging
import os
from glob import glob
import csv
import re
from pathlib import Path
import pandas as pd
from glob import glob
from webapp import create_app
from webapp.model import db
from webapp.gpu.models import Regard, Citilink
from pprint import pprint
from datetime import datetime

models = {'citilink': Citilink, 'regard': Regard}


def get_latest_file(mask='*citilink*.csv'):
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


def get_regard_model(name):
    pattern = "\(([^)]*)"
    match = re.search(pattern, name)
    if match:
        return match[1]
    else:
        return 'delete'


def write_to_db(model, data):
    db.session.bulk_insert_mappings(model, data)
    db.session.commit()


def merge_data_from_shops():

    regard_file = "regard_2021-03-27 20-21.csv"
    citilink_file = "citilink 2021-3-27-gpu.csv"

    citilink_df = pd.read_csv(citilink_file, encoding="UTF-8", sep=';')
    citilink_df['model'] = citilink_df['shortName'].apply(lambda x: x.split(', ')[-1].strip())

    regard_df = pd.read_csv(regard_file, encoding="UTF-8", sep=';')
    regard_df['model'] = regard_df['name'].apply(lambda x: get_regard_model(x))
    regard_df = regard_df.loc[regard_df['model'] != 'delete']

    gpu = pd.merge(citilink_df, regard_df, how='inner', on='model', suffixes=('_citilink', '_regard'))

    return gpu


def write_merged_data_to_db(gpu, db_table='GPU'):
    gpu = gpu.drop(['id', 'categoryId', 'categoryName', 'price_citilink', 'oldPrice',
                          'clubPrice', 'regard_id', 'brand_name', 'name', 'picture_regard',
                          'price_regard'], axis=1)
    gpu.columns=['name', 'vendor', 'picture', 'model']
    try:
        gpu.to_sql(name=db_table, con=db.engine, index=False, if_exists='append')
        logging.info('gpus in da base!')
    except Exception as exp:
        logging.info(f'{__name__} something goes wrong in {write_merged_data_to_db.__name__}')


# def main():
#     full_path_to_csv = get_latest_file()
#     print(f'filename: {full_path_to_csv}')
#     fields = get_fields(full_path_to_csv)
#     print(f'Fields: {fields}')
#     products = get_products_from_csv(full_path_to_csv, fields)
#     write_to_db(Regard, products)


if __name__ == '__main__':
    shop = 'regard'
    model = models[shop]
    if model:
        latest_file = get_latest_file('*' + shop + '*.csv')
        print(f'latest file: {latest_file}')
        fields = get_fields(latest_file)
        print(f'fields: {fields}')
        products = get_products_from_csv(latest_file, fields)
        print('Products========================================')
        # pprint(products)
        app = create_app()
        with app.app_context():
            #write_to_db(models['citilink'], products)
            write_to_db(model, products)



    # app = create_app()
    # with app.app_context():
    #     df = merge_data_from_shops()
    #     print(df.head())
        # write_merged_data_to_db(df)



