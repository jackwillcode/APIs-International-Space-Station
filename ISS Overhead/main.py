import requests
from datetime import datetime
from dateutil.parser import isoparse
import time
import smtplib

# Enter your current location's latitude and longitude values (www.latlong.net)
MY_LAT = 32.535301
MY_LNG = -92.046349

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0,
}

# Enter your email credentials
sending_email = ""
sending_email_password = ""
receiving_email = ""
sending_email_smtp_address = ""

# Enter how often you want to send email (in seconds) if ISS is still overhead your current location
EMAIL_TIME_INTERVAL = 60


def is_iss_close():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # ISS location doesn't need to be exactly above your current location, so set tolerances
    iss_min_lat = iss_latitude - 5
    iss_max_lat = iss_latitude + 5
    iss_min_long = iss_longitude - 5
    iss_max_long = iss_longitude + 5

    #Your position is within +5 or -5 degrees of the ISS position.
    if iss_min_lat <= MY_LAT <= iss_max_lat and iss_min_long <= MY_LNG <= iss_max_long:
        return True
    else:
        return False


def datetime_from_utc_to_local(utc_datetime):
    now_time = time.time()
    offset = datetime.fromtimestamp(now_time) - datetime.utcfromtimestamp(now_time)
    return utc_datetime + offset


def is_night():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    # Convert sunrise and sunset into your own local time
    sunrise = int(str(datetime_from_utc_to_local(isoparse(data["results"]["sunrise"]))).split(" ")[1].split(":")[0])
    sunset = int(str(datetime_from_utc_to_local(isoparse(data["results"]["sunset"]))).split(" ")[1].split(":")[0])

    # Convert sunrise and sunset into utc time
    # sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    # sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True
    else:
        return False

# start_time = time.time()
# elapsed_time = start_time

while True:
    # Wait 60 seconds before sending email if conditions are met
    time.sleep(EMAIL_TIME_INTERVAL)

    # Send email if iss is nearby and is currently dark outside
    if is_iss_close() and is_night():
        # Smtplib object to connect to our email provider's smtp email server
        with smtplib.SMTP(sending_email_smtp_address, 587) as connection:
            # Secure our connection to email server using tls
            connection.starttls()

            # Login to email
            connection.login(user=sending_email, password=sending_email_password)
            connection.sendmail(from_addr=sending_email,
                                to_addrs=receiving_email,
                                msg=f"Subject:The International Space Station (ISS) Is Near You!\n\nGo ahead and look up at the night sky to view!"
                                )

        # Reset start/elapsed time to resend email again at next available interval
        # start_time = time.time()
        # elapsed_time = start_time
        print(f"Email message sent @ {datetime.now()}")