import os
import csv
import time
from datetime import datetime
from pprint import pprint

from webapp import create_app
from webapp.model import GPU, db
from webapp.user.models import User


def read_users(filename='profiles.csv'):
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
        save_gpu_data2(video_cards)


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


def get_fields(filename='regard_2021-03-18 17-17.csv'):
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_fullpath = os.path.join(basedir, 'webapp', 'parse', filename)
    with open(file_fullpath, 'r') as ff:
        line = ff.readline().strip()
        print(line)
        fields = line.split(';')
    return fields


if __name__ == '__main__':
    # app = create_app()
    # with app.app_context():
    #     start = time.perf_counter()
    #     users = read_users()
    #     pprint(users)
    #     db.session.bulk_insert_mappings(User, users)
    #     db.session.commit()
    #     end = time.perf_counter() - start
    #     print(f'Загрузка заняла: {end} секунд')
    app = create_app()
    with app.app_context():
        fields = get_fields()
        print(fields)
