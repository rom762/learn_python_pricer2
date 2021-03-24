from .models import GPU
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, url_for)
from flask_login import current_user, login_required, login_user, logout_user

blueprint = Blueprint('gpu', __name__, template_folder='templates/gpu',
                      url_prefix='/gpu')


@blueprint.route('/')
@login_required
def gpu():
    gpus = GPU.query.all()
    return render_template(
        'gpu.html', menu=current_app.menu, title='Видеокарты', gpus=gpus)
