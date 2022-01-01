import requests
from datetime import datetime as dt
from twilio.rest import Client
import os

# Get my latitude and longitude:
position = requests.get(url="http://ipinfo.io/json")
position.raise_for_status()
# Your latitude
MY_LAT = float(position.json()["loc"].split(",")[0])
# Your longitude
MY_LONG = float(position.json()["loc"].split(",")[1])
# ----------------------------------------------

# Twilio sid and token
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
# ----------------------------------------------

# Openweather.org map auth
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
API_KEY = os.environ['OWM_API_KEY']

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": API_KEY,
    "exclude": "current,minutely,daily"
}
# ----------------------------------------------

weather = requests.get(url=OWM_ENDPOINT, params=weather_params)
weather.raise_for_status()

will_rain = False
if dt.now().hour == 7:
    for n in range(0, 12):
        if weather.json()["hourly"][n]["weather"][0]["id"] < 700:
            will_rain = True

    if will_rain is True:
        message = client.messages.create(
            body="Today it's going to rain, you should bring an umbrella ☂.",
            from_='phonenumber',
            to='phonenumber'
        )
        print(message.status)
