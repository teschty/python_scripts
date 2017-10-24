#!/usr/bin/env python3
"""
Fetches current weather based on IP location


Example Usage:
weather
"""

import requests


def weather():
    """main program"""

    # Fetch IP for city data
    try:
        url = "http://ip-api.com/json"
        request = requests.get(url)
        if request.status_code == 200:
            data = request.json()
            location = data['zip']
    except requests.exceptions.RequestException:
        print("Location not found")
        exit(1)

    apixu_key = "6510b92495fd472ca30155709172803&q"
    api_url = f"https://api.apixu.com/v1/current.json?key={apixu_key}={location}"
 
    # Feed city for weather info
    if data["status"] == "success":
        request = requests.get(api_url)
        if request.status_code == 200:
            data = request.json()
            printer(data)
    elif data["status"] == "fail":
        print("City not found")
        exit(1)


def printer(data):
    """Displays information from json pulled from site"""

    print("-----------------------")
    print(f"City: {data['location']['name']}")
    print(f"Temp: {data['current']['temp_f']}°F")
    print(f"Feels Like: {data['current']['feelslike_f']}°F")
    print(f"Humidity: {data['current']['humidity']}%")
    print(f"Wind speed: {data['current']['wind_mph']} mph")
    print(f"Condition: {data['current']['condition']['text']}")
    print("-----------------------")


weather()
