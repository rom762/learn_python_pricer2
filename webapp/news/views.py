from flask import Blueprint, render_template
from webapp.news.models import News

blueprint = Blueprint('news', __name__, url_prefix='/news')


@blueprint.route('/news')
def news():
    title = 'Python News'
    news_list = News.query.order_by(News.published.desc()).all()
    return render_template('news.html', page_title=title, news_list=news_list)
