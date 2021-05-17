import logging
from pprint import pprint
from decimal import Decimal
from webapp.user.forms import RegistrationForm
from .forms import SubscribeForm
from webapp.user.models import User
from webapp.model import db, Shop
from .models import GPU, GpuPrice, GpuLink, GpuUser
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, url_for, abort, request)
from flask_login import current_user, login_required, login_user, logout_user
from webapp.utils import get_redirect_target
from webapp.settings import SUBSCRIBES_LIMIT

blueprint = Blueprint('gpu', __name__, template_folder='templates',
                      url_prefix='/gpu')


@blueprint.route('/')
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
    subscribe_form = SubscribeForm()
    video_card = GPU.query.filter_by(id=gpu_id).first()
    shops = Shop.query.all()
    prices = []
    for shop in shops:
        shop_last_price = GpuPrice.query.filter(
            GpuPrice.gpu_id == video_card.id,
            GpuPrice.shop_id == shop.id).order_by(
            GpuPrice.created_on.desc())\
            .first()

        price_link = GpuLink.query.filter(
            GpuLink.gpu_id == video_card.id,
            GpuLink.shop_id == shop.id)\
            .first()

        if shop_last_price and price_link:
            prices.append({
                'shop_id': shop.id,
                'shop_name': price_link.shop.name,
                'price': shop_last_price.price.quantize(Decimal("1.00")),
                'link': price_link.url,
            })

    already_subscribed = GpuUser.query.filter(GpuUser.user_id == current_user.get_id(), GpuUser.gpu_id == video_card.id).all()
    print(f'detail page - already_subscribed: {already_subscribed}')
    print(f'detail page - current user id: {current_user.get_id()}')
    print(f'detail page - gpu id: {video_card.id}')
    subscribes = GpuUser.query.filter(GpuUser.user_id == current_user.get_id()).count()
    can_subscribe = subscribes < SUBSCRIBES_LIMIT

    if not video_card:
        abort(404)
    else:
        return render_template('/detail.html', menu=current_app.menu, title=video_card.name, gpu=video_card, prices=prices,
                               subscribe_form=subscribe_form,
                               already_subscribed=already_subscribed,
                               can_subscribe=can_subscribe)


@blueprint.route('/subscribe/<int:gpu_id>')
@login_required
def subscribe(gpu_id):
    print(f'receive gpu id: {gpu_id}')
    user = User.query.filter(User.id == current_user.get_id()).first()
    gpu = GPU.query.filter_by(id=gpu_id).first()

    already_in = GpuUser.query.filter(GpuUser.user_id == user.id, GpuUser.gpu_id == gpu.id).count()
    print(f'already in: {already_in}')
    subscribes_by_user = GpuUser.query.filter(GpuUser.user_id == user.id).count()
    print(f'subscribes: {subscribes_by_user}')

    if already_in:
        flash(f'You already subscribed for {gpu.name}', 'error')

    elif subscribes_by_user > 2:
        print(f'you have exceeded the limit of subscriptions')
        flash(f'You have exceeded the limit of subscriptions')
    else:
        gpu_user = GpuUser(gpu_id=gpu.id, user_id=user.id)
        db.session.add(gpu_user)
        db.session.commit()
        flash(f'You subscribed for {gpu.name}', 'success')

    return redirect(get_redirect_target())


@blueprint.route('/unsubscribe/<int:gpu_id>')
@login_required
def unsubscribe(gpu_id):

    subscriptions = GpuUser.query.filter(
        GpuUser.user_id == current_user.get_id(),
        GpuUser.gpu_id == gpu_id)

    video_card = GPU.query.get(gpu_id)

    for each in subscriptions.all():
        print(f'each id: {each.id}')

    if subscriptions.count():
        try:
            subscriptions.delete()
            db.session.commit()
            flash(f'You\'re now un-subscribed from {video_card.name}', 'warning')
        except Exception as exp:
            flash(f'Something goes wrong with unsubscribe', 'error')
            print('Ошибка при удалении записи')
            print(exp, exp.args)

    return redirect(get_redirect_target())

