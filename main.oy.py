import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 12.971599
MY_LONG = 77.594566
MY_EMAIL = "amruthamsha28@gmail.com"
PASSWORD = "Apr@2005"

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_lat = float(data["iss_position"]["latitude"])
    iss_lng = float(data["iss_position"]["longitude"])

    #yr position shd be +5 or -5 of current position
    if MY_LAT-5 <= iss_lat <= MY_LAT+5 or MY_LONG-5 <= iss_lng <= MY_LONG+5:
        return True

def is_night():
    parameters= {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if sunset <= time_now or time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_night() and is_iss_overhead():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject: look up \n\nThe ISS is above you in the sky."
        )



