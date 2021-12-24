"""Module containing functions that can be used to obtain necessary info"""
import requests
from datetime import datetime

def time_converter(utc):
    dt = utc
    dt = datetime.fromtimestamp(dt)
    dt = str(dt)[12:16]
    # print(dt)
    return dt

def nasa_apod(count=1):
    """Returns the NASA astronomy picture of the day"""
    
    with open("keys/nasa_key.txt") as api_key:
        key = api_key.read().rstrip('\n')

    if count == 1:
        api_request = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={key}")
    else:
        api_request = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={key}&count={count}")
    info = {}
    
    if api_request.status_code == 200:
        if count == 1:
            info["hd_link"] = api_request.json()["hdurl"]
            info["title"] = api_request.json()["title"]
            info["description"] = api_request.json()["explanation"]
        else:
            api_request = list(api_request.json())
            info["hd_link"] = []
            info['title'] = []
            info['description'] = []
            for n in range(count):
                info["hd_link"].append(api_request[n]["hdurl"])
                info["title"].append(api_request[n]["title"])
                info["description"].append(api_request[n]["explanation"])
    # could potentially be customizable via function arguments (e.g. number of images)
    return info

    
def weather_api(city):
    """Returns weather for the city"""

    with open("keys/weather_key.txt") as api_key:
        key = api_key.read().rstrip('\n')
    units = "imperial"

    api_request = requests.get(f"https://api.openweathermap.org/data/2.5/?q={city}&units={units}&appid={key}")
    info = {}
    print(api_request.json())

    if api_request.status_code == 200:
        print('success')
        # kelvin_temp = api_request.json()["main"]["temp"]
        # info["temp"] = int((kelvin_temp - 273.15) * 1.8 + 32.5)
        info["description"] = api_request.json()["weather"][0]["description"][0].upper() + api_request.json()["weather"][0]["description"][1:] # capitalize first character
        info['temp'] = int(api_request.json()['main']['temp'])
        info['feels_like'] = int(api_request.json()['main']['feels_like'])
        info['temp_min'] = int(api_request.json()['main']['temp_min'])
        info['temp_max'] = int(api_request.json()['main']['temp_max'])
        info['pressure'] = int(api_request.json()['main']['pressure'])
        info['humidity'] = int(api_request.json()['main']['humidity'])
        info['visibility'] = int(api_request.json()['visibility'] * 0.000621371) # convert meters to miles
        info['wind'] = api_request.json()['wind'] # contains wind.speed, wind.deg (direction), wind.gust
        info['clouds'] = api_request.json()['clouds']['all'] # cloudiness %
        info['icon'] = api_request.json()['weather'][0]['icon']
        info['main'] = api_request.json()['weather'][0]['main']
        info['city'] = api_request.json()['name']
        info['sunrise'] = time_converter(api_request.json()['sys']['sunrise'])
        info['sunset'] = time_converter(api_request.json()['sys']['sunset'])
        info['lat'] = api_request.json()['coord']['lat']
        info['lon'] = api_request.json()['coord']['lon']
    else:
        print(f'error code: {api_request.status_code}')

    '''api_request = requests.get(f"https://api.openweathermap.org/data/2.5?lat={info['lat']}&lon={info['lon']}")
    if api_request.status_code == 200:
        print(api_request.json())'''
    return info

#print(weather_api("New+York+City"))

'''
{'coord': {'lon': -74.006, 'lat': 40.7143}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 36.28, 'feels_like': 36.28, 'temp_min': 33.24, 'temp_max': 39.29, 'pressure': 1021, 'humidity': 46}, 'visibility': 10000, 'wind': {'speed': 1.99, 'deg': 266, 'gust': 5.99}, 'clouds': {'all': 1}, 'dt': 1640286600, 'sys': {'type': 2, 'id': 2039034, 'country': 'US', 'sunrise': 1640261859, 'sunset': 1640295164}, 'timezone': -18000, 'id': 5128581, 'name': 'New York', 'cod': 200}
'''
