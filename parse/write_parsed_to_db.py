import logging
import os
import csv
import re
from pathlib import Path
import pandas as pd
from glob import glob
from webapp import create_app
from webapp.model import db
from webapp.gpu.models import Regard
from pprint import pprint
from datetime import datetime


def get_latest_file():
    basedir = os.path.abspath(os.path.dirname(__file__))
    files = os.listdir(os.path.join(basedir, 'data'))
    files.sort(reverse=True)
    filename = files[0]
    full_path = os.path.join(basedir, 'data', filename)
    return full_path


def get_fields(full_path):
    with open(full_path, 'r') as ff:
        line = ff.readline().strip()
        print(line)
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


def write_to_db(model, data):
    db.session.bulk_insert_mappings(model, data)
    db.session.commit()


def main():
    full_path_to_csv = get_latest_file()
    print(f'filename: {full_path_to_csv}')
    fields = get_fields(full_path_to_csv)
    print(f'Fields: {fields}')
    products = get_products_from_csv(full_path_to_csv, fields)
    write_to_db(Regard, products)


def merge_data_from_shops():
    regard_file = r"data/regard_2021-03-19 00-41.csv"
    citilink_file = r"data/citilink_2021-03-25.csv"
    regard_df = pd.read_csv(regard_file, encoding="UTF-8", sep=';')
    citilink_df = pd.read_csv(citilink_file, encoding="UTF-8", sep=';')
    citilink_df['model'] = citilink_df['shortName'].apply(lambda x: x.split(', ')[-1].strip())
    regard_df['model'] = regard_df['name'].apply(lambda x: get_regard_model(x))
    regard_df = regard_df.loc[regard_df['model'] != 'delete']
    gpu = pd.merge(citilink_df, regard_df, how='inner', on='model', suffixes=('_citilink', '_regard'))
    gpu = gpu.drop(['id', 'categoryId', 'categoryName', 'price_citilink', 'oldPrice',
                           'clubPrice', 'regard_id', 'brand_name', 'name', 'picture_regard',
                           'price_regard'], axis=1)
    gpu.columns=['name', 'vendor', 'picture', 'model']
    # df.to_sql(name='client_history', con=db.engine, index=False)
    return gpu


def write_merged_data_to_db(df, db_table='GPU'):
    try:
        df.to_sql(name=db_table, con=db.engine, index=False, if_exists='append')
        logging.info('gpus in da base!')
    except Exception as exp:
        logging.info(f'{__name__} something goes wrong in {write_merged_data_to_db.__name__}')


def get_regard_model(name):
    pattern = "\(([^)]*)"
    match = re.search(pattern, name)
    if match:
        return match[1]
    else:
        return 'delete'


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        df = merge_data_from_shops()
        write_merged_data_to_db(df)


