import requests
from bs4 import BeautifulSoup
from pathlib import Path
from flask import current_app


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
            published_date = news.find('time')['datetime']
            result_news.append({
                'title':title,
                'url': url,
                'published': published_date,
            })
        return result_news
    return False


if __name__ == "__main__":
    get_python_news()
