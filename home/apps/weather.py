import requests
import datetime


token = "5e028467-0619-4aec-bfb9-9df6591bd63a"


def get_weather(lat=55.45, lon=37.36, days=7, hours=False):  # По-умолчанию Москва на 7 дней без прогноза по часам
    hours = "true" if hours else "false"
    d = datetime.datetime.today()
    url = "https://api.weather.yandex.ru/v1/forecast?lat={}&lon={}&limit={}&hours={}".format(lat, lon, days, hours)
    headers = {"X-Yandex-API-Key": token}
    indicators = [0]*10
    try:
        weather = requests.get(url=url, headers=headers).json()
        data = weather.get('fact')
        forecast = weather.get('forecasts')
        parts = forecast[4]
        part = parts.get('parts')
        if 18 <= d.hour <= 23:
            pogoda = part.get('evening')
        elif 6 <= d.hour <= 11:
            pogoda = part.get('morning')
        elif 0 <= d.hour <= 5:
            pogoda = part.get('night')
        else:
            pogoda = part.get('day')
        wind_dir = data.get('wind_dir')
        wind_dir = wind_dir.replace("s", 'Ю')
        wind_dir = wind_dir.replace("e", 'В')
        wind_dir = wind_dir.replace("n", 'C')
        wind_dir = wind_dir.replace("w", 'З')
        indicators.append(wind_dir)
        indicators[0] = data.get('temp')
        indicators[9] = data.get('feels_like')
        indicators[1] = data.get('condition')
        indicators[2] = data.get('wind_speed')
        indicators[3] = wind_dir
        indicators[4] = data.get('humidity')
        indicators[6] = data.get('pressure_mm')
        indicators[5] = data.get('part_name')
        indicators[7] = pogoda.get('prec_prob')
        indicators[8] = pogoda.get('prec_mm')
        return indicators
    except requests.ConnectionError:
        return {}


if __name__ == '__main__':
    get_weather()