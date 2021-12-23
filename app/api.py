"""Module containing functions that can be used to obtain necessary info"""
import requests

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

    api_request = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+key)
    info = {}

    print(api_request.json())

    if api_request.status_code == 200:
        info["description"] = api_request.json()["weather"][0]["description"]
        kelvin_temp = api_request.json()["main"]["temp"]
        info["temp"] = int((kelvin_temp - 273.15) * 1.8 + 32.5)
    return info

#print(weather_api("New+York+City"))
