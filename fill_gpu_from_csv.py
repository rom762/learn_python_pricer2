import os
import csv
import time
from datetime import datetime
from pprint import pprint

from webapp import create_app
from webapp.model import db
from webapp.gpu.models import GPU
from webapp.user.models import User


def read_users(filename='users.csv'):
    with open(filename, 'r', encoding='ansi') as ff:
        fields = ['id', 'firstname', 'lastname', 'city', 'email', 'password', 'date', 'role']
        reader = csv.DictReader(ff, fields, delimiter=';', )
        users = []
        for row in reader:
            if row['email'] == 'email':
                continue
            # row.pop('date')
            try:
                row['date'] = datetime.strptime(row['date'], '%Y-%m-%d %H:%M%:%S.%f')
            except ValueError:
                row['date'] = datetime.now()
            row.pop('id')

            users.append(row)
        return users


def read_csv(filename='citilink.csv'):
    with open(filename, 'r', encoding='utf-8') as ff:
        fields = ['citilink_id', 'category_id', 'price', 'old_price', 'short_name',
                  'category_name', 'brand_name', 'club_price', 'picture']
        reader = csv.DictReader(ff, fields, delimiter=';')
        video_cards = []
        for row in reader:
            try:
                row['price'] = float(row['price'])
                video_cards.append(row)
            except (ValueError, AttributeError) as exp:
                print(exp, exp.args)
        return video_cards



def save_gpu_data2(table, data):
    db.session.bulk_insert_mappings(table, data)
    db.session.commit()


def save_gpu_data(row):
    try:
        gpu = GPU(citilink_id=row['id'], categoryId=row['categoryId'], price=row['price'], oldPrice=row['oldPrice'],
                  shortName=row['shortName'], categoryName=row['categoryName'], brandName=row['brandName'],
                  clubPrice=row['clubPrice'], picture=row['picture'])
        db.session.add(gpu)
        db.session.commit()
        print(f'gpu {row["id"]} added to the base')
    except Exception as exp:
        db.session.rollback()  # откатываем изменения
        print(f"Ошибка добавления в БД: {exp}, {exp.args}")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        fields = get_fields()
        print(fields)

