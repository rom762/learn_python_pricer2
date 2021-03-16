from pprint import pprint
import requests
import settings


def weather_city(city_name='Moscow,Russia'):
    url = settings.WEATHER_URL
    params = {
        'key': settings.WEATHER_API_KEY,
        'q': city_name,
        'format': 'json',
        'num_of_days': 1,
        'lang': 'ru',
    }
    try:
        response = requests.get(url, params)
        print(f'Weather source response.status_code {response.status_code}')
    except requests.RequestException:
        print('Сетевая ошибка')
        return None

    try:
        weather = response.json()
        if 'data' in weather:
            if 'current_condition' in weather['data']:
                return weather
    except (IndexError, TypeError) as exp:
        print(exp, exp.args)
        return None


if __name__ == '__main__':
    pprint(weather_city())
