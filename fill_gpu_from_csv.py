import csv
import time

from webapp.model import db, GPU
from webapp import create_app


def read_csv(filename='citilink.csv'):
    with open(filename, 'r', encoding='utf-8') as ff:
        # fields = ['citilink_id', 'categoryId', 'price', 'oldPrice', 'shortName',
        #           'categoryName', 'brandName', 'clubPrice', 'picture']
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


def save_gpu_data2(data):
    db.session.bulk_insert_mappings(GPU, data)
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
        start = time.perf_counter()
        read_csv()
        end = time.perf_counter() - start
        print(f'Загрузка заняла: {end} секунд')
