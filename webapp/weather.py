import requests
from webapp import settings
from pprint import pprint


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
        weather = response.json()
        # pprint(weather)
        # months = weather['data']['ClimateAverages'][0]['month']
        # pprint(months)
        if 'data' in weather:
            if 'current_condition' in weather['data']:
                try:
                    #return weather['data']['current_condition'][0]
                    return weather
                except (IndexError, TypeError):
                    return False
    except(requests.RequestException):
        print('Сетевая ошибка')
        return False
    return False


if __name__ == '__main__':
    pprint(weather_city())
