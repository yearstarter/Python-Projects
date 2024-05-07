import requests
import os
from twilio.rest import Client


API_key_openweathermap = 'YOUR_OWM_API_KEY'
OWM_endpoint = "https://api.openweathermap.org/data/2.5/forecast?"
account_sid = os.environ['YOUR_TWILIO_SID']
auth_token = os.environ['YOUR_TWILIO_TOKEN']


city_coord = (50, 50)  # YOUR COORDINATES HERE


# define a function to get weather
def get_weather(coord):
    parameters = {
        "lat": coord[0],
        "lon": coord[1],
        "appid": API_key_openweathermap,
        "units": "metric",
        "cnt": 4
    }
    response = requests.get(url=OWM_endpoint, params=parameters)
    response.raise_for_status()
    weather = response.json()
    # list.weather.id contains codes of weather:
    # https://openweathermap.org/weather-conditions

    rain = False
    for i in weather["list"]:
        # print(i["dt"])
        # print(i["weather"])
        for item in i["weather"]:
            if item["id"] < 800:
                rain = True
                break
        if rain:
            print(f"Bring an umbrella!")
            client = Client(account_sid, auth_token)
            message = client.messages \
                            .create(
                                body="It's going to rain. Bring an umbrella!",
                                from_='YOUR_TWILIO_NUMBER',
                                to='NUMBER_TO_SEND'
                            )
            print(message.status)
            break


get_weather(city_coord)
