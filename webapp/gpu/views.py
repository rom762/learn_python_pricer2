from pprint import pprint
from decimal import Decimal

from webapp.model import db, Shop
from .models import GPU, GpuPrice, GpuLink
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, url_for, abort)
from flask_login import current_user, login_required, login_user, logout_user

blueprint = Blueprint('gpu', __name__, template_folder='templates',
                      url_prefix='/gpu')


@blueprint.route('/')
@login_required
def gpu():
    gpus_from_db = GPU.query.all()
    gpus = []
    for gpu in gpus_from_db:
        elem = {
            'gpu_id': gpu.id,
            'vendor': gpu.vendor,
            'name': gpu.name,
        }
        gpus.append(elem)

    return render_template(
        'gpu.html', menu=current_app.menu, title='Видеокарты', gpus=gpus)


def first_var():
    gpus = GPU.query.all()
    first_var = []
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
                'prices': prices_cleared,
                }
        first_var.append(elem)
    return first_var


def second_var():
    gpus = GPU.query.all()
    second_var = []
    query = db.session.query(GPU, GpuPrice).join(
        GpuPrice, GPU.id == GpuPrice.gpu_id,
    )
    return second_var


def third_var():
    query = db.session.query(GPU)
    price_list = []
    for vc in query:
        prices = []
        for price in vc.prices:
            prices.append({
                'shop_id': price.shop_id,
                'price': float(price.price),
            })

        elem = {
            'gpu_id': vc.id,
            'model': vc.model,
            'name': vc.name,
            'vendor': vc.vendor,
            'prices': prices,
        }
        price_list.append(elem)
    return price_list


@blueprint.route('/<int:gpu_id>')
@login_required
def gpu_detail(gpu_id):
    gpu = GPU.query.filter_by(id=gpu_id).first()
    shops = Shop.query.all()
    prices = []
    for shop in shops:
        shop_last_price = GpuPrice.query.filter(
            GpuPrice.gpu_id == gpu.id,
            GpuPrice.shop_id == shop.id).order_by(
            GpuPrice.created_on.desc())\
            .first()

        price_link = GpuLink.query.filter(
            GpuLink.gpu_id == gpu.id,
            GpuLink.shop_id == shop.id)\
            .first()

        if shop_last_price and price_link:
            prices.append({
                'shop_id': shop.id,
                'price': shop_last_price.price.quantize(Decimal("1.00")),
                'link': price_link.url,
            })

    if not gpu:
        abort(404)
    else:
        return render_template('/detail.html', menu=current_app.menu, title=gpu.name, gpu=gpu, prices=prices)
