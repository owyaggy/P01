"""Module containing functions that can be used to obtain necessary info"""
import requests
from datetime import datetime

def nasa_apod(count=1):
    """Returns the NASA astronomy picture of the day, or {count} random images"""
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
    return info

def nytimes_api(days=1):
    """Returns the most viewed NYTimes articles from the past {days} days"""
    with open('keys/nytimes_key.txt') as api_key:
        key = api_key.read().rstrip('\n')

    api_request = requests.get(f'https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key={key}')
    info = {}

    # print(f'https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key={key}')

    if api_request.status_code == 200:
        info['url'] = list()
        info['title'] = list()
        info['abstract'] = list()
        info['img'] = list()
        info['caption'] = list()
        info['num'] = int(api_request.json()['num_results'])
        for result in api_request.json()['results']:
            info['url'].append(result['url'])
            info['title'].append(result['title'])
            info['abstract'].append(result['abstract'])
            try:
                info['img'].append(result['media'][0]['media-metadata'][2]['url'])
                info['caption'].append(result['media'][0]['caption'])
            except:
                info['img'].append(None)
                info['caption'].append(None)
    return info

def get_time(utc, minutes=True):
    """Helper function to convert UTC timestamp to datetime for weather api"""
    dt = utc
    dt = datetime.fromtimestamp(dt)
    if minutes:
        dt = str(dt)[11:16]
    else:
        dt = str(dt)[11:14]
    return dt

def minute_forecast(minutes):
    """Helper minutely forecast data analysis function for weather api"""
    minute_start = -1
    minute_end = -1
    for minute in range(len(minutes)):
        if minutes[minute]['precipitation'] == 0:
            if minute_start != -1:
                minute_end = minute
        else:
            if minute_start == -1:
                minute_start = minute
    if minute_start == -1:
        return "There will be no precipitation for the next hour."
    elif minute_end == -1:
        return f"Precipitation will begin in {minute_start} minutes."
    else:
        return f"Precipitation will begin in {minute_start} minutes and end after {minute_end - minute_start} minutes."

def weather_api(city):
    """Returns weather for the city"""
    with open("keys/weather_key.txt") as api_key:
        key = api_key.read().rstrip('\n')

    units = "imperial" # other potential option metric
    api_request = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={key}")
    info = {}

    if api_request.status_code == 200:
        # kelvin_temp = api_request.json()["main"]["temp"]
        # info["temp"] = int((kelvin_temp - 273.15) * 1.8 + 32.5)
        info['temp_min'] = int(api_request.json()['main']['temp_min'])
        info['temp_max'] = int(api_request.json()['main']['temp_max'])
        info['city'] = api_request.json()['name']
        info['lat'] = api_request.json()['coord']['lat']
        info['lon'] = api_request.json()['coord']['lon']
        if 'rain' in api_request.json().keys():
            info['rain'] = api_request.json()['rain']
        if 'snow' in api_request.json().keys():
            info['snow'] = api_request.json()['snow']

    with open('keys/forecast_key.txt') as api_key:
        key = api_key.read().rstrip('\n') # changes key to avoid making two requests per call

    # print(f"https://api.openweathermap.org/data/2.5/onecall?lat={info['lat']}&lon={info['lon']}&units={units}&appid={key}")
    api_request = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={info['lat']}&lon={info['lon']}&units={units}&appid={key}")
    if api_request.status_code == 200:
        info["description"] = api_request.json()['current']["weather"][0]["description"][0].upper() + \
                              api_request.json()["current"]['weather'][0]["description"][1:]  # capitalize first character
        info['temp'] = int(api_request.json()['current']['temp'])
        info['feels_like'] = int(api_request.json()['current']['feels_like'])
        info['pressure'] = int(api_request.json()['current']['pressure'])
        info['humidity'] = int(api_request.json()['current']['humidity'])
        info['visibility'] = int(api_request.json()['current']['visibility'] * 0.000621371)  # convert meters to miles

        info['wind_speed'] = api_request.json()['current']['wind_speed']
        info['wind_deg'] = api_request.json()['current']['wind_deg']
        info['wind_gust'] = api_request.json()['current']['wind_gust']
        info['clouds'] = api_request.json()['current']['clouds']  # cloudiness %
        info['icon'] = api_request.json()['current']['weather'][0]['icon']
        info['main'] = api_request.json()['current']['weather'][0]['main']
        info['sunrise'] = get_time(api_request.json()['current']['sunrise']).lstrip('0')
        info['sunset'] = str(int(get_time(api_request.json()['current']['sunset']).lstrip('0')[:2]) - 12) + get_time(api_request.json()['current']['sunset'])[2:]
        info['dew_point'] = api_request.json()['current']['dew_point']
        info['uvi'] = api_request.json()['current']['uvi']
        info['minutely'] = minute_forecast(api_request.json()['minutely'])
        info['hourly'] = []
        for hour in range(10):
            info['hourly'].append({
                'time': get_time(api_request.json()['hourly'][hour]['dt'], minutes=False),
                'temp': int(api_request.json()['hourly'][hour]['temp']),
                'description': api_request.json()['hourly'][hour]['weather'][0]['description'][0].upper() + api_request.json()['hourly'][hour]['weather'][0]['description'][1:],
                'icon': api_request.json()['hourly'][hour]['weather'][0]['icon']
            })
            info['hourly'][-1]['time'] += "00"
            if int(info['hourly'][-1]['time'][:2]) < 12:
                info['hourly'][-1]['time'] += " AM"
            else:
                info['hourly'][-1]['time'] += " PM"
            if info['hourly'][-1]['time'][:2] == '00':
                info['hourly'][-1]['time'] = '12' + info['hourly'][-1]['time'][2:]
            if int(info['hourly'][-1]['time'][:2]) > 12:
                info['hourly'][-1]['time'] = str(int(info['hourly'][-1]['time'][:2]) - 12) + info['hourly'][-1]['time'][2:]
        info['daily'] = []
        for day in api_request.json()['daily']:
            info['daily'].append({
                'date': str(datetime.fromtimestamp(day['dt']))[5:10],
                'moon_phase': int(100 * float(day['moon_phase'])),
                'min': int(day['temp']['min']),
                'max': int(day['temp']['max']),
                'description': day['weather'][0]['description'][0].upper() + day['weather'][0]['description'][1:],
                'icon': day['weather'][0]['icon'],
                'uvi': day['uvi']
            })
        info['daily'][0]['date'] = 'Today'
    return info

def nba_api(year):
    """Returns the NBA rankings for each division and conference"""
    with open("keys/nba_key.txt") as api_key:
        key = api_key.read().rstrip('\n')
    info = {}

    api_request = requests.get(f"https://api.sportradar.us/nba/trial/v7/en/seasons/{year}/REG/rankings.json?api_key={key}")
    if api_request.status_code == 200:
        for conference in api_request.json()["conferences"]:
            info[conference["name"]] = {}
            for division in conference["divisions"]:
                info[conference["name"]][division["name"]] = {}
                for team in division["teams"]:
                    if "rank" in team.keys():
                        info[conference["name"]][division["name"]][team["rank"]["division"]] = team["market"] + " " + team["name"]

    return info

def nhl_api(year):
    """Returns the NHL rankings for each division and conference"""
    with open("keys/nhl_key.txt") as api_key:
        key = api_key.read().rstrip('\n')
    info = {}

    api_request = requests.get(f"https://api.sportradar.us/nhl/trial/v7/en/seasons/{year}/REG/rankings.json?api_key={key}")
    if api_request.status_code == 200:
        for conference in api_request.json()["conferences"]:
            info[conference["name"]] = {}
            for division in conference["divisions"]:
                info[conference["name"]][division["name"]] = {}
                for team in division["teams"]:
                    if "rank" in team.keys():
                        info[conference["name"]][division["name"]][team["rank"]["division"]] = team["market"] + " " + team["name"]

    return info

def mlb_api(year):
    """Returns the MLB rankings for each division and league"""
    with open("keys/mlb_key.txt") as api_key:
        key = api_key.read().rstrip('\n')
    info = {}

    api_request = requests.get(f"https://api.sportradar.us/mlb/trial/v7/en/seasons/{year}/REG/rankings.json?api_key={key}")
    if api_request.status_code == 200:
        for league in api_request.json()["league"]["season"]["leagues"]:
            info[league["name"]] = {}
            for division in league["divisions"]:
                info[league["name"]][division["name"]] = {}
                for team in division["teams"]:
                    if "rank" in team.keys():
                        info[league["name"]][division["name"]][team["rank"]["division"]] = team["market"] + " " + team["name"]

    return info

def nfl_api(year):
    """Returns the NFL rankings for each division and conference"""
    with open("keys/nfl_key.txt") as api_key:
        key = api_key.read().rstrip('\n')
    info = {}

    api_request = requests.get(f"https://api.sportradar.us/nfl/official/trial/v7/en/seasons/{year}/REG/standings/season.json?api_key={key}")
    if api_request.status_code == 200:
        for conference in api_request.json()["conferences"]:
            info[conference["name"]] = {}
            for division in conference["divisions"]:
                info[conference["name"]][division["name"]] = {}
                for team in division["teams"]:
                    if "rank" in team.keys():
                        info[conference["name"]][division["name"]][team["rank"]["division"]] = team["market"] + " " + team["name"]

    return info

def sports_api(year):
    """Returns the team rankings for nba, nhl, mlb, and nfl"""
    info = {}
    info["nba"] = nba_api(year)
    info["nhl"] = nhl_api(year)
    info["mlb"] = mlb_api(year)
    info["nfl"] = nfl_api(year)

    return info

#This only has 100 calls per month, so try not to use too much
#def stocks_api(symbols):
#    """Returns latest end-of-day opening, high, low and closing prices for each stock in the list symbols"""
#    with open("keys/stocks_key.txt") as api_key:
#        key = api_key.read().rstrip('\n')
#    info = {}
#
#    for symbol in symbols:
#        info[symbol] = {}
#        api_request = requests.get(f"http://api.marketstack.com/v1/eod?access_key={key}&symbols={symbol}")
#        if api_request.status_code == 200:
#            info[symbol]["open"] = api_request.json()["data"][0]["open"]
#            info[symbol]["high"] = api_request.json()["data"][0]["high"]
#            info[symbol]["low"] = api_request.json()["data"][0]["low"]
#            info[symbol]["close"] = api_request.json()["data"][0]["close"]
#
#    return info
