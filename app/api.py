"""Module containing functions that can be used to obtain necessary info"""
import requests

def nasa_apod():
    """Returns the NASA astronomy picture of the day"""
    
    with open("keys/nasa_key.txt") as api_key:
    	key = api_key.read().rstrip('\n')

    print("https://api.nasa.gov/planetary/apod?api_key="+key)
    	
    api_request = requests.get("https://api.nasa.gov/planetary/apod?api_key="+key)
    info = {}
    
    if api_request.status_code == 200:
    	info["hd_link"] = api_request.json()["hdurl"]
    	info["title"] = api_request.json()["title"]
    	info["description"] = api_request.json()["explanation"]
    # could potentially be customizable via function arguments (e.g. number of images)
    return info
    
def weather_api():
    """Returns """
    return "something"
    
print (nasa_apod())
