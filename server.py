from flask import Flask, render_template
from weather import weather_city

app = Flask(__name__)


menu = {
    'Home': '/',
    'News': '/news',
    'Weather': '/weather',
    'Register': '/register',
}


@app.route('/')
def index():
    title = 'Pricer'
    return render_template('index.html', page_title=title, menu=menu)


@app.route('/weather')
def weather(city='Barcelona, Spain'):
    title = f'Weather in {city}'
    weather = weather_city(city_name=city)
    current_city = weather['data']['request'][0]['query']
    current_weather = weather['data']['current_condition'][0]
    months = weather['data']['ClimateAverages'][0]['month']
    # pprint(weather)
    return render_template('weather.html', page_title=title, current_city=current_city, current_weather=current_weather,
                           months=months, menu=menu)


if __name__ == "__main__":
    app.run(debug=True)