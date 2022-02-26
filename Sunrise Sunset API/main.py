import datetime as dt
import requests

MY_LAT = 58.310699
MY_LONG = 25.244150

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0
}

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = data["results"]["sunrise"]
sunset = data["results"]["sunset"]

current_time = dt.datetime.now()
sunrise_string = str(sunrise).split("T")
sunrise_time = sunrise_string[1].split(":")
sunset_string = str(sunset).split("T")
sunset_time = sunset_string[1].split(":")

print(current_time)
print(sunrise)
print(sunrise_string)
print(sunrise_time)
print(sunset)
print(sunset_string)
print(sunset_time)