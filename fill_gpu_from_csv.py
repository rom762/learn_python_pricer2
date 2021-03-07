import csv
from webapp.model import db, GPU
from webapp import create_app


def read_csv(filename='citilink.csv'):
    with open(filename, 'r', encoding='utf-8') as ff:
        fields = ['id', 'categoryId', 'price', 'oldPrice', 'shortName',
                  'categoryName', 'brandName', 'clubPrice', 'picture']
        reader = csv.DictReader(ff, fields, delimiter=';')
        for row in reader:
            save_gpu_data(row)


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
        read_csv()
