import requests
import os
from twilio.rest import Client


# This script fetches the weather data from OpenWeatherMap API and sends an SMS alert if rain is forecasted.
# It uses Twilio API to send SMS notifications.
# Make sure to set the environment variables OWM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN,
# MY_TWILIO_PHONE_NO, and MY_PHONE_NO before running this script.


OWM_URL = "https://api.openweathermap.org/data/2.5/forecast"
OWM_API_KEY = os.environ.get("OWM_API_KEY")
LATITUDE = 59.334591
LONGITUDE = 18.063240


def get_current_weather_data() -> dict:
    """ It fetches the current weather data from OpenWeatherMap API for the given latitude and longitude
    for the next 12 hours. """
    print(OWM_API_KEY)
    parameters = {
        "lat": LATITUDE,
        "lon": LONGITUDE,
        "cnt": 4,
        "appid": OWM_API_KEY,
    }
    response = requests.get(url=OWM_URL, params=parameters)
    response.raise_for_status()
    weather_data = response.json()
    return weather_data


def is_rain_forecasted(weather_data: dict) -> bool:
    """ It checks if there is any rain forecast in given weather data. """
    rain_forecasted = False
    hourly_forecasts = weather_data['list']
    for forecast in hourly_forecasts:
        weather_id = forecast['weather'][0]['id']
        rain_forecasted = True if weather_id < 700 else rain_forecasted
    return rain_forecasted


def send_sms(msg: str) -> None:
    """ It sends an SMS with the given message using Twilio API. """
    acc_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    if not acc_sid or not auth_token:
        raise ValueError("Twilio credentials are not set in environment variables.")
    client = Client(acc_sid, auth_token)
    message = client.messages.create(
        body=msg,
        from_=os.environ.get("MY_TWILIO_PHONE_NO"),
        to=os.environ.get("MY_PHONE_NO"),
    )
    if message.status in ["queued", "sent"]:
        print("SMS sent successfully.")
    else:
        raise RuntimeError(f"Failed to send SMS: {message.status}")


def rain_alert() -> None:
    """ Main method to execute rain alert notifier app. It fetches the current weather data
    and checks if rain is forecasted. If rain is forecasted, it sends an SMS alert. """
    weather_data = get_current_weather_data()
    rain_forecasted = is_rain_forecasted(weather_data)
    print(rain_forecasted)
    if rain_forecasted:
        msg = "It's going to rain today. Remember to bring an umbrella ☔️"
        send_sms(msg)
    else:
        print("No rain forecasted today.")


if __name__ == "__main__":
    rain_alert()
