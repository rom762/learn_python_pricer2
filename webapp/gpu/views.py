from .models import GPU
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, url_for, abort)
from flask_login import current_user, login_required, login_user, logout_user

blueprint = Blueprint('gpu', __name__, template_folder='templates',
                      url_prefix='/gpu')


@blueprint.route('/')
@login_required
def gpu():
    gpus = GPU.query.all()
    return render_template(
        'gpu.html', menu=current_app.menu, title='Видеокарты', gpus=gpus)


@blueprint.route('/<int:gpu_id>')
@login_required
def gpu_detail(gpu_id):
    gpu = GPU.query.filter_by(id=gpu_id).first()
    citilink
    if not gpu:
        abort(404)
    else:
        return render_template('/detail.html', menu=current_app.menu, title=gpu.name, gpu=gpu)
