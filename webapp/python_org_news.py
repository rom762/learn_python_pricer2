from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from flask import current_app

from webapp.model import News, db


def get_html(url, save=True):
    try:
        result = requests.get(url)
        result.raise_for_status()
        if save:
            with open('../python_org.html', 'w') as f:
                f.write(result.text)
        return result.text
    except(requests.RequestException, ValueError):
        return False


def get_python_news(local=True):
    if local:
        filename = Path("../python_org.html")
        with open(filename, 'r') as f:
            html = f.read()
    else:
        html = get_html(current_app.config['NEWS_URL'])

    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_="list-recent-posts").findAll('li')
        result_news = []
        for news in all_news:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time')['datetime']
            try:
                published = datetime.strptime(published, '%Y-%m-%d')
            except ValueError:
                published = datetime.now()
            save_news(title, url, published)
        #     result_news.append({
        #         'title':title,
        #         'url': url,
        #         'published': published,
        #     })
        # return result_news
    return False


def save_news(title, url, published):
    news_exists = News.query.filter(News.url == url).count()
    print(news_exists)
    if not news_exists:
        new_news = News(title=title, url=url, published=published)
        db.session.add(new_news)
        db.session.commit()


def show_news():
    pass

if __name__ == "__main__":
    get_python_news()
