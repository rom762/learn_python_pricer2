from pprint import pprint

from webapp import create_app

from webapp.model import db
from webapp.user.models import User
from webapp.gpu.models import GPU, GpuPrice


def get_user_by_id(user_id):
    try:
        user = User.query.filter(User.id == user_id).first()
        if not user:
            print('user not found!')
            return None
        return user
    except Exception as exp:
        print(f'Get data from Database error: {exp}')

    return None


def get_user_by_email(email):
    print(f'email: {email}')
    try:
        user = User.query.filter(User.email == email).first()
        if not user:
            print(f'user with email: {email} not found!')
            return None
        return user

    except Exception as exp:
        print(f'Get data from Database error: {exp}')

    return None


def first_var():
    gpus = GPU.query.all()
    final = []
    for gpu in gpus:
        prices = GpuPrice.query.filter(GpuPrice.gpu_id == gpu.id).order_by(GpuPrice.created_on).all()
        prices_cleared = []
        if prices:
            for price in prices:
                prices_cleared.append({'shop_id': price.shop_id,
                                       'price': float(price.price),
                                       })
        elem = {'gpu_id': gpu.id,
                'name': gpu.name,
                'vendor': gpu.vendor,
                'price': prices_cleared,
                }
        final.append(elem)
    return final


def second_var():
    query = db.session.query(GpuPrice, GPU).join(
        GPU, GpuPrice.gpu_id == GPU.id
    )
    gpu_list = []

    for prices, gpu in query:
        prices_cleared = []
        # print(f'gpu - {gpu.id, gpu.model}')
        if prices:
            # print(prices.price)
            elem = {'gpu_id': gpu.id,
                    'name': gpu.name,
                    'vendor': gpu.vendor,
                    'price': prices,
                    }
        gpu_list.append(elem)

    return gpu_list


def third_var():
    query = db.session.query(GPU)
    price_list = []
    for vc in query:
        prices = []
        for price in vc.prices:
            prices.append({
                'shop_id': price.shop_id,
                'price': price.price,
            })

        elem = {
            'gpu_id': vc.id,
            'name': vc.name,
            'vendor': vc.vendor,
            'prices': prices,
            'url': vc.links,
        }
        price_list.append(elem)
    return price_list


if __name__ == '__main__':

    app = create_app()
    with app.app_context():
        # print(third_var(1))
        gpus = third_var()

        for each in gpus:
            if each['gpu_id'] == 1:
                print(f"gpu_id: {each['gpu_id']}")
                print(f"name: {each['name']}")
                print(f"vendor: {each['vendor']}")
                print(f"links: {each['url']}")
                for price in each['prices']:
                    print(f"shop {price['shop_id']} - {float(price['price'])}")
